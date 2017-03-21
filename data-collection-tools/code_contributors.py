import os
from datetime import datetime

import matplotlib.pyplot as plt
import utils.cache as cache
from collections import Counter


from utils.analyzer import get_distribution

file_name = os.path.basename(__file__)  # file cache key


def get_repo_contributors(repo, g):
    print(repo['color'] + repo['name'])
    key = file_name + '_' + repo['key'] + '_users'
    since = datetime.fromtimestamp(int(repo['since']))
    until = datetime.fromtimestamp(int(repo['until']))
    users = cache.cache(get_repo_commits, key=key ,g=g, repo_name=repo['name'], since=since, until=until)
    return users

def get_repo_commits(args_dict):
    users = []
    commits = args_dict['g'].get_repo(args_dict['repo_name']).get_commits(since=args_dict['since'], until=args_dict['until'])
    for commit in commits:
        users.append(commit.commit.author.name)
    return users


def analyze_users(repo, users):
    output = [repo['color'] + repo['name'],
              'All users (' + str(len(users)) + '): ' + str(users)]
    print(type(users))
    unique_dict = Counter(users)
    output.append('Unique users(' + str(len(unique_dict)) + '): ' + str(unique_dict))
    plt.plot(get_distribution(unique_dict), label=repo['name'])
    return '\n'.join(output)


def run(g, config):
    print('----------------------------Code contributors----------------------------')
    results = []
    for repo in config.repos:
        contributors = get_repo_contributors(repo, g)
        results.append(analyze_users(repo, contributors))
    plt.ylabel('users (%)')
    plt.xlabel('commits (%)')
    plt.legend()
    plt.savefig('results/code_contributors/commits_dist.png')
    plt.savefig('results/code_contributors/commits_dist.pdf')
    for res in results:
        print(res)
    pass
