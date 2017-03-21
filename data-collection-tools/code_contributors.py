import os
from collections import defaultdict, Counter
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
from utils import cache, analyzer, plotter

file_name = os.path.basename(__file__)  # file cache key


def analyze_users(repo, dict, label):
    output = [repo['color'] + repo['name'], 'Unique users(' + str(len(dict)) + '): ' + str(dict)]
    plt.plot(analyzer.get_distribution(dict), label=label)
    return '\n'.join(output)


def get_contributors_data(g, repo_name, since, until):
    unique_users = defaultdict(int)
    addition_dict = defaultdict(int)
    deletion_dict = defaultdict(int)
    commits = g.get_repo(repo_name).get_commits(since=since, until=until)
    for commit in commits:
        unique_users[commit.commit.author.name] += 1
        addition_dict[commit.commit.author.name] += commit.stats.additions
        deletion_dict[commit.commit.author.name] += commit.stats.deletions
    return {'commits_dict': unique_users,
            'additions_dict': addition_dict,
            'deletions_dict': deletion_dict}


def visualize_results(repos, datatype, contributors_data):
    for repo in repos:
        analyze_users(repo, contributors_data[repo['name']][datatype + '_dict'], repo['name'])
    plotter.save('users (%)', datatype + ' (%)', 'code_contributors/' + datatype + '_dist')


def run(g, config):
    print('----------------------------Code contributors START----------------------------')
    contributors_data = {}
    for repo in config.repos:
        print(repo['color'] + repo['name'])
        contributors_data[repo['name']] = cache.cache(get_contributors_data,
                                                      key=file_name + '_' + repo['key'] + '_contributors',
                                                      g=g,
                                                      repo_name=repo['name'],
                                                      since=datetime.fromtimestamp(int(repo['since'])),
                                                      until=datetime.fromtimestamp(int(repo['until'])))
    visualize_results(config.repos, 'commits', contributors_data)
    visualize_results(config.repos, 'additions', contributors_data)
    visualize_results(config.repos, 'deletions', contributors_data)

    pprint(contributors_data)
    print('----------------------------Code contributors END----------------------------')
    pass
