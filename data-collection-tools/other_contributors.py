import os
from collections import defaultdict
from datetime import datetime

from github.GithubException import RateLimitExceededException

from utils import cache, analyzer
from utils.pretty_printer import nc_print
from utils.init import config

file_name = os.path.basename(__file__)  # file cache key


def get_issues_data(g, repo_name, since, until, labels):
    try:
        issues = get_issues(g, repo_name, since, labels, 'closed')
        unique_users = get_unique_users(issues, until)
    except RateLimitExceededException:
        g = new_g(g)
        issues = get_issues(g, repo_name, since, labels, 'closed')
        unique_users = get_unique_users(issues, until)
    return unique_users


def get_defect_repair_time(g, repo, since, until):
    try:
        labels = [g.get_repo(repo['name']).get_label(repo['bug'])]
        issues = get_issues(g, repo['name'], since, labels, 'closed')
        repair_times = get_repair_times(issues, until)
    except RateLimitExceededException:
        g = new_g(g)
        labels = [g.get_repo(repo['name']).get_label(repo['bug'])]
        issues = get_issues(g, repo['name'], since, labels, 'closed')
        repair_times = get_repair_times(issues, until)
    return repair_times


def get_issues(g, repo_name, since, labels, state):
    return g.get_repo(repo_name).get_issues(since=since, labels=labels, state=state)


def get_unique_users(issues, until):
    unique_users = defaultdict(int)
    for issue in issues:
        if int(issue.created_at.timestamp()) < int(until):
            if not any(label.name == "duplicate" for label in issue.labels):
                unique_users[issue.user.login] += 1
    return unique_users


def new_g(g):
    print("RATE LIMIT EXCEEDED TRYING WITH NEW ACCOUNT")
    return config.get_other_g(g)


def get_repair_times(issues, until):
    repair_times = []
    for issue in issues:
        if int(issue.closed_at.timestamp()) < until:
            if not any(label.name == "duplicate" for label in issue.labels):
                repair_times.append(((int(issue.closed_at.timestamp()) - int(issue.created_at.timestamp())) / 3600)/24)
    return repair_times if len(repair_times) > 0 else [0]


def run(g, config):
    nc_print('----------------------------Other Contributors START----------------------------')
    problem_reporters_data = {}
    feature_proposers_data = {}
    repair_times_data = {}
    for repo in config.repos:
        print(repo['color'] + repo['name'])
        since = datetime.fromtimestamp(int(repo['since']))
        until = int(repo['until'])
        pr_dict = cache.cache(get_issues_data,
                              key=file_name + '_' + repo['key'] + '_problem_reporters',
                              g=g,
                              repo_name=repo['name'],
                              since=since,
                              until=until,
                              labels=[g.get_repo(repo['name']).get_label(repo['bug'])])
        problem_reporters_data[repo['name']] = {}
        problem_reporters_data[repo['name']]['problem_reporters_dict'] = pr_dict
        fp_dict = cache.cache(get_issues_data,
                              key=file_name + '_' + repo['key'] + '_feature_proposers',
                              g=g,
                              repo_name=repo['name'],
                              since=since,
                              until=until,
                              labels=[g.get_repo(repo['name']).get_label(repo['enhancement'])])
        feature_proposers_data[repo['name']] = {}
        feature_proposers_data[repo['name']]['feature_proposers_dict'] = fp_dict
        repair_times = cache.cache(get_defect_repair_time,
                                   key=file_name + '_' + repo['key'] + '_repair_times',
                                   g=g,
                                   repo=repo,
                                   since=since,
                                   until=until,)
        repair_times_data[repo['name']] = {}
        repair_times_data[repo['name']]['repair_times_array'] = repair_times
    analyzer.visualize_results(config.repos,
                               'problem_reporters',
                               problem_reporters_data,
                               'problem_reporters/problem_reporters',
                               x_axis='problem reporters')
    analyzer.visualize_results(config.repos,
                               'feature_proposers',
                               feature_proposers_data,
                               'feature_proposers/feature_proposers',
                               x_axis='feature proposers')
    analyzer.analyze_repair_time(config.repos,
                                 'repair_times',
                                 repair_times_data,
                                 'repair_times/repair_times')
    nc_print('----------------------------Other Contributors END----------------------------')
    pass
