import os.path
import tomllib


def get_version():
    if os.path.exists("pyproject.toml"):
        path = "pyproject.toml"
    else:
        path = "../pyproject.toml"
    with open(path, "rb") as f:
        data = tomllib.load(f)
        return data["tool"]["poetry"]["version"]


__version__ = f"ChatBot Charlie v{get_version()}"
