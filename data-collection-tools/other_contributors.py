import os
from collections import defaultdict
from datetime import datetime
from pprint import pprint

from utils import cache, analyzer
from utils.pretty_printer import nc_print

file_name = os.path.basename(__file__)  # file cache key


def get_issues_data(g, repo_name, since, until, labels):
    unique_users = defaultdict(int)
    issues = g.get_repo(repo_name).get_issues(since=since, labels=labels, state='closed')
    for issue in issues:
        if int(issue.created_at.strftime('%s')) < until:
            if not any(label.name == "duplicate" for label in issue.labels):
                unique_users[issue.user.login] += 1
    return unique_users


def get_defect_repair_time(g, repo, since, until):
    labels = [g.get_repo(repo['name']).get_label(repo['bug'])]
    issues = g.get_repo(repo['name']).get_issues(since=since, labels=labels, state='closed')
    repair_times = []
    for issue in issues:
        if int(issue.closed_at.strftime('%s')) < until:
            if not any(label.name == "duplicate" for label in issue.labels):
                repair_times.append(((int(issue.closed_at.strftime('%s')) - int(issue.created_at.strftime('%s'))) / 3600)/24)
    return repair_times


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
