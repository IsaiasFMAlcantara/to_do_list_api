import os

def _open_file(file):
    raiz = os.path.join(os.getcwd())
    path = f'{raiz}/{file}'
    with open(path, "r") as file:
        return file.read()