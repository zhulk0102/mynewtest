# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/3 10:15
@Auth ： zhulk

"""
import unittest
from common.mainTest import mainTest
from common.log import Log
import base64
from config.settings import url,browser
from common import flowlist

log = Log()
HTML_IMG_TEMPLATE = """
    <img src="data:image/png;base64, %s" width="%spx" height="%spx"/>
"""
flo_list = flowlist.get_flow_list_locals()

class myTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        log.warning("=========================START=========================\n")
        log.debug("测试用例开始执行:{}".format(self._testMethodName))
        flo = self._testMethodName.split("test_")[1]
        self.flow_list = flo_list.get(flo)

    def test_case(self):
        test = mainTest(self.flow_list,browser)
        test.driver.to(url)
        try:
            test.main(self.flow_list)
        except Exception as e:
            img_path = test.driver.save_screen_shot()
            with open(img_path, 'rb') as file:
                img = file.read()
            data = base64.b64encode(img).decode()
            # 记到日志里面展示
            # log.info(HTML_IMG_TEMPLATE % (data, 1000, 500))
            log.error('Message: %s' % str(flowlist))
            log.error(e)
            raise e
        finally:
            test.driver.quit()

    def tearDown(self):
        log.debug("测试用例执行结束:{}".format(self._testMethodName))
        log.warning("========================= END =========================\n")

    @classmethod
    def tearDownClass(cls):
        pass
