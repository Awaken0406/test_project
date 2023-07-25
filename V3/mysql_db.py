import sys
import pymysql
from  datetime import date
from auto_fill import CAccountClass
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



def GetAccount_ita(date:date):
  try:
    sql = 'SELECT * FROM ita where  DATE(%s) <= end and state = 0'
    cursor.execute(sql,(str(date)))
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
    sql = 'SELECT * FROM deu where  DATE(%s) <= end and state = 0'
    cursor.execute(sql,(str(date)))
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

#time_date = datetime.datetime.strptime('2023-8-10', "%Y-%m-%d").date()
#data = GetAccount_ita(time_date)
#print('%s',vars(data))
