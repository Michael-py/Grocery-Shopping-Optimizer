# Libraries for time in cache and cache  
from datetime import datetime, timedelta
import functools as ft
from functools import lru_cache, wraps

#memoization function 
def timed_lru_cache(seconds: int =43200, maxsize=None): #12 hours cache and no maxsize limit 
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache