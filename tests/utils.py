from functools import wraps
from importlib import import_module
import inspect
import os

from bs4 import BeautifulSoup


def mksoup(path):
    with open(path) as f:
        soup = BeautifulSoup(f, 'lxml')
    return soup


def mksoup_decorator(relpath=None):
    stk = inspect.stack()[1]
    drc = os.path.dirname(stk.filename)
    def decorator(func):
        @wraps(func)
        def inner(*fargs, **fkwargs):
            nonlocal relpath
            if not relpath:
                fullpath = os.path.join(
                    drc, 'snippets', func.__name__ + '.html')
            else:
                fullpath = os.path.join(drc, relpath)
            #fkwargs['soup'] = fullpath
            with open(fullpath) as f:
                fkwargs['soup'] = BeautifulSoup(f, 'lxml')
            return func(*fargs, **fkwargs)
        return inner
    return decorator


def get_cases(__file, __package):
    cases = []
    dirname = os.path.dirname(__file)
    for mod in os.listdir(dirname):
        if mod.startswith('case'):
            cases.append(import_module('.'+mod, __package))
    return cases
