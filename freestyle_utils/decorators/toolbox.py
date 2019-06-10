import time
import signal
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
        print('%r  %6.8f seconds' % (func.__name__, te - ts))
        return result
    return timed


def set_timeout(num, callback):
    """
    处理函数执行超时的装饰器, 调用回调函数
    """
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap


def after_timeout():  # 超时后的处理函数
    print("Time out!")


