#/*****************线程函数*****************/
#!/usr/bin/python3
# -*- coding: utf-8 -*-  

from datetime import datetime
import os
import sys
import time
import threading

import bill
import create
import interactive

from bill_class import DB
from bill_class import Email
from bill_class import Index

# #/*****************检查费用余额*****************/
def check_balance():
    while True:
        _res = os.system("ping -c 1 www.baidu.com")
        if _res == 0:   break
        print("网络错误")
        time.sleep(60)

# 修改一下，只有一个url也可以
    bill.get_balance()
    if Email.m_now_water == None and Email.m_now_electricity == None:
        print("get water and electricity bill balance fail, please check url")
        return

    i_now_hour = datetime.now().hour
    #判断是否是白天 白天消耗少，刷新时间间隔缩长
    if  i_now_hour > 9 or i_now_hour < 18:   Email.m_timeout = 2  * 60 * 60
    else:                                    Email.m_timeout = 30 * 60

    #当余额不足时提示充值
    if ((Email.m_balance_water       == None and Email.m_now_water       < Email.m_min_tip) or 
        (Email.m_balance_electricity == None and Email.m_now_electricity < Email.m_min_tip)):
        Email.m_bill_status         = False
        Email.m_balance_water       = Email.m_now_water
        Email.m_balance_electricity = Email.m_now_electricity
        bill.send_email()
       #已充值  全部重置
    elif ((Email.m_balance_water       != None and Email.m_now_water       > Email.m_min_tip) or 
          (Email.m_balance_electricity != None and Email.m_now_electricity > Email.m_min_tip)):
        Email.m_bill_status         = True
        bill.send_email()
        Email.m_balance_water       = None
        Email.m_balance_electricity = None

    #当通知缴费后,5分钟获取一次余额,
    if Email.m_bill_status == False:    Email.m_timeout = 5 * 60

def update_now_user():
    sql_res = DB._db.execute(f"SELECT * FROM {DB.table_user}")
    l_user = list(sql_res)
    user_idx = 0
    for user in l_user:
        user_idx += 1
        if Email.m_now_user[Index._EMAIL] == user[Index._EMAIL]: break
    if user_idx >= len(l_user): Email.m_now_user = l_user[0]
    else:                       Email.m_now_user = l_user[user_idx]
    DB._db.execute(f"DELETE FROM {DB.table_now}")
    DB._db.execute(f"INSERT INTO {DB.table_now} VALUES('{Email.m_now_user[Index._EMAIL]}', '{Email.m_now_user[Index._NAME]}');")
    DB.m_db.commit()
    print(f"now user to update: email: {Email.m_now_user[Index._EMAIL]}, name: {Email.m_now_user[Index._NAME]}")

def add_now_user():
    sql_res = DB._db.execute(f"SELECT * FROM {DB.table_user}")
    l_user = list(sql_res)
    if len(l_user) == 0:
        print("没有用户, 无法添加当前缴费用户。请使用add命令添加用户")
        exit()
    Email.m_now_user = l_user[0]
    DB._db.execute(f"INSERT INTO {DB.table_now} VALUES('{Email.m_now_user[Index._EMAIL]}','{Email.m_now_user[Index._NAME]}');")
    DB.m_db.commit()
    print("now user is null, Add the first user as the recharge user.")
    print(f"email: {Email.m_now_user[Index._EMAIL]}, name: {Email.m_now_user[Index._NAME]}")

def check_now_user():
    res = DB._db.execute("SELECT * FROM now")
    l_now = list(res)
    if len(l_now):
        Email.m_now_user = l_now[0]
        if Email.m_bill_status:     update_now_user()
    else:   add_now_user()

#/*****************时间线程*****************/
def time_thread(_temp):
    while True:
        check_now_user()
        check_balance()
        time.sleep(Email.m_timeout)

if __name__ == '__main__':
    create.create_db()
    DB.init()

    if len(sys.argv) > 2:
        print("格式错误，进入交互线程 python3 thread.py back")
        sys.exit()
    elif len(sys.argv) == 2:
        if not sys.argv[1] == "back":
            print("格式错误，最后一个参数应为 back")
            sys.exit()
        t_thread = threading.Thread(target = interactive.init(), args = (0,))
    else:   t_thread = threading.Thread(target = time_thread, args = (0,))
    t_thread.start()
    t_thread.join()