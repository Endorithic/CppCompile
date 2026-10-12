from os import environ
from shutil import which


def get_default_compiler() -> str | None:
    """Returns the user's default compiler.

    First checks the CXX environment variable. If this variable is not set, the function
    checks if clang++ and g++ are present, in that order, and uses the first one found.
    If neither are found, return None.
    """
    if "CXX" in environ:
        return environ["CXX"]

    if which("clang++"):
        return "clang++"
    elif which("g++"):
        return "g++"

    return None
