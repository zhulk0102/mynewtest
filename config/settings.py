# -*- coding: utf-8 -*-
"""
@Time ： 2019/12/26 11:54
@Auth ： zhulk

"""
import os

#工作路径
basePath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
#浏览器驱动路径
driverPath = os.path.join(basePath,'drivers')
#日志路径
logPath = os.path.join(basePath,'log')
#报告路径
reportPath = os.path.join(basePath,'report')
#默认寻找延时
TIMEOUT = 5
#是否开启Js报错检查
JSCHECK = False
#常用定位
TEXT_XPATH = "//*[text()='%s']"
# 设置间隔时间
INTERVAL_TIME = 0.5
#谷歌配置(docker)
DRIVER_MODE = 'local'
DRIVER_URL = '192.168.66.66'
DRIVER_PORT = '5900'
#访问地址
url = 'http://192.168.64.12:9000/pages/login.jsp'
# 默认浏览器
browser = 'chrome'
#测试报告名称
reportName = '自动化测试报告'
#工具包路径
untilsPath = os.path.join(basePath,'utils')