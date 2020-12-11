# k=dict()
# k['one']=1
# k['two']=2
# print(k['one'])

import pymysql

#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="gapps" )
cursor = connection.cursor()
# some other statements  with the help of cursor
c=7879
a='Jazz'
# insert1 = "INSERT INTO Artists(NAME, TRACK) VALUES(%s, %s)"
# val=(c,a)
cursor.execute("INSERT INTO Artists(NAME, TRACK) VALUES(%s, %s)",(c,a))
connection.commit()
connection.close()