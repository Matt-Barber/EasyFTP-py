from functools import wraps


def log_func_call(func):
    """logs a function / method call """
    import logging
    logging.basicConfig(
        filename='./EasyFTP/log/debug_func_call.log',
        level=logging.DEBUG,
        format='%(asctime)s %(message)s'
    )
    @wraps(func)
    def inner(*args, **kwargs):
        logging.debug(
            (
                "[{func}] called with args {args} |"
                "| kwargs {kwargs}").format(
                    func=func.__name__,
                    args=args,
                    kwargs=kwargs
                )
        )
        return func(*args, **kwargs)
    return inner
