from time import sleep


def retry(func):
    """Permanently calls the function if result is None."""
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        counter = 1
        while res is None:
            if counter == 6:
                print('Cannot receive data. Try again later.')
                exit()
            print(f'RETRYING ({counter})')
            counter += 1
            sleep(30)
            retry(func)
        return res
    return wrapper
