import pymysql



mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"

)
cur = mydb.cursor()
