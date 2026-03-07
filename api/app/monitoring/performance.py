import time
import functools


def time_register(label=None):
    """
    Decorator to measure execution time of any function.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            result = func(*args, **kwargs)

            end = time.perf_counter()

            name = label if label else func.__name__
            duration = end - start

            print(f"[PERF] {name} took {duration:.2f} sec")

            return result

        return wrapper

    return decorator