import sys
import pymysql
import time
import datetime


db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,database='senge')
if db.ping() == False:
    print("connect database fail")
    sys.exit()
cursor = db.cursor()




def UpdateLogin(account,date,count):

    sql = 'INSERT INTO login(account,date,count,updateTime)values(%s,%s,%s,now()) ON DUPLICATE KEY UPDATE date = %s,count=%s, updateTime = now();'
    sql_record = 'INSERT INTO record(account,loginTime) values(%s,now());'
   # params = ('f', str(new_time.date()), str(1), str(new_time.date()), str(10))
    params = (account, date, count, date, count)
    params_record = (account)
    try:
        cursor.execute(sql,params)
        cursor.execute(sql_record,params_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print("error",e)

def GetLoginCount(account):
 try:
    sql = 'SELECT date,count FROM login where account=%s'
    cursor.execute(sql,account)
    row = cursor.fetchone()
    return row
 except Exception as e:
    print("error",e)
 

def WriteDate(date):
 try:
    sql = 'INSERT INTO date(date,updateTime) values(%s,now());'
    cursor.execute(sql,str(date))
    db.commit()
 except Exception as e:
    print("error",e)
