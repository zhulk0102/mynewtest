# -*- coding: utf-8 -*-
"""
@Time ： 2020/1/3 11:56
@Auth ： zhulk

"""
# 获取流程列表的属性
flow_list_locals = locals()

def get_flow_list_locals():
    return flow_list_locals

# 参数
login = ['su1', '1']
logintd=['y2','1']
adminlogin=['guangda','123456']

# 流程
submit_flow = {'login': login,'totrip':'' ,'inttrip':'','submit':''}
assgin_flow = {'login': login,'assgin':''}
td_plow = {'login':logintd,'tdflow':''}
admin_flow = {'adminlogin':adminlogin,'admintd':''}
tdcomfirm_flow = {'login':logintd,'tdcomfirm_flow':''}
intticket_flow ={'adminlogin':adminlogin,'intticket':''}
submitdouble_flow ={'login': login,'totrip':'','doubleinttrip':''}
# 组装流程（测试用例）
flow = [
submit_flow,
assgin_flow,
td_plow,
admin_flow,
tdcomfirm_flow,
intticket_flow
# submitdouble_flow
]

