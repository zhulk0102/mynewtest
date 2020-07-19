# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/8 15:54
@Auth ： zhulk

"""
from common.mainTest import mainTest,router

class formPage(mainTest):
    @router('totrip')
    def totrip(self):
        self.driver.switch_to_frame("#main")
        self.driver.click('填写单据')
        self.driver.switch_to_frame("#formTree")
        self.driver.click('201-差旅申请单-行程明细合并')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#formContent')
        self.driver.click('#addtravelbuttonid')
        self.driver.wait(2)

    @router('submit')
    def submit(self):
        self.driver.switch_to_frame('#main')
        self.driver.switch_to_frame('#formContent')
        self.driver.click('/html/body/div[5]/div[1]/div/table/tbody/tr[10]/td[10]/input[1]')
        self.driver.click('/html/body/div[5]/div[4]/table/tbody/tr[2]/td/div/div/div/div/ul/div/li[2]/div/a/span')
        self.driver.click('/html/body/div[5]/div[1]/div/table/tbody/tr[11]/td[1]/img[2]')
        self.data_pool['number'] = self.driver.find_elements('/html/body/div[5]/div[1]/div/table/tbody/tr[2]/td[15]').get_attribute('title')
        self.driver.click('//*[@id="flow_submit"]')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame("#jd_iframe")
        self.driver.click('#btnSubmit')
        self.driver.wait(1)

    @router('assgin')
    def assgin(self):
        self.driver.click('共享中心')
        self.driver.click('TD任务管理')
        self.driver.switch_to_frame("#main")
        self.driver.switch_to_frame("/html/body/div[3]/div[1]/iframe")
        self.driver.js_send_keys('/html/body/table[1]/tbody/tr[1]/td[2]/input',self.data_pool['number'])
        self.driver.wait(1.5)
        self.driver.click('/html/body/table[1]/tbody/tr[3]/td/input[1]')
        self.driver.wait(1.5)
        self.driver.click('/html/body/table[2]/tbody/tr/td/div/div[1]/div[2]/table/tbody/tr/td[1]/input[1]')
        self.driver.wait(1.5)
        self.driver.click('/html/body/table[1]/tbody/tr[3]/td/input[3]')
        self.driver.wait(2)
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('#closeBtn')
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('/html/body/div[3]/table/tbody/tr[2]/td/ul/div/div/div/ul/li/ul/li/ul/li[1]/div/a/span')
        self.driver.wait(0.5)

    @router('tdflow')
    def tdflow(self):
        self.driver.click('商旅商城')
        self.driver.click('我的TD台-国际')
        self.driver.switch_to_frame("#main")
        self.driver.js_send_keys('/html/body/table/tbody/tr[1]/td[2]/input', self.data_pool['number'])
        self.driver.wait(1)
        self.driver.click('/html/body/table/tbody/tr[3]/td/input[2]')
        self.driver.click('询价')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('/html/body/div[3]/div[2]/table[1]/tbody/tr[3]/td/input')
        self.driver.wait(1)
        self.driver.click('/html/body/div[3]/div[3]/input[1]')
        self.driver.wait(2)

    @router('tdcomfirm_flow')
    def tdcomfirm_flow(self):
        self.driver.click('商旅商城')
        self.driver.click('我的TD台-国际')
        self.driver.switch_to_frame("#main")
        self.driver.js_send_keys('/html/body/table/tbody/tr[1]/td[2]/input', self.data_pool['number'])
        self.driver.wait(1)
        self.driver.click('/html/body/table/tbody/tr[3]/td/input[2]')
        self.driver.wait(1)
        self.driver.click('/html/body/table/tbody/tr[4]/td/div/div[1]/div[2]/table/tbody/tr/td[18]/a/p')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.switch_to_frame("/html/body/div[3]/div[1]/iframe")
        self.driver.click('/html/body/div[3]/div[3]/table/tbody/tr[1]/td[19]/input')
        self.driver.click('/html/body/div[3]/div[1]/p[4]/input')
        self.driver.click('/html/body/div[6]/table/tbody/tr/td/input[2]')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame("#main")
        self.driver.click('/html/body/div[4]/table/tbody/tr/td[3]/input')
        self.driver.switch_to_parent_frame()
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('#btnSubmit')
        self.driver.switch_to_frame('#jd_iframe')
        self.driver.click('/html/body/table/tbody/tr[2]/td/input[1]')
        self.driver.wait(1)