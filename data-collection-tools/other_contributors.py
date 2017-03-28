import os
from collections import defaultdict
from datetime import datetime
from pprint import pprint

from utils import cache, analyzer
from utils.pretty_printer import nc_print

file_name = os.path.basename(__file__)  # file cache key


def get_issues_data(g, repo_name, since, labels):
    unique_users = defaultdict(int)
    issues = g.get_repo(repo_name).get_issues(since=since, labels=labels, state='closed')
    for issue in issues:
        for method in dir(issue):
            nc_print(method)
        comments = issue.get_comments()
        for comment in comments:
            print(comment)
            for method in dir(comment):
                print(method)
        if not any(label.name == "duplicate" for label in issue.labels):
            unique_users[issue.user.login] += 1
        break
    return unique_users


def run(g, config):
    nc_print('----------------------------Other Contributors START----------------------------')
    problem_reporters_data = {}
    feature_proposers_data = {}
    for repo in config.repos:
        print(repo['color'] + repo['name'])
        pr_dict = cache.cache(get_issues_data,
                              key=file_name + '_' + repo['key'] + '_problem_reporters',
                              g=g,
                              repo_name=repo['name'],
                              since=datetime.fromtimestamp(int(repo['since'])),
                              labels=[g.get_repo(repo['name']).get_label("bug")])
        problem_reporters_data[repo['name']] = {}
        problem_reporters_data[repo['name']]['problem_reporters_dict'] = pr_dict
        fp_dict = cache.cache(get_issues_data,
                              key=file_name + '_' + repo['key'] + '_feature_proposers',
                              g=g,
                              repo_name=repo['name'],
                              since=datetime.fromtimestamp(int(repo['since'])),
                              labels=[g.get_repo(repo['name']).get_label("enhancement")])
        feature_proposers_data[repo['name']] = {}
        feature_proposers_data[repo['name']]['feature_proposers_dict'] = fp_dict
    analyzer.visualize_results(config.repos,
                               'problem_reporters',
                               problem_reporters_data,
                               'problem_reporters/problem_reporters_dist')
    analyzer.visualize_results(config.repos,
                               'feature_proposers',
                               feature_proposers_data,
                               'feature_proposers/feature_proposers_dist')
    nc_print('----------------------------Other Contributors END----------------------------')
    pass
