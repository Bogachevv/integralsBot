import sys


def logger(f):
    def foo(*args, **kwargs):
        print(f"Running {f.__name__} with {args=} and {kwargs=}")
        return f(*args, **kwargs)

    return foo
