
import pymysql,datetime
t=datetime.datetime.now()
e=datetime.datetime.now()
u='abhinay'
c='comamand'
cnx = pymysql.connect(host='localhost',user='root',password='Pamidi7997',db='mydatabase')
cursor = cnx.cursor()

i='hbfvdfvidpuvhpdi'
cursor.execute("INSERT INTO  user_execution_session_log(username,command,starttime,endtime,exe_session_id)VALUES (%s,%s,%s,%s,%s)",(u,c,t,e,i))
  # # for i in cursor.fetchall():
  # #     print(i)
  # # Make sure data is committed to the database
  # data = {
  #   'username': emp_no,
  #   'command': 50000,
  #   'starttime': tomorrow,
  #   'endtime': date(9999, 1, 1),
  #   'exe_session_id':
  # }
  # cursor.execute("insert into students(sid,sname,sage) values(%s,%s,%s)",(110,'phani',22))
  # for i in cursor.fetchall():
  #     print(i)

cnx.commit()

cursor.close()
cnx.close()