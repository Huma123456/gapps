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
# insert1 = "INSERT INTO one(NAME, TRACK) VALUES(%s, %s)"
# val=(a,c)
# insert1 = "INSERT INTO two(name, number) VALUES(%s, %s)"
# val=("SELECT NAME FROM one WHERE TRACK ='%s'" ,c)
# cursor.execute("insert1,val")
# cursor.execute("INSERT INTO two(NAME, number) VALUES(%s, %s)",("select NAME from one WHERE TRACK = 'Jazz'",2))

############## select ###############
sql = "SELECT NAME FROM one WHERE TRACK ='%s'"
cursor.execute(sql % c)
for row in cursor:
    # print(row[0])
    cursor.execute("INSERT INTO two(NAME, number) VALUES(%s, %s)",(row[0],2))
connection.commit()
connection.close()