import os
import pickle

temp_folder_path = os.path.join(os.path.dirname(__file__), os.pardir)


def get(key):
    file_path = _fp(key)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)
    return None


def store(key, value):
    file_path = _fp(key)
    with open(file_path, 'wb') as file:
        pickle.dump(str(value), file)
    return value

def cache(func, key, **kwargs):
    cached = get(key)
    if cached:
        return cached
    else:
        value = store(key, func(kwargs))
        return value


def _fp(key):
    return temp_folder_path + '/temp/' + key + '.pickle'
