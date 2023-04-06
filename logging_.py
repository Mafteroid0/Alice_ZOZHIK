import typing

from loguru import logger

DO_LOGGING = True
WRITE_LOGS = False

if DO_LOGGING and WRITE_LOGS:
    logger.add('zozhik.log', level='DEBUG', rotation='10 mb', compression='tar.xz', enqueue=True)


def logged(f: typing.Callable):
    def wrapper(*args, **kwargs):
        if not DO_LOGGING:
            return f(*args, **kwargs)

        try:
            res = f(*args, **kwargs)
        except BaseException as e:
            logger.exception(f'tried to call {f} with args {args} and kwargs {kwargs}, but raised {e}')
            raise e
        else:
            logger.debug(f'{f} called with args {args} and kwargs {kwargs} and returned {res}')
            return res

    return wrapper
