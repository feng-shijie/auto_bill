#!/usr/bin/python3
# -*- coding: utf-8 -*-  

from itertools import chain

from bill_class import DB
from bill_class import Cmd
from bill_class import Index


#/*****************交互线程*****************/
def check_email(_table, _email):
    _cmd = f"SELECT * FROM {_table} WHERE {DB.type_email} = '{_email}';"
    _res = DB._db.execute(_cmd)
    if len(list(_res)) == 0:
        return False
    return True

def result(_table, _email):
    DB.m_db.commit()
    _cmd = f"SELECT * FROM {_table} WHERE {DB.type_email} = '{_email}';"
    _res = DB._db.execute(_cmd)

    print(list(chain.from_iterable(list(_res))))

#false 为普通用户， true 为管理员用户
def add_user(_list, _is_special):
    if _is_special == False:
        if check_email(DB.table_user,_list[1]):
            print("用户已存在, 请使用edit命令来修改用户")
            return
        _cmd = f"INSERT INTO {DB.table_user} VALUES('{_list[1]}', '{_list[2]}');"
        DB._db.execute(_cmd)
        result(DB.table_user, _list[1])
    else:
        _result = DB._db.execute(f"SELECT (email) FROM {DB.table_admin};")
        _res    = list(chain.from_iterable(list(_result)))
        if len(_res) == 4:
            print("admin用户已存在, 请使用eadmin命令来修改admin用户")
            return
        else:
            _cmd = f"DELETE FROM {DB.table_admin};"
            DB._db.execute(_cmd)
            _cmd = f"INSERT INTO {DB.table_admin} VALUES('{_list[1]}', '{_list[2]}', '{_list[3]}', '{_list[4]}');"
            DB._db.execute(_cmd)
            result(DB.table_admin, _list[1])
            if not check_email(DB.table_user,_list[1]):
                print("添加admin用户到用户列表")
                add_user(_list, False)

#判断当前用户是否为用户成员，如不是请先添加
def setnow(_list):
    _result = DB._db.execute(f"SELECT * FROM {DB.table_user} WHERE {DB.type_email} = '{_list[1]}';")
    _res    = list(chain.from_iterable(list(_result)))

    if len(_res) == 0:
        print("请先在用户列表中添加用户")
        return

    DB._db.execute(f"INSERT INTO {DB.table_now} VALUES('{_res[Index._EMAIL]}', '{_res[Index._NAME]}');")
    DB.m_db.commit()
    print(f"now = {_res} 设置成功")

def seturl(_list):
    if not (_list[1] == "water" or _list[1] == "electricity"):
        print("name 错误 水费为:water 电费为:electricity")
        return
    DB._db.execute(f"UPDATE {DB.table_url} SET {DB.type_url} = '{_list[2]}' WHERE {DB.type_name} = '{_list[1]}';")
    DB.m_db.commit()
    print(f"name = {_list[1]} url = {_list[2]} 修改成功")


#判断当前删除的用户是否为缴费用户，如果是询问是否删除
def remove_user(_list):
    if not check_email(DB.table_user,_list[1]):     print("用户不存在, 请使用add命令来添加用户")
    else:
        sql_res = DB._db.execute(f"SELECT * FROM {DB.table_now} WHERE {DB.type_email} = '{_list[1]}';")
        now_user = list(sql_res)
        if len(now_user):
            print("要删除的用户为缴费用户，如删除将自动轮询到下一位用户")
            while True:
                in_res = input("删除请输入y, 不删除请输入n:")
                in_res = in_res.strip()
                in_res = in_res.lower()
                if in_res == 'y':
                    sql_res = DB._db.execute(f"SELECT * FROM {DB.table_user}")
                    l_user = list(sql_res)
                    idx = 0
                    for user_idx in range(0, len(l_user)):
                        if now_user[0][Index._EMAIL] == l_user[user_idx][Index._EMAIL]: idx = user_idx + 1
                    if idx >= len(l_user):  now_user = l_user[0]
                    else:                   now_user = l_user[idx]
                    DB._db.execute(f"DELETE FROM {DB.table_now};")
                    DB._db.execute(f"INSERT INTO {DB.table_now} VALUES('{now_user[Index._EMAIL]}', '{now_user[Index._NAME]}');")
                    print(f"now user to update: {now_user}")
                    break
                elif in_res == 'n':    return
                else:   print("输入有误")

        result(DB.table_user, _list[1])
        _cmd = f"DELETE FROM {DB.table_user} WHERE {DB.type_email} = '{_list[1]}';"         
        DB._db.execute(_cmd)
        DB.m_db.commit()
        if check_email(DB.table_user,_list[1]): print("DELETE error")
        else:                                   print("用户已删除")

#false为普通用户，true为admin用户
#判断当前修改的用户是否为缴费用户，如果是更新now表
def edit_user(_list, _is_special):
    if not _is_special:
        if not check_email(DB.table_user,_list[1]):
            print("用户不存在, 请使用add命令来添加用户")
            return
        _cmd = "UPDATE %s SET %s = '%s', %s = '%s' WHERE %s = '%s';" \
        %(DB.table_user, DB.type_email, _list[1], DB.type_name, _list[2], DB.type_email, _list[1])
        DB._db.execute(_cmd)
        res = DB._db.execute(f"SELECT * FROM {DB.table_now} WHERE {DB.type_email} = '{_list[1]}';")
        if len(list(res)):
            DB._db.execute(f"UPDATE {DB.table_now} SET {DB.type_email} = '{_list[1]}', {DB.type_name} = '{_list[2]}';")
        result(DB.table_user, _list[1])
    else:
        if not check_email(DB.table_user,_list[1]):
            print("admin用户不存在, 请使用admin命令来添加admin用户")
            return
        _cmd = "UPDATE %s SET %s = '%s', %s = '%s', %s = '%s', %s = '%s' WHERE %s = '%s';" \
        %(DB.table_admin, DB.type_email, _list[1], DB.type_name, _list[2], DB.type_server, _list[3], DB.type_password, _list[4], DB.type_email, _list[1])
        
        DB._db.execute(_cmd)
        result(DB.table_admin, _list[1])
    DB.m_db.commit()
    print("用户已修改")


def select_user(_list):
    _cmd = f"SELECT * FROM {DB.table_user} WHERE {DB.type_email} = '{_list[1]}';" 
    _result = DB._db.execute(_cmd)
    _res = list(chain.from_iterable(list(_result)))     #把多维list解为一层list
    if bool(_res):  print(" email = ", _res[Index._EMAIL], " name = ", _res[Index._NAME])
    else:           print("用户不存在")

def getall_user():
    _cmd = f"SELECT * FROM {DB.table_user};"
    _result = DB._db.execute(_cmd)

    l_user = list(_result)
    if len(l_user):
        for _val in l_user:
            print(" email = ", _val[Index._EMAIL], " name = ", _val[Index._NAME])
    else:   print("没有用户, 请使用add命令添加用户")

def getadmin_user():
    _cmd = f"SELECT * FROM {DB.table_admin};"
    _result = DB._db.execute(_cmd)
    _res = list(chain.from_iterable(list(_result)))
    if bool(_res):
        pw_res = input("请输入admin用户的email密码：")
        if _res[Index._PASSWORD] == pw_res.strip():
            print("email = ", _res[0], " name = ", _res[1], " server = ", _res[2], " password = ", _res[3])
        else:   print("密码错误")
    else:       print("没有admin用户, 请使用add命令添加admin用户")

def get_balance():
    print("%s")
    print("%s")

def quit():
    DB._db.close()
    DB.m_db.close()
    exit()

def help(_dic):
    _result = DB._db.execute("SELECT * FROM help;")
    _mat = "{0:<10}\t{1:<35}\t{2:<10}"
    print(_mat.format("命令", "参数", "说明"))
    i = 0
    for _str in _result:
        _dic[_str[0]] = i   #ID key 字典 id与命令的映射关系
        i+=1
        print(_mat.format(_str[0], _str[1], _str[2]))
        # print("{0:<10}\t{1:<10}\t{2:<10}" .format(_str[0], _str[1], _str[2]))

def execute_cmd(_dic, _list):
    if len(_list[0]) == 0: return

    _val = _dic.get(_list[0])
    if _val == None:
        print("没有该命令, 请重试")
        return
    
    _cmd    = f"SELECT (param) FROM {DB.table_help} WHERE cmd = '{_list[0]}';"
    _result = DB._db.execute(_cmd)
    _res    = list(chain.from_iterable(list(_result)))
    if len(str(_res[0]).strip()) == 0:    param_len = 0
    else:                                 param_len = len(str(_res[0]).split('+'))

    if len(_list) - 1 != param_len:
        print("命令参数数量不正确")
        return

    if   _val == Cmd._ADD:      add_user(_list, False)
    elif _val == Cmd._ADMIN:    add_user(_list, True )
    elif _val == Cmd._SETNOW:   setnow(_list)
    elif _val == Cmd._SETURL:   seturl(_list)
    elif _val == Cmd._REMOVE:   remove_user(_list)
    elif _val == Cmd._EDIT:     edit_user(_list, False)
    elif _val == Cmd._EADMIN:   edit_user(_list, True )
    elif _val == Cmd._SELECT:   select_user(_list)
    elif _val == Cmd._GETALL:   getall_user()
    elif _val == Cmd._GETADMIN: getadmin_user()
    elif _val == Cmd._GETBILL:  get_balance()
    elif _val == Cmd._QUIT:     quit()
    elif _val == Cmd._HELP:     help()

def init():
    _dic = {}
    help(_dic)
    
    while True:
        _cmd = input("请输入：")
        _cmd = _cmd.strip()
        # _case_list.append(_cmd.split(' '))    #append是把返回的列表添加到列表里面，所以它的type是list[list[]] 而不是 list["str"]
        _case_list = _cmd.split(' ')
        execute_cmd(_dic, _case_list)
        _case_list.clear()
