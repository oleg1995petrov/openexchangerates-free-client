from time import sleep


def retry(func):
    """Permanently calls the function if result is None."""
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        while res is None:
            sleep(10)
            print('RETRYING')
            retry(func)
        return res
    return wrapper
