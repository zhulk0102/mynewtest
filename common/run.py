# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/3 14:17
@Auth ： zhulk

"""

import sys
from config.settings import basePath
from common.mytest import myTest
from common import flowlist
import unittest
from utils import BeautifulReport
import time
import os
from config.settings import reportPath,logPath,reportName
from common.log import Log
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import smtplib

log = Log()

sys.path.append(basePath)


def load_case(suite):
    """装载测试用例"""
    # 这里在装载的时候，通过改变测试用例的名字可以实现
    # 1.装载相同的测试用例
    # 2.多个测试用例调用的一个执行方法test_case
    # 3.所有的name对应的都是test_case
    def set_case(cls, name, remark):
        setattr(cls, name, cls.test_case)
        testcase = getattr(cls, name)
        testcase.__doc__ = remark
        suite.addTest(cls(name))
    # 获取flow_list的属性
    flow_list_locals = flowlist.get_flow_list_locals()
    flowlis = flow_list_locals.get('flow')
    if flowlis is None:
        return
    for flow in flowlis:
        for flowkey in flow_list_locals:
            if flow_list_locals[flowkey]== flow:
                test_case_name = "test_%s" % flowkey
                set_case(myTest,name=test_case_name, remark=test_case_name)
                log.debug("SUCCESS 装载测试用例: %s" % test_case_name)

def get_report_name(name='TestResult'):
    """生成Report Name"""
    now = time.strftime('%Y%m%d_%H%M%S')
    return '%s%s.html' % (name, now)

def creatReport():
    test_report = os.path.join(reportPath, 'testReport')
    if not os.path.exists(test_report):
        os.makedirs(test_report)
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    return test_report

def newReport():
    lists = os.listdir(reportPath+'\\'+'testReport')
    print(lists)
    lists.sort(key=lambda fn: os.path.getmtime(reportPath +'\\'+'testReport'+'\\' + fn))
    newpath = os.path.join(reportPath+'\\'+'testReport'+'\\', lists[-1])
    return newpath

def sendEmail(filename):
    mailfrom = 'zlk_0102@163.com'
    mailto = '517122472@qq.com'
    f = open(filename, 'rb')
    mailcontent = f.read()
    f.close()
    msg = MIMEMultipart()
    msg.attach(MIMEText(mailcontent, _subtype='html', _charset='utf-8'))
    att = MIMEText(mailcontent, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=' + filename
    msg.attach(att)
    msg['Subject'] = Header(u'商旅测试自动化测试报告', 'utf-8')
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['From'] = mailfrom
    msg['to'] = mailto
    username = 'zlk_0102@163.com'
    password = 'nicaiya0102'
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(mailfrom, mailto, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    load_case(suite)
    test_report = creatReport()
    #正常模式
    # result = BeautifulReport.BeautifulReport(suite)
    # result.report(reportName, get_report_name(), logPath, test_report)
    # res_report = newReport()
    # log.debug('最新的报告为 %s'%(res_report))
    # sendEmail(res_report)
    #调试模式
    unittest.TextTestRunner().run(suite)