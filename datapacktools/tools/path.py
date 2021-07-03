import os

def is_valid(path: str) -> bool:
    return path.split(os.sep)[-2] == 'datapacks'

def is_empty(path: str) -> bool:
    files = os.listdir(path)
    return ( 
        'pack.mcmeta' not in files 
        and
        'data' not in files
    )

def datapack_name(path: str) -> str:
    return path.split(os.sep)[-1]

def makedirs(*args):
    if not os.path.exists(os.path.join(*args)):
        os.makedirs(os.path.join(*args))