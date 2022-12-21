from typing import Callable


def through(func: Callable, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        pass


def through_decorator(func: Callable):
    def inner(*args, **kwargs):
        return through(func, *args, **kwargs)
    return inner
