# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/13 16:34
@Auth ： zhulk

"""
from common.mainTest import mainTest,router
import random
import datetime

class tripPage(mainTest):
    def getdata(self):
        ran = random.randint(1,32)
        yearMonth = (datetime.datetime.now()+ datetime.timedelta(days=ran)).strftime("%Y-%m")
        monthDate = (datetime.datetime.now()+ datetime.timedelta(days=ran)).strftime("%d")
        monthLength = len(self.driver.find_elements('//*[@id="container"]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/div'))
        for i in range(1, monthLength):
            yearMonthIfo =self.driver.find_elements('//*[@id="container"]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/div[%d]/div'%(i))
            if yearMonthIfo.text == yearMonth:
                dateLength = len(self.driver.find_elements('//*[@id="container"]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/div[1]/span'))
                for j in range(1,dateLength):
                    dateIfo = self.driver.find_elements('//*[@id="container"]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/div[%d]/span[%d]'%(i,j))
                    if dateIfo.text == monthDate:
                        dateIfo.click()
                        break
                break

    @router('inttrip')
    def inttrip(self):
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('出发地')
        self.driver.click('上海')
        self.driver.click('目的地')
        self.driver.click('非中国大陆(国际/港澳台)')
        self.driver.click('香港')
        self.driver.click('出发日期')
        self.getdata()
        self.driver.click('去预订')
        self.driver.wait_element_disapper('正在加载中...')
        self.driver.js_click('/html/body/div[1]/div/div[2]/div/div[1]/div[2]/article/div/ul/ul/li[1]')
        self.driver.click('预订')
        self.driver.wait_element_disapper('正在获取最低价')
        self.driver.wait(2.5)
        self.driver.click('提交')
        self.driver.wait(0.5)
        self.driver.wait_element_disapper('加载中...')
        self.driver.click('#container > div > div.nav-btmbar-container > div.right')
        self.driver.wait(1)

    @router('doubleinttrip')
    def doubleinttrip(self):
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('出发地')
        self.driver.click('上海')
        self.driver.click('目的地')
        self.driver.click('非中国大陆(国际/港澳台)')
        self.driver.click('香港')
        self.driver.click('出发日期')
        self.getdata()
        self.driver.click('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[5]/a/div[2]/div[1]')
        self.driver.click('外部/支持人员')
        self.driver.click('测试')
        self.driver.wait(1)
        self.driver.click('/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[5]/div[1]/button')
        self.driver.wait(2)
        self.driver.click('/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]')
        self.driver.wait_element_disapper('正在加载中...')
        self.driver.js_click('/html/body/div[1]/div/div[2]/div/div[1]/div[2]/article/div/ul/ul/li[1]')
        self.driver.click('预订')
        self.driver.wait_element_disapper('正在获取最低价')
        self.driver.wait(2.5)
        self.driver.click('提交')
        self.driver.wait(0.5)
        self.driver.wait_element_disapper('加载中...')
        self.driver.click('#container > div > div.nav-btmbar-container > div.right')
        self.driver.wait(1)
