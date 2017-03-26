import os
from collections import defaultdict
from datetime import datetime
from pprint import pprint

from utils import cache, analyzer

file_name = os.path.basename(__file__)  # file cache key


def get_issues_data(g, repo_name, since, labels):
    unique_users = defaultdict(int)
    issues = g.get_repo(repo_name).get_issues(since=since, labels=labels)
    for issue in issues:
        unique_users[issue.user.login] += 1
    return unique_users


def run(g, config):
    print('----------------------------Problem reporters START----------------------------')
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
        pprint(pr_dict)
        problem_reporters_data[repo['name']] = {}
        problem_reporters_data[repo['name']]['problem_reporters_dict'] = pr_dict
        fp_dict = cache.cache(get_issues_data,
                              key=file_name + '_' + repo['key'] + '_feature_proposers',
                              g=g,
                              repo_name=repo['name'],
                              since=datetime.fromtimestamp(int(repo['since'])),
                              labels=[g.get_repo(repo['name']).get_label("enhancement")])
        pprint(fp_dict)
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
    print('----------------------------Problem reporters END----------------------------')
    pass
