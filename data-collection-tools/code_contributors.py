import os
import matplotlib.pyplot as plt
import utils.cache as cache
from collections import Counter


from utils.analyzer import get_distribution

key = os.path.basename(__file__)  # file cache key


def get_repo_contributors(repo, g):
    print(repo['color'] + repo['name'])
    print('--------' + repo['since'])
    users = cache.get(key + '_users')
    if users:
        return users
    else:
        users = []
        for commits in g.get_repo(repo['name']).get_commits(since=repo['since'],
                                                            until=repo['until']):
            users.append(commits.commit.author.name)
        cache.store(key + '_users', users)
    return users


def analyze_users(repo, users):
    output = [repo['color'] + repo['name'],
              'All users (' + str(len(users)) + '): ' + str(users)]
    unique_dict = Counter(users)
    output.append('Unique users(' + str(len(unique_dict)) + '): ' + str(unique_dict))
    plt.plot(get_distribution(unique_dict), label=repo['name'])
    return '\n'.join(output)
