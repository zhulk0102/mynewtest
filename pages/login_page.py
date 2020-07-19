# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/3 16:50
@Auth ： zhulk

"""

from common.mainTest import mainTest,router

class loginPage(mainTest):
    @router('login')
    def login(self,username,password):
        self.driver.send_keys('#usernameInput',username)
        self.driver.send_keys('#passwordInput', password)
        self.driver.click('#submitButton')

    @router('adminlogin')
    def adminlogin(self,username,password):
        self.driver.get('http://test.td.51ykb.com')
        self.driver.send_keys('/html/body/div/div/form/div/div[2]/div/div/input',username)
        self.driver.send_keys('/html/body/div/div/form/div/div[3]/div/div/input',password)
        self.driver.click('登录')
        self.driver.wait(1)
