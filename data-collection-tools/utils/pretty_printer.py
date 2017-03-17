import json
"""JSON printer"""

def j_print(str):
    """JSON print"""
    print(json.dumps(str))


def jp_print(str):
    """JSON pretty print"""
    print(json.dumps(str, indent=4))
