import typing

from loguru import logger

logger.add('zozhik.log', level='INFO', rotation='10 mb', compression='tar.xz', enqueue=True)


def logged(f: typing.Callable):
    def wrapper(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
        except BaseException as e:
            logger.exception(f'tried to call {f} with args {args} and kwargs {kwargs}, but raised {e}')
        else:
            logger.info(f'{f} called with args {args} and kwargs {kwargs} and returned {res}')
    return wrapper
