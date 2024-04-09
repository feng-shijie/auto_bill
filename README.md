# auto_bill
* Automatic utility bill based on python3 and qt

## python3
* python3 执行文件

### 模块安装
pip3 install beautifulsoup4

### 初始化
* python3 main.py back   进入后台
1. 添加admin用户 <发送者>
2. 添加普通用户 <接收者>
3. 添加水费，电费的url链接 <必须有一个>
4. 添加当前缴费人员 <如果没有会自动把第一位的普通用户添加为缴费用户>
5. 全部添加完毕后退出
6. 后台运行    nohup python3 main.py &

### 文件详解
#### bill_class.py
* 所有自定义结构体类型

#### create.py
* 创建sqlite3数据库 <有以下几个表>
1. admin       管理员email
2. email_user  所有用户的email
3. help        所有帮助命令
4. now         当前缴费人员
5. url         链接

#### main.py
1. python3 main.py back 进入后台
2. python3 main.py 启动
   1. 检查当前缴费用户情况，如不存在，自动修改为第一个普通用户，普通用户不存在则报错
   2. 开始检查余额
      1. 大于早上9点小于晚上18点每2小时检查一次，其它时间30分钟检查一次
      2. 当其中一项费用低于最小值(10，可自行修改)，发送email通知缴费人员并每5分钟检查一次
      3. 当充值成功，就提示所有人，并自动轮询缴费人员

#### interactive.py
* 后台交互模块

#### bill.py
1. 余额不足发送至当前缴费人员
2. 充值成功发送至全体人员

#### tools.py
* 用于写log 该类采用单例模式

---
<br>

## lib
* c/c++ 动态库<用于写log>， tools.py是调用它的示例  <只是熟悉一下这种用法>

---
<br>

## qt
* 可视化窗口 <基于数据库的交互>