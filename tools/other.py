import itertools


def any_from(*args, in_: str):
    if not isinstance(args[0], str):
        args = itertools.chain(args[0], args[1:])
    return any((i in in_ for i in args))