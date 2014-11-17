import psycopg2

print("Connecting...")
# Connect to an existing database
conn = psycopg2.connect(database="Project", user="Project", host="162.243.19.108")
print("Connected")

# Open a cursor to perform database operations
cur = conn.cursor()
run = True

def entry():
        print("\nTables:\n")
        sql="select table_name from information_schema.tables where table_schema='public';"
        tables = sql_print_first(sql)
        option = input("\nSelect a table: ")
        selected = tables[option-1][0]

        sql_get_all(selected)

def sql_print_first(sql):
        cur.execute(sql)
        i = 1
        rows = cur.fetchall()
        for row in rows:
                print(str(i) + ". " + str(row[0]))
                i += 1
        return rows

def sql_get_all(table):
        sql="select column_name from information_schema.columns where table_name='" + table + "';"
        cur.execute(sql)
        i = 0
        columns = cur.fetchall()
        names = []
        rows = []
        for name in columns:
                names.append(name[0])
        rows.append(names)

        sql="select * from " + table
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
                data = []
                i = 0
                for datum in row:
                        data.append(row[i])
                        i += 1
                rows.append(data)
        print(rows)
        return rows

while run:
        print("OPTIONS:\n1. Manual Entry\n2. View Data\n3. Plan Trip\n4. Plan Multi-Flight Trip\n5. Cancel Trip\n6. EXIT")

        option = input("Choose an option: ")

        if (str(option) == '1'):
                entry()
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

        elif (str(option) == '6'):
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