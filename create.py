#!/usr/bin/python3
# -*- coding: utf-8 -*-  

import sqlite3
import os
import sys
from bill_class import DB

def create_db():
    _dir = sys.path[0] + "/db"
    if not os.path.isdir(_dir):
        _cmd = "mkdir " + _dir
        os.system(_cmd)

    _dir = _dir + "/user.db"
    if os.path.exists(_dir):    return
    else:   print("create ./db/user.db!")

    m_db = sqlite3.connect(_dir)
    _db = m_db.cursor()
    _db.execute("create table now(email,name);")
    _db.execute("create table bill(name,balance);")
    _db.execute("create table url(name,url);")
    _db.execute("create table email_user(email,name);")
    _db.execute("create table help(cmd, param, explain);")
    _db.execute("create table admin(email,name,server,password);")

    # _db.execute("create table email_user(id INTEGER PRIMARY KEY,email,name);")
    # _db.execute('''
    #             CREATE TRIGGER auto_sort AFTER DELETE ON email_user
    #             BEGIN
    #                 UPDATE email_user SET id = id-1 WHERE id > OLD.id;
    #             END;''')
    # _db.execute("create table help(id INTEGER PRIMARY KEY,cmd);")

    _db.execute(f"INSERT INTO {DB.table_admin}({DB.type_server}) VALUES ('smtp.tom.com');")
    _db.execute(f"INSERT INTO {DB.table_bill}({DB.type_name}) VALUES ('water');")
    _db.execute(f"INSERT INTO {DB.table_bill}({DB.type_name}) VALUES ('electricity');")
    _db.execute(f"INSERT INTO {DB.table_url}({DB.type_name}, {DB.type_url}) VALUES ('water' ,'http://wx.tqdianbiao.com/Client/dc2edm30010040002526');")
    _db.execute(f"INSERT INTO {DB.table_url}({DB.type_name}, {DB.type_url}) VALUES ('electricity', 'http://wx.tqdianbiao.com/Client/27f69m211003334646');")

    _db.execute("INSERT INTO help VALUES('add', 'email+name', '添加用户');")
    _db.execute("INSERT INTO help VALUES('admin', 'email+name+smtp_server+password', '添加管理员<管理员只能存在一位>');")
    _db.execute("INSERT INTO help VALUES('setnow', 'email+name', '修改当前缴费者');")
    _db.execute("INSERT INTO help VALUES('seturl', 'name+url', '设置water/electricity url');")
    _db.execute("INSERT INTO help VALUES('edit', 'email+name', '修改用户');")
    _db.execute("INSERT INTO help VALUES('eadmin', 'email+name+smtp_server+password', '修改管理员');")
    _db.execute("INSERT INTO help VALUES('remove', 'email', '删除用户');")
    _db.execute("INSERT INTO help VALUES('select', 'email', '查找用户');")
    _db.execute("INSERT INTO help VALUES('getall', ' ', '获取所有用户信息');")
    _db.execute("INSERT INTO help VALUES('getadmin', ' ', '获取管理员信息');")
    _db.execute("INSERT INTO help VALUES('getbalance', ' ', '获取当前的余额');")
    _db.execute("INSERT INTO help VALUES('quit', ' ', '退出');")
    _db.execute("INSERT INTO help VALUES('help', ' ', '打印帮助信息');")

    m_db.commit()
    m_db.close()
    print("user.db Lib create success")