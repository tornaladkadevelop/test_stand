import pymysql
#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="mkv64ftj",database="simple_database" )
cursor = connection.cursor()

# queries for retrievint all rows
retrive = 'SELECT * FROM simple_database.maker ORDER BY id_maker;'
#executing the quires
cursor.execute(retrive)
rows = cursor.fetchall()
for row in rows: print(row)
#commiting the connection then closing it. connection.commit()




# some other statements with the help of cursor
connection.close()
