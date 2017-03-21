import os
import utils.cache as cache

filename = os.path.basename(__file__)  # file cache key

atom = {'name': 'atom/atom',
        'key': 'aa',
        'color': '\033[92m',
        'since_sha': '58bc966053e400e2caaccb1c0a79d9afb7ebf156',
        'until_sha': '4573089108d3ebf48515f0a1c049ce22600ee878'}

codelite = {'name': 'eranif/codelite',
            'key': 'ec',
            'color': '\033[94m',
            'since_sha': '507458c98d7bc77397e54fcbe716bbdb4f06daa6',
            'until_sha': '91fcddd84101224c8fe853d8dcca82b23a36799b'}

neovim = {'name': 'neovim/neovim',
          'key': 'nv',
          'color': '\033[96m',
          'since_sha': 'c4826c300340a9e4df20964a14650caf64fc1b58',
          'until_sha': '0542baac28681050483c685c79efcb4d3c1e32ea'}

repos = [neovim, codelite, atom]


def init(g):
    print('\033[91m**  Initializing config  **')
    for repo in repos:
        key = filename + '_' + repo['key']
        repo['since'] = cache.cache(commit_to_date, key + '_since', repo=repo, g=g, sha_key=repo['since_sha'])
        repo['until'] = cache.cache(commit_to_date, key + '_until', repo=repo, g=g, sha_key=repo['until_sha'])
    print('**  Init done!  **\033[0m')


def commit_to_date(args_dict):
    repo = args_dict['repo']
    sha_key = args_dict['sha_key']
    g = args_dict['g']
    return g.get_repo(repo['name']).get_commits(sha=sha_key)[0].commit.author.date.strftime('%s')
