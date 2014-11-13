import psycopg2

print("Connecting...")
# Connect to an existing database
conn = psycopg2.connect(database="Project", user="Project", host="162.243.19.108")
print("Connected")

# Open a cursor to perform database operations
cur = conn.cursor()
run = True

while run:
        print("OPTIONS:\n1. INSERT INTO\n2. UPDATE\n3. DELETE\n4. SELECT ALL\n5. EXIT")
        
        option = input("Choose an option: ")
        
        if (str(option) == '1'):
            
                
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (2, 1, 35);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (18, 1, 20);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (5, 1, 15);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (12, 2, 20);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (42, 2, 20);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (101, 2, 20);"
                cur.execute(sql)                
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (9, 3, 20);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (17, 3, 20);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (45, 3, 20);"
                cur.execute(sql)                
                print("\nINSERTED")        
            
        elif (str(option) == '2'):
                sql = "UPDATE airplanes SET tail_number = 1802 WHERE tail_number = 1745;"
                cur.execute(sql)
                print("\nUPDATED")    
            
        elif (str(option) == '3'):
                sql = "DELETE FROM airplanes WHERE type_code = 1;"
                cur.execute(sql)
                print("\nDELETED")
        
        elif (str(option) == '4'):
                sql = "SELECT * FROM airplanes;"
                cur.execute(sql)
                print(cur.fetchall())
                
        elif (str(option) == '5'):
                run = False
        
        
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