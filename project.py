import psycopg2
import datetime
from prettytable import PrettyTable


print("Connecting...")
# Connect to an existing database
conn = psycopg2.connect(database="Project", user="Project", host="162.243.19.108")
print("Connected")

# Open a cursor to perform database operations
cur = conn.cursor()
run = True

def edit():
        print("OPTIONS:\n1. CREATE\n2. UPDATE\n3.DELETE")
        option = input("Choose an option: ")
        if str(options) == '1':
                sql = input("Enter create statement: ")
                cur.execute(sql)
        elif str(options) == '2':
                sql = input("Enter update statement: ")
                cur.execute(sql)
        elif str(options) == '3':
                sql = input("Enter delete statement: ")
                cur.execute(sql)

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
<<<<<<< HEAD
                        table.get_string(sortby = str(sort))
        
        elif sort == 1:
                table.get_string(sortby = "code")
        
=======
                        table.sortby = sort

        elif sort == 1:
                print('here')
                table.sortby = "code"

>>>>>>> origin/master
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

        sql="select * from " + table + " order by " + names[0] + " ASC"
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
        print("Choose destinations.\n")
        rows = sql_get_all('airports')
        print_table(rows, sort = 1)
        start = input("Starting destination index number: ")
        start_code = rows[int(start)]
        end = input("Ending destination index number: ")
        end_code = rows[int(end)]

def get_weekday(num):
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return(days[num])

def populate_week():
        start_date = datetime.datetime.now()
        for i in range(0,7):
                date = start_date + datetime.timedelta(days=i)
                cur.execute("select count(*) from leg_instance where date = '" + date_str(date) + "';")
                if cur.fetchall()[0][0] == 0:
                        populate_day(date)

def populate_day(date):
        weekday = get_weekday(date.weekday())
        planes = check_planes(date)
        print(planes)

        sql = "select * from flights where " + weekday + "=true;"
        cur.execute(sql)
        flights = cur.fetchall()

        for flight in flights:
                sql = "select * from flight_legs where flight_num = " + str(flight[0]) + ";"
                cur.execute(sql)
                for leg in cur.fetchall():
                        sql = "insert into leg_instance (date, flight_num, leg_num, tail_number, depart_time, arrival_time) values ('{}', {}, {}, {}, '{}', '{}');".format(date_str(date), leg[1], leg[0], planes.pop(), leg[4], leg[5])
                        print(sql)
                        cur.execute(sql)
        print(planes, "\n")
        conn.commit()

def date_str(date):
        return str(date.year) + "-" + str(date.month) + "-" + str(date.day)

def check_planes(date):
        sql = "select tail_number from leg_instance where date = '" + date_str(date) + "';"
        cur.execute(sql)
        used_planes = []
        for row in cur.fetchall():
                used_planes.append(row[0])

        sql = "select tail_number from airplanes;"
        cur.execute(sql)
        all_planes = []
        for row in cur.fetchall():
                all_planes.append(row[0])

        return(list(set(all_planes)-set(used_planes)))
while run:
        print("OPTIONS:\n1. Manual Entry\n2. View Data\n3. Plan Trip\n4. Plan Multi-Flight Trip\n5. Cancel Trip\n6. EXIT")

        option = input("Choose an option: ")

        if (str(option) == '1'):
                edit()
        elif (str(option) == '2'):
                entry()
        elif (str(option) == '3'):
                populate_week()
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