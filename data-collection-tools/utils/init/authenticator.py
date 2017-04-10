from github import Github
import json
import os


def get_githubs():
    """Authenticates the user and returns

    Prompts the users for credentials if they're missing

    :return: a Github instance
    """
    g1 = _get_github(os.path.join(os.path.dirname(__file__), 'credentials1.json'))
    g2 = _get_github(os.path.join(os.path.dirname(__file__), 'credentials2.json'))
    return [g1, g2]


def _get_github(file_name):
    credentials = {}
    if os.path.exists(file_name):
        with open(file_name, "r+") as file:
            credentials = json.load(file)
    else:
        print('\033[93m Creating credentials file. \033[0m')
        credentials['u'] = input('username: ')
        credentials['pw'] = input('password: ')
        with open(file_name, 'w') as new_file:
            json.dump({'u': credentials['u'], 'pw': credentials['pw']}, new_file)

    return Github(login_or_token=credentials['u'], password=credentials['pw'], per_page=100)
