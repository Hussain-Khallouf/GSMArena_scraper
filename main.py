from Phone import Phone
import sqlite3 

con = sqlite3.connect('phony.db')

# mobile = Phone('SAMSONG','A3', 'About 150 EUR','2013, November.','4.5 inches'
#     ,'4GB 1GB RAM', 'Android 4.1.2')
cursor = con.cursor()
# command1= "CREATE TABLE phones(phone_id INTEGER PRIMARY KEY, name TEXT)"
# cursor.execute(command1)

cursor.execute("INSERT INTO phones VALUES(1,'A3')")

print(cursor.execute('select * from phones').fetchall())