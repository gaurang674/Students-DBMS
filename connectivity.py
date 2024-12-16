import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="IluAbcde.1",
    database="dbms6"
)

mycursor = mydb.cursor()

rollno = int(input("Enter Rollno: "))
name =input("Enter Name: ")
marks = int(input("Enter Marks: "))
data = (rollno,name,marks)

mycursor.execute("Insert into stud(rollno,name,marks) values (%s,%s,%s)",data)
mydb.commit()

mycursor.execute("Select * from stud")
for i in mycursor:
    print(i)