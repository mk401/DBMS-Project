import psycopg2

print("Connecting...")
# Connect to an existing database
conn = psycopg2.connect(database="Project", user="Project", host="162.243.19.108")
print("Connected")

# Open a cursor to perform database operations
cur = conn.cursor()

print("OPTIONS:\n1. INSERT INTO\n2. UPDATE\n3. DELETE\n4. SELECT ALL\n")

option = input("Choose an option: ")

if (str(option) == '1'):
    #sid = input("Enter sid to add: ")
        #sid = int(sid)
        #age = input("Enter age to add: ")
        #age = int(age)
        #name = input("Enter name to add: ")
        #name = str(name)
        
        #print("Adding...")
        sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (1745, 1, 20);"
        cur.execute(sql)
        print("\nINSERTED")
        #data = (sid, age, name, )
        #cur.execute(sql, data)
        #print("Added")    
    #table = input("Enter table to update: ")
    #oldvalue = input("Enter value to be updated: ")
    #newvalue = input("Enter new value: ")
    #where = input("Enter where value should be updated: ")
    #whereis = input("Enter where condition part 2: ")
    
    
    
elif (str(option) == '2'):
        sql = "UPDATE airplanes SET tail_number = 1802 WHERE tail_number = 1745;"
        cur.execute(sql)
        print("\nUPDATED")    
    
elif (str(option) == '3'):
        sql = "DELETE FROM airplanes WHERE tail_number = 1802;"
        cur.execute(sql)
        print("\nDELETED")

elif (str(option) == '4'):
        sql = "SELECT * FROM airplanes;"
        cur.execute(sql)
        print(cur.fetchall())
        
elif (str(option) == '5'):
        break


else:
        print("Invalid option choice!")

# Query the database and obtain data as Python objects
#cur.execute("select * from people;")
#print(cur.fetchall())

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()