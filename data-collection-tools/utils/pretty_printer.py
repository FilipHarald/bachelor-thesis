import json
"""JSON printer"""


def j_print(string):
    """JSON print"""
    print(json.dumps(string))


def jp_print(string):
    """JSON pretty print"""
    print(json.dumps(string, indent=4))


def nc_print(string):
    print('\033[0m' + string)
