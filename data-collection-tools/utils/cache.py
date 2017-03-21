import os
import json

temp_folder_path = os.path.join(os.path.dirname(__file__), os.pardir)


def exists(key):
    file_path = _make_file_path(key)
    return os.path.exists(file_path)


def get(key):
    if exists(key):
        with open(_make_file_path(key), "r") as file:
            return json.load(file)
    return None


def store(key, value):
    file_path = _make_file_path(key)
    with open(file_path, 'w') as file:
        json.dump(value, file)
    return value


def cache(func, key, **kwargs):
    """"Returns the data if stored, otherwise it calls the function and stores the returned value"""
    cached = get(key)
    if cached:
        return cached
    else:
        value = store(key, func(**kwargs))
        return value


def _make_file_path(key):
    return temp_folder_path + '/cache_files/' + key + '.json'
