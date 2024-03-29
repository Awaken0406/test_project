import sys
import pymysql
from  datetime import date
from auto_fill import CAccountClass
import datetime


class CProxyData:
  def __init__(self):
    self.secret_id  = ''
    self.signature  = ''
    self.proxy_name = ''
    self.proxy_password = '' 



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



def GetAccount_ita(date:date):
  try:
    sql = 'SELECT * FROM ita where DATE(%s) >= start and DATE(%s) <= end and state = 0'
    cursor.execute(sql,( str(date),str(date)))
    rows = cursor.fetchall()
    for row in rows:
        data = CAccountClass()
        data.sexual  = row[0]
        data.name  = row[1]
        data.sex = row[2]
        data.phone = row[3]
        data.mail = row[4]
        data.passport = row[5]
        data.start = row[6]
        data.end = row[7]
        data.birth = row[8]
        data.effective = row[9]

        sql = 'UPDATE  ita SET state = 1 WHERE passport = %s'
        cursor.execute(sql, (data.passport))
        db.commit()
        return data
    return None
  except Exception as e:
    print("error",e)


def GetAccount_deu(date:date):
  try:
    sql = 'SELECT * FROM deu where DATE(%s) >= start and DATE(%s) <= end and state = 0'
    cursor.execute(sql,( str(date),str(date)))
    rows = cursor.fetchall()
    for row in rows:
        data = CAccountClass()
        data.sexual  = row[0]
        data.name  = row[1]
        data.sex = row[2]
        data.phone = row[3]
        data.mail = row[4]
        data.passport = row[5]
        data.start = row[6]
        data.end = row[7]
        data.birth = row[8]
        data.effective = row[9]

        sql = 'UPDATE  deu SET state = 1 WHERE passport = %s'
        cursor.execute(sql, (data.passport))
        db.commit()
        return data
    return None
  except Exception as e:
    print("error",e)




def GetProxyData():
    data = CProxyData()
    sql = 'SELECT * FROM proxy'
    cursor.execute(sql)
    row = cursor.fetchone()
    data.secret_id  = row[0]
    data.signature  = row[1]
    data.proxy_name = row[2]
    data.proxy_password = row[3] 
   
    return data 


data = GetProxyData()
