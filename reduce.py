#coding:utf-8
import pymysql
import re,requests
from bs4 import BeautifulSoup

#定义数据库连接
db= pymysql.connect(host="localhost",user="root",  
    password="root",db="yu",port=3306,charset="utf8")  
#用来伪装成浏览器访问
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}
#正则表达式匹配
pat='该域名未被注册或被隐藏'
#打开游标
cur = db.cursor()  
#新建数据表
create_sql="""
CREATE TABLE IF NOT EXISTS `cihui_data` (
  `cihui_data` varchar(100) DEFAULT NULL,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `com_flag` varchar(6) DEFAULT NULL,
  `cn_flag` varchar(6) DEFAULT NULL,
  `reason` varchar(6) DEFAULT NULL
)
"""
cur.execute(create_sql)
# 新建检查表
check_sql="""CREATE TABLE IF NOT EXISTS  `cihui_check` (
  `cihui_flag` varchar(100) DEFAULT NULL,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP
)"""

cur.execute(check_sql)
#检查第一步插入是否已经完成
check_sql_sel='select count(1) from cihui_check where cihui_flag=1'
cur.execute(check_sql_sel)
check_data = cur.fetchone()
if check_data[0] !=1:
    #因为3位数的域名基本没了，所以从四位开始
    list=['0','1','2','3','4','5','6','7','8','9']
    for a in list:
        for b in list:
            for c in list:
                for d in list:
                    sql_insert ="""insert into cihui_data(cihui_data) values('%s')""" % (a+b+c+d)
                    cur.execute(sql_insert) 
                    print(a+b+c+d)
    
    for a in list:
        for b in list:
            for c in list:
                for d in list:
                    for e in list:
                        sql_insert ="""insert into cihui_data(cihui_data) values('%s')""" % (a+b+c+d+e)
                        cur.execute(sql_insert) 
                        print(a+b+c+d+e)
    
    for a in list:
        for b in list:
            for c in list:
                for d in list:
                    for e in list:
                        for f in list:
                            sql_insert ="""insert into cihui_data(cihui_data) values('%s')""" % (a+b+c+d+e+f)
                            cur.execute(sql_insert) 
                            print(a+b+c+d+e+f)
    sql_check='insert into cihui_check(cihui_flag) values(%s)'% 1
    cur.execute(sql_check)
    db.commit()
cur.execute("SELECT cihui_data from  cihui_data where com_flag is  null")
data = cur.fetchall()

print("开始处理域名~")
for i in data:
    try:
        url='http://whois.chinaz.com/%s.com' % i[0]
        cont=requests.get(url,headers=headers)
        soup=BeautifulSoup(cont.text,'lxml')
        if re.search(pat, soup.find("div", class_="IcpMain02").text):
            sql = "UPDATE cihui_data SET com_flag =1 WHERE cihui_data = '%s'" % i[0]
            cur.execute(sql)
            db.commit()
            print(i)
        else:
            sql = "UPDATE cihui_data SET com_flag =0 WHERE cihui_data = '%s'" % i[0]
            cur.execute(sql)
            db.commit()
            print(i)
    except:
        sql = "UPDATE cihui_data SET reason ='error' WHERE cihui_data = '%s'" % i[0]
        cur.execute(sql)
        db.commit()
        print('error~')
        continue
print("完成域名处理~")
db.close()
