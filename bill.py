#! /usr/bin/python3
#-*- coding:utf-8 -*-

import re
import smtplib
import requests
from bs4 import BeautifulSoup

from bill_class import DB
from bill_class import Email

from bill_class import Index
from itertools import chain
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 


#/**********************变量*********************/
#是否开启打印
IS_PING = False

#/**********************费用余额*********************/
#获取水费电费余额
def get_balance():
	l_bill_url = DB._db.execute("SELECT * FROM url")

	for curr_info in l_bill_url:
		#获取html
		res = requests.get(str(curr_info[1]))
		res.encoding = 'utf_8'

		if IS_PING:	print("type::", type(res))

		#解析?
		bs1 = BeautifulSoup(res.text,'html.parser')

		html_all = bs1.find_all('script', type='text/javascript')

		#通过正则表达式获取当前电表费用
		balanc = re.search('"value":(.*?),', str(html_all[1].string))

		if IS_PING:	print(balanc.group())

		if str(balanc).find(':')  > 0 or str(balanc).find('.') >0:
			#只要整数		可能出现错误  https://stackoverflow.com/questions/1841565/valueerror-invalid-literal-for-int-with-base-10
			i_balance = int(str(balanc)[str(balanc).find(':') + 1 : str(balanc).rfind('.')])
			if	 str(curr_info[0]) == 'water':			Email.m_now_water 		= i_balance
			elif str(curr_info[0]) == 'electricity':	Email.m_now_electricity = i_balance

	DB._db.execute(f"UPDATE {DB.table_bill} SET {DB.type_balance} = '{Email.m_now_water}' WHERE {DB.type_name} = 'water';")
	DB._db.execute(f"UPDATE {DB.table_bill} SET {DB.type_balance} = '{Email.m_now_electricity}' WHERE {DB.type_name} = 'electricity';")
	DB.m_db.commit()

#/**********************email*********************/
#充值成功通知所有人, 每次只能通知一个人NOW不能在这里++
def email_all():
	_bill = "充值前电费余额为: "	+ str(Email.m_balance_electricity)
	_bill += "\n充值前水费余额为: " + str(Email.m_balance_water		 )
	_bill += "\n充值后电费余额为: " + str(Email.m_now_electricity	 )
	_bill += "\n充值后水费余额为: " + str(Email.m_now_water			 )

	sql_res = DB._db.execute(f"SELECT * FROM {DB.table_user}")
	l_user  = list(sql_res)
	#用于防止出错的情况，可自行核对
	if len(l_user):
		_bill += "\n所有用户:"
		mat = "{0:<5}\t{1:<5}\t{2:<5}\t{3:<5}"
		for user in l_user:	_bill += mat.format("\n用户: ", user[Index._NAME], "用户email: ", user[Index._EMAIL])
		mat = "{0:<3}\t{1:<3}"
	_bill += mat.format("\n充值用户: ", Email.m_now_user[Index._NAME])
	_bill += mat.format("\n充值用户email: ", Email.m_now_user[Index._EMAIL])
	return _bill

#提醒NOW充值费用
def email_only():
	_bill =  "电费余额为: "   + str(Email.m_now_electricity)
	_bill += "\n水费余额为: " + str(Email.m_now_water)
	_bill += "\n电费使用量大，请合理缴费\n"
	return _bill

#发送email
def send_email():
	sql_res    = DB._db.execute("SELECT * FROM admin")
	admin_info = list(chain.from_iterable(list(sql_res)))

	if len(admin_info) < 4:
		print("请补全admin邮箱账户信息")
		exit()

	sql_res 	 = DB._db.execute("SELECT * FROM email_user")
	l_email_user =  list(sql_res)	# 二维列表

	if not bool(l_email_user):
		print("用户email为空,请添加用户")
		exit()

	admin_email  = str(admin_info[0])
	admin_name   = str(admin_info[1])
	admin_server = str(admin_info[2])
	admin_pw	 = str(admin_info[3])

	#加密的有问题无法登录，可能是要smtp授权码等等，没找到
	# email_con = smtplib.SMTP_SSL(admin_server, Email.m_smtp_port)
	email_con = smtplib.SMTP(admin_server, Email.m_smtp_port)
	email_con.login(admin_email, admin_pw)

	email_msg 	= MIMEMultipart()
	email_theme = Header('水电缴费单通知', "utf-8").encode()

	email_msg['Subject'] = email_theme
	email_msg['From'] = admin_email

	if(Email.m_bill_status == None):
		print("bill status is none")
		exit()

	#需要缴费只给一个人发送email, 充值成功给所有人发丝email
	if Email.m_bill_status:	_bill_text = email_all()
	else:					_bill_text = email_only()

	_text_format = MIMEText(_bill_text, 'plain', 'utf-8')
	email_msg.attach(_text_format)

	if Email.m_bill_status:
		for e_user in l_email_user:
			email_msg['To'] = e_user[Index._EMAIL]
			email_con.sendmail(admin_email, e_user[Index._EMAIL], email_msg.as_string())
	else:
		email_msg['To'] = Email.m_now_user[Index._EMAIL]
		email_con.sendmail(admin_email, Email.m_now_user[Index._EMAIL], email_msg.as_string())

	email_con.quit()
	print("发送完毕")