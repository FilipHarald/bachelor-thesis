from github import Github
import json
import os


def get_github():
    """Authenticates the user and returns

    Prompts the users for credentials if they're missing

    :return: a Github instance
    """
    cred_file = os.path.join(os.path.dirname(__file__), 'credentials.json')
    credentials = {}

    if os.path.exists(cred_file):
        with open(cred_file, "r+") as file:
            credentials = json.load(file)
    else:
        print('\033[93m Creating credentials file. \033[0m')
        credentials['u'] = input('username: ')
        credentials['pw'] = input('password: ')
        with open(cred_file, 'w') as new_file:
            json.dump({'u': credentials['u'], 'pw': credentials['pw']}, new_file)

    return Github(credentials['u'], credentials['pw'])
