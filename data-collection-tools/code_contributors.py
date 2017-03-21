import os
from datetime import datetime

import matplotlib.pyplot as plt
import utils.cache as cache
from collections import Counter


from utils.analyzer import get_distribution

key = os.path.basename(__file__)  # file cache key


def get_repo_contributors(repo, g):
    print(repo['color'] + repo['name'])
    temp_key = key + '_' + repo['key'] + '_users'
    cached_users = cache.get(temp_key)
    if cached_users:
        return cached_users
    else:
        users = []
        since = datetime.fromtimestamp(int(repo['since']))
        until = datetime.fromtimestamp(int(repo['until']))
        for commits in g.get_repo(repo['name']).get_commits(since=since, until=until):
            users.append(commits.commit.author.name)
        cache.store(temp_key, users)
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
