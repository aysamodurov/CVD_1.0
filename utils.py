import time
import logging


def executable_time(f):

    def wrapper(*args,**kwargs):
        start_time = time.perf_counter()
        res = f(*args, **kwargs)
        finish_time = time.perf_counter()
        logging.info(f"Executable time function {f} is {finish_time-start_time}")
        return res
    
    return wrapper