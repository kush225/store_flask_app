import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query= 'Select * from user'
result = cursor.execute(query)

print("User List:")
for i in result:
    print(i)

print()
print("Items List:")
query2= 'Select * from item'
result2 = cursor.execute(query2)
for i in result2:
    print(i)
