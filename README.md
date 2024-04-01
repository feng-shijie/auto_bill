# auto_bill
Automatic utility bill based on python3 and qt

## 模块安装
pip3 install beautifulsoup4

## 初始化
python3 thred.py back   进入交互线程
添加admin用户<发送者>
添加普通用户<接收者>
添加当前缴费人员
添加水费，电费的url链接
全部添加完毕后退出
后台运行    nohup python3 thread.py &

## 文件详解
### bill_class.py
所有自定义结构体类型

### create.py
创建sqlite3数据库
admin       管理员email
email_user  所有用户的email
help        所有帮助命令
now         当前缴费人员
url         地址

### create.sh   <以弃用>
数据保存到文件

### main.py
1. back线程
   用户交互线程，
2. time线程
   检查余额
   工作日和非工作日 <按照耗费来判断， 工作日不高于5>
   工作日 9-18 每隔3小时检查余额
   非工作日     每隔1小时检查余额

### email.py
    从数据库中获取数据， 发送email
    email发送情况
    余额不足发送至当前缴费人员
    充值成功发送至全体人员
