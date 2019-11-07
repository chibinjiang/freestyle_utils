# -*- coding: utf-8 -*-

class DotDict(dict):
    """
    为了让字典支持key和点索引的方式, 将字典的内容赋给__dict__
    Usage:
        d = {'a': 1, 'b': 2}
        d = DotDict(d)
        d.a  # 1
        d['a']  # 1
    """
    def __init__(self, *args, ** kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

