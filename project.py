import psycopg2
from prettytable import PrettyTable


print("Connecting...")
# Connect to an existing database
conn = psycopg2.connect(database="Project", user="Project", host="162.243.19.108")
print("Connected")

# Open a cursor to perform database operations
cur = conn.cursor()
run = True

def entry(options = []):
        print("\nTables:\n")
        sql="select table_name from information_schema.tables where table_schema='public';"
        tables = sql_print_first(sql)
        option = input("\nSelect a table: ")
        selected = tables[int(option)-1][0]

        data = sql_get_all(selected)
        print_table(data, options)     

def sql_print_first(sql):
        cur.execute(sql)
        i = 1
        rows = cur.fetchall()
        for row in rows:
                print(str(i) + ". " + str(row[0]))
                i += 1
        return rows

def sql_print_column_names(columns):
        i = 1
        j = 0
        for column in columns:
                print(str(i) + ". " + str(columns[j]))
                i += 1
                j += 1

def print_table(rows, options = [], sort = 0):
        table = PrettyTable()
        names = rows[0]
        table.field_names = names
        for i in range(1,len(rows)):
                table.add_row(rows[i])
        
        
        if sort == 0:
                print("\nSort by which column?")
                sql_print_column_names(names)                
                option = input("Sort by (Enter 0 to skip sorting): ")
                if str(option) != '0':
                        sort = names[int(option)-1]
                        table.sortby = sort
        
        elif sort == 1:
                print('here')
                table.sortby = "code"
        
        index = []
        index.extend(range(1, len(rows)))
        table.add_column("index", index)
        if len(options) != 0:
                print(table.get_string(fields = options))
        else:
                print(table)        

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
        
        return rows

def create_reservation():
        print("Choose starting destination.")
        rows = sql_get_all('airports')
        print_table(rows, sort = 1)




while run:
        print("OPTIONS:\n1. Manual Entry\n2. View Data\n3. Plan Trip\n4. Plan Multi-Flight Trip\n5. Cancel Trip\n6. EXIT")

        option = input("Choose an option: ")

        if (str(option) == '1'):
                entry()
        elif (str(option) == '2'):
                entry()
        elif (str(option) == '3'):
                create_reservation()
        elif (str(option) == '4'):
                sql = "SELECT * FROM airplanes WHERE seats = 300;"
                cur.execute(sql)
                print(cur.fetchall())

        elif (str(option) == '6'):
                run = False


        else:
                print("Invalid option choice!\n")
                
        input("Press Enter to continue...")
        print("\n")

        # Query the database and obtain data as Python objects
        #cur.execute("select * from people;")
        #print(cur.fetchall())

        # Make the changes to the database persistent
        conn.commit()



# Close communication with the database
cur.close()
conn.close()