import json
import os
from collections import defaultdict
from datetime import datetime

from utils import cache, analyzer
from utils.pretty_printer import nc_print
from utils.init import config
from github.GithubException import RateLimitExceededException

file_name = os.path.basename(__file__)  # file cache key
json_file = os.path.join(os.path.dirname(__file__), os.pardir) + 'commits_counter.json'


def get_contributors_data(g, repo_name, since, until):
    try:
        commits = g.get_repo(repo_name).get_commits(since=since, until=until)
        commit_data = get_commits_data(commits)
    except RateLimitExceededException:
        print("RATE LIMIT EXCEEDED TRYING WITH NEW ACCOUNT")
        g = config.get_other_g(g)
        commits_rest = g.get_repo(repo_name).get_commits(since=since, until=until)
        with open(json_file, "r") as file:
            counter = json.load(file)
        one = commits[:counter]
        two = commits_rest[counter:]
        print(type(one))
        new_commits = one + two
        commit_data = get_commits_data(new_commits)
    return commit_data


def get_commits_data(commits):
    unique_users = defaultdict(int)
    addition_dict = defaultdict(int)
    deletion_dict = defaultdict(int)
    counter = 0
    for commit in commits:
        with open(json_file, 'w') as file:
            json.dump(counter, file)
        unique_users[commit.commit.author.name] += 1
        addition_dict[commit.commit.author.name] += commit.stats.additions
        deletion_dict[commit.commit.author.name] += commit.stats.deletions
        counter += 1
    return {'commits_dict': unique_users,
            'additions_dict': addition_dict,
            'deletions_dict': deletion_dict}


def run(g, config):
    nc_print('----------------------------Code contributors START----------------------------')
    contributors_data = {}
    for repo in config.repos:
        print(repo['color'] + repo['name'])
        contributors_data[repo['name']] = cache.cache(get_contributors_data,
                                                      key=file_name + '_' + repo['key'] + '_contributors',
                                                      g=g,
                                                      repo_name=repo['name'],
                                                      since=datetime.fromtimestamp(int(repo['since'])),
                                                      until=datetime.fromtimestamp(int(repo['until'])))
    analyzer.visualize_results(config.repos, 'commits', contributors_data, 'code_contributors/commits')
    analyzer.visualize_results(config.repos, 'additions', contributors_data, 'code_contributors/additions', 'LoC')
    analyzer.visualize_results(config.repos, 'deletions', contributors_data, 'code_contributors/deletions', 'LoC')

    nc_print('----------------------------Code contributors END----------------------------')
    pass
