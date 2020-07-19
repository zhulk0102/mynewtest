# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/14 17:09
@Auth ： zhulk

"""
from common.mainTest import mainTest,router

class adminPage(mainTest):
    @router('admintd')
    def admintd(self):
        self.driver.click('行程管理')
        self.driver.click('/html/body/div/div/div[1]/div[1]/div/ul/div[1]/li/ul/a/li')
        self.driver.wait(2)
        self.driver.switch_to_frame('/html/body/div/div/div[2]/section/div/iframe')
        self.driver.wait_element_disapper('处理中...')
        self.driver.send_keys('/html/body/div/div[2]/div/div[1]/input[3]', self.data_pool['number'])
        self.driver.click('/html/body/div/div[2]/div/div[1]/button')
        self.driver.wait(2.5)
        self.driver.click('/html/body/div/div[2]/div/div[3]/div/table/tbody/tr[2]/td[6]/input[1]')
        self.driver.switch_to_frame('/html/body/div[3]/div[2]/iframe')
        self.driver.click('/html/body/div/div[3]/div[2]/ol[1]/li[1]/div/table/tbody/tr[2]/td[2]/div/select/option[2]')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[1]/li[1]/div/table/tbody/tr[2]/td[9]/div/input','B')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[3]/div[2]/div[1]/input','2000')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[3]/div[2]/div[2]/input','50')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[3]/div[2]/div[3]/input','20')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[4]/div[2]','201911111111')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[5]/div[2]/textarea','退改规则')
        self.driver.send_keys('/html/body/div/div[3]/div[2]/ol[2]/li[6]/div[2]/textarea','签证')
        self.driver.click('提交报价')
        self.driver.wait(5)

    @router('intticket')
    def int_ticket(self):
        self.driver.click('国际机票')
        self.driver.click('正常订单')
        self.driver.wait(8)
        self.driver.send_keys('/html/body/div/div/div[2]/section/div/div/div[2]/div[1]/div/form[1]/div[3]/div/div/input',self.data_pool['number'])
        self.driver.click('/html/body/div/div/div[2]/section/div/div/div[2]/div[1]/div/form[2]/div[3]/div/button/span')
        self.driver.click('/html/body/div/div/div[2]/section/div/div/div[2]/div[1]/div/div[1]/div/div[3]/table/tbody/tr/td[13]/div/button[1]/span')
        self.driver.click('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[2]/div/div[2]/form/div[2]/div/div/div[1]/input')
        self.driver.click('/html/body/div[3]/div[1]/div[1]/ul/li[1]')
        self.driver.click('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[2]/div/div[2]/form/div[3]/div/div/div[1]/input')
        self.driver.click('/html/body/div[4]/div[1]/div[1]/ul/li[1]')
        self.driver.send_keys('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[2]/div/div[4]/form/div[2]/div/div/input','166')
        self.driver.send_keys('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[2]/div/div[6]/div/form/div[1]/div/div/input','123-55555')
        self.driver.click('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[2]/div/div[6]/div/form/div[2]/div/div/div/button/span')
        self.driver.upload_file(r'C:\Users\woshi\Desktop\123.pdf')
        self.driver.wait(4)
        self.driver.click('/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div/div[4]/div/div[3]/div/button[1]')
        self.driver.wait(5)
