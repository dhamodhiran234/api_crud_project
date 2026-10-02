import mysql.connector

def conn():
    dbcon=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhamo@123#Db",
        database="uniq",
        auth_plugin="mysql_native_password"
    )
    if dbcon.is_connected():
        print("suceesss")
    return dbcon
conn()