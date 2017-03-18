import os
import utils.cache as cache

key = os.path.basename(__file__)  # file cache key

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
          'key': 'nn',
          'color': '\033[96m',
          'since_sha': 'c4826c300340a9e4df20964a14650caf64fc1b58',
          'until_sha': '0542baac28681050483c685c79efcb4d3c1e32ea'}

repos = [neovim, codelite, atom]


def init(g):
    print('\033[91m**  Initializing config  **')
    for repo in repos:
        temp_key = key + '_' + repo['key']
        since_cached = cache.get(temp_key + '_since')
        until_cached = cache.get(temp_key + '_until')
        repo['since'] = since_cached if since_cached \
            else cache.store(temp_key + '_since',
                             g.get_repo(repo['name']).get_commits(
                                 sha=repo['since_sha'])[0].commit.author.date.strftime('%s'))
        repo['until'] = until_cached if until_cached \
            else cache.store(temp_key + '_until',
                             g.get_repo(repo['name']).get_commits(
                                 sha=repo['until_sha'])[0].commit.author.date.strftime('%s'))
    print('**  Init done!  **\033[0m')

