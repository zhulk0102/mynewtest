# -*- coding: utf-8 -*-
"""
@Time ： 2019/12/30 15:05
@Auth ： zhulk

"""
from functools import wraps
from common.basepage import basePage
from common.ownerror import RouterNameRepeatError
urlpatterns = dict()

# 将url与方法绑定
def router(urlname):
    def fool(func):
        if urlname in urlpatterns.keys():
            raise RouterNameRepeatError('url repeat: %s' % urlname)
        urlpatterns[urlname] = func
        @wraps(func)
        def test(*args, **kwargs):
            return func(*args, **kwargs)
        return test
    return fool

class mainTest(object):
    data_pool = dict()
    '''所有的page类都应该继承该类,页面操作的方法需要注册router'''
    def __init__(self,flow_list,browser):
        import pages
        self.driver = basePage(browser_type = browser)
        self.flow_list = flow_list

    def main(self, flow):
        for key in flow.keys():
            if key in urlpatterns.keys():
                _self = self._get_self(urlpatterns[key])
                if isinstance(flow[key], str):
                    if flow[key] == '':
                        urlpatterns[key](_self, )
                    else:
                        urlpatterns[key](_self, flow[key])
                else:
                    urlpatterns[key](_self, *flow[key])

    def _get_self(self, func):
        m = __import__(name=func.__module__)
        for a in dir(m):
            attr = getattr(m, a)
            if type(attr) == type and issubclass(attr, mainTest) and hasattr(attr, func.__name__):
                ins = attr(self.flow_list, self.driver.type).set_driver(self.driver)
                return ins

    def set_driver(self, driver):
        self.driver = driver
        return self

    # 前置步骤，继承即可
    def pre_operation(self):
        pass

    # 后置步骤，继承即可
    def pos_operation(self):
        pass

