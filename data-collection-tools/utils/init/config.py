import os
import utils.cache as cache

filename = os.path.basename(__file__)  # file cache key

atom = {'name': 'atom/atom',
        'key': 'aa',
        'color': '\033[92m',
        "bug": "bug",
        "enhancement": "enhancement",
        'since_sha': '58bc966053e400e2caaccb1c0a79d9afb7ebf156',
        'until_sha': '4573089108d3ebf48515f0a1c049ce22600ee878'}

neovim = {'name': 'neovim/neovim',
          'key': 'nv',
          'color': '\033[96m',
          "bug": "bug",
          "enhancement": "enhancement",
          'since_sha': 'c4826c300340a9e4df20964a14650caf64fc1b58',
          'until_sha': '0542baac28681050483c685c79efcb4d3c1e32ea'}

# repos = [testrepo]
repos = [neovim, atom]
# repos = [neovim, codelite, atom]


def init(g):
    print('\033[91m**  Initializing config  **')
    for repo in repos:
        key = filename + '_' + repo['key']
        repo['since'] = cache.cache(commit_to_date, key + '_since', repo=repo, g=g, sha_key=repo['since_sha'])
        repo['until'] = cache.cache(commit_to_date, key + '_until', repo=repo, g=g, sha_key=repo['until_sha'])
    print('**  Init done!  **\033[0m')


def commit_to_date(repo, sha_key, g):
    repo = repo
    sha_key = sha_key
    g = g
    return g.get_repo(repo['name']).get_commits(sha=sha_key)[0].commit.author.date.strftime('%s')


other_g = {}


def init_2(new_repos, g2):
    """
    This method is used if you want to gather information from the same date for all repos.
    """
    global other_g
    other_g = g2
    print('\033[91m**  Initializing config (method 2)  **')
    for repo in new_repos:
        repo['since'] = "1451606400"  # 01 Jan 2016
        repo['until'] = "1483228800"  # 01 Jan 2017
    print('**  Init done!  **\033[0m')
    return new_repos


def get_other_g(other_other_g):
    """
    This function is used to avoid rate limit exceeded 
    """
    global other_g
    outgoing_g = other_g
    other_g = other_other_g
    print('other_g: ' + str(other_g._Github__requester._Requester__authorizationHeader))
    print('other_other_g: ' + str(other_other_g._Github__requester._Requester__authorizationHeader))
    print('outgoing_g: ' + str(outgoing_g._Github__requester._Requester__authorizationHeader))
    return outgoing_g
