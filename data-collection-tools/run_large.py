import json
import os


import code_contributors
import other_contributors
from utils.init import authenticator, config

gs = authenticator.get_githubs()
repos_file = os.path.join(os.path.dirname(__file__), 'utils/init/alot_of_repos.json')
new_repos = []

if os.path.exists(repos_file):
    with open(repos_file, 'r+') as file:
        new_repos = json.load(file)
    config.repos = config.init_2(new_repos, gs[1])
    code_contributors.run(g=gs[0], config=config)
    other_contributors.run(g=gs[0], config=config)
else:
    print('repos_file :' + repos_file + ' does not exist')

