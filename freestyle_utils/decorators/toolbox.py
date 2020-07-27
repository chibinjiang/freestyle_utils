import json
import time
import signal
import traceback
from functools import wraps
import hashlib
from itertools import chain
from typing import Callable, Any

from redis import StrictRedis


def async_retry(exceptions, retries=3, delay=2, back_off=3, logger=None):
    """
    加上重试, 应该是执行了 retries + 1 次
    :param exceptions: 异常列表
    :param retries:
    :param delay: 基数
    :param back_off: 底数
    :param logger:
    :return:
    """

    def deco_retry(f):
        @wraps(f)
        async def f_retry(*args, **kwargs):
            for i in range(retries):
                idle_time = delay * pow(back_off, i)
                try:
                    result = await f(*args, **kwargs)
                    return result
                except exceptions as e:
                    if logger:
                        logger.error(traceback.format_exc())
                    else:
                        traceback.print_exc()
                    time.sleep(idle_time)
            result = await f(*args, **kwargs)
            return result

        return f_retry

    return deco_retry


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


def catch_400_message(logger=None):
    """
    捕获 Resource 的方法的异常, 返回 400 和 error_message
    :param logger: logger
    :return:
    """

    def deco_catch(func):
        @wraps(func)
        def catch_exception(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception as e:
                if logger:
                    logger.error("TRACEBACK", traceback.format_exc())
                else:
                    traceback.print_exc()
                return {'error_message': e.message}, 400

        return catch_exception

    return deco_catch


def _gen_key(func: Callable, *args, **kwargs):
    """
    make cache key with func name & args & kwargs
    根据function & args & kwargs 生成缓存key

    :param func: function
    :param args: function`s args
    :param kwargs: function`s kwargs
    :return: key[str]
    """

    def parameter_check(x: Any):
        """
        parameter check
        参数检查

        :param x: parameter
        :return: bool
        """
        return (hasattr(x, '__str__')) and (isinstance(x, type) is False)

    # make cache args & cache kwargs
    cached_args = map(str, filter(parameter_check, args))
    cached_kwargs = map(str, filter(parameter_check, kwargs.values()))

    # make a formatted key & md5 args
    args_key = '_'.join(chain(cached_args, cached_kwargs)).encode('utf8')
    key = f'{func.__module__}.{func.__name__}.{hashlib.md5(args_key).hexdigest() if len(args_key) != 0 else ""}'
    return key


# 改成 装饰器
# 有没有办法识别出 self 参数
def cache_key(f):
    def deco_cache(*args, **kwargs):
        print('获取位置参数内容', *args)
        print('获取位置参数元祖', args)
        print('获取关键字参数的key', *kwargs)
        key = _gen_key(f, *args, **kwargs)
        print(key)
        return key

    return deco_cache


redis_conn = StrictRedis()


def cache_by_redis(expire=None):
    def deco_cache(func):
        @wraps(func)
        def cache(*args, **kwargs):
            key = _gen_key(func, *args, **kwargs)
            cache_value = redis_conn.get(key)
            if cache_value is not None:
                value = json.loads(cache_value)
            else:
                # 没有
                value = func(*args, **kwargs)
                cache_value = json.dumps(value)
                if isinstance(expire, int):
                    redis_conn.setex(key, cache_value, expire)
                else:
                    redis_conn.set(key, cache_value)
            return value
        return cache

    return deco_cache
