import time
import traceback
from functools import wraps


def retry(exceptions, tries=3, delay=3, backoff=2, logger=None):
    """
    retry decorator, if raise some exceptions, retry <tries> times.
    Sleep Intervel: pow(2, try_time) * delay
    Use example:
        ```
        @retry(Exception, tries=2, delay=1, backoff=2)
        ```
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.error(msg)
                        logger.error(traceback.format_exc())
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


def timeit(func):
    """
    How much time the function costs
    """
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        print '%r  %6.8f seconds' % (method.__name__, te - ts)
        return result
    return timed

