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
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (10, 1, 35);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (5, 1, 25);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (16, 2, 75);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (27, 2, 75);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (89, 2, 65);"
                cur.execute(sql)                
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (19, 3, 300);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (183, 3, 300);"
                cur.execute(sql)
                sql = "INSERT INTO airplanes (tail_number, type_code, seats) VALUES (47, 3, 290);"
                cur.execute(sql)                
                print("\nINSERTED")        
            
        elif (str(option) == '2'):
                sql = "UPDATE airplanes SET tail_number = 1802 WHERE tail_number = 1745;"
                cur.execute(sql)
                print("\nUPDATED")    
            
        elif (str(option) == '3'):
                sql = "DELETE FROM airplanes WHERE type_code = 1;"
                cur.execute(sql)
                sql = "DELETE FROM airplanes WHERE type_code = 2;"
                cur.execute(sql)
                sql = "DELETE FROM airplanes WHERE type_code = 3;"
                cur.execute(sql)                
                print("\nDELETED")
        
        elif (str(option) == '4'):
                sql = "SELECT * FROM airplanes WHERE seats = 300;"
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