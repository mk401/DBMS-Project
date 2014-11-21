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

def print_table(rows, options = []):
        table = PrettyTable()
        names = rows[0]
        table.field_names = names
        for i in range(1,len(rows)):
                table.add_row(rows[i])


        #if sort == 0:
                #print("\nSort by which column?")
                #sql_print_column_names(names)
                #option = input("Sort by (Enter 0 to skip sorting): ")
                #if str(option) != '0':
                        #sort = names[int(option)-1]
                        #table.get_string(sortby = str(sort))

        #elif sort == 1:
                #table.get_string(sortby = "code")
                #table.sortby = sort

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

def create_reservation(round_trip = False):
        pass_name = input("Enter passenger's name: ")
        pass_phone = input("Enter passenger's phone number (no hyphens or spaces): ")

        print("Choose destinations.\n")
        rows = sql_get_all('airports')
        print_table(rows)

        start = input("Starting destination index number: ")
        start_code = rows[int(start)][0]
        end = input("Ending destination index number: ")
        end_code = rows[int(end)][0]
        depart_date = input("Departure date (yyyy-mm-dd): ")

        get_trip(start_code, end_code, depart_date, pass_name, pass_phone)

        if round_trip == True:
                return_date = input("Return Date (yyyy-mm-dd): ")
                get_trip(end_code, start_code, return_date, pass_name, pass_phone)

def get_trip(start_code, end_code, depart_date, pass_name, pass_phone):
        sql = "SELECT flight_num, fare_code FROM flights WHERE start_point='{}' AND end_point='{}';".format(start_code, end_code)
        cur.execute(sql)
        flight = cur.fetchall()[0]
        sql = "SELECT * FROM leg_instance WHERE flight_num = {}  AND date = '{}' AND seats > 0".format(flight[0], depart_date)
        cur.execute(sql)
        legs = cur.fetchall()
        if len(legs) > 0:
                for leg in legs:
                        seats = leg[4] - 1
                        sql = "SELECT max(seat_num) from reservations WHERE leg_num = " + str(leg[2]) + " and date ='" + depart_date + "';"
                        cur.execute(sql)
                        test = cur.fetchall()[0][0]
                        if test == None: test = 0

                        seat_num = int(test) + 1
                        sql = "INSERT INTO reservations (seat_num, date, flight_num, leg_num, pass_phone, pass_name) VALUES ({},'{}',{},{},'{}','{}')".format(seat_num, depart_date, leg[1], leg[2], pass_phone, pass_name)
                        cur.execute(sql)
                        cur.execute("UPDATE leg_instance SET seats = " + str(seats) + " WHERE leg_num = " + str(leg[2]) + " AND date = '" + depart_date + "';")

                cur.execute("select cost from fares where code = " + str(flight[1]) + ";")
                print("Cost for flight from", start_code, "to", end_code, "is " + str(cur.fetchall()[0][0]))
                conn.commit()
        else: print("No Available flights with those parameters")
        #leg_instance = date, flight_num, leg_num, tail_number, seats, depart_time, arrival_time, index
        #reservations = seat_num, date, flight_num, leg_num, pass_phone, pass_name, index

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


        sql = "select * from flights where " + weekday + "=true;"
        cur.execute(sql)
        flights = cur.fetchall()

        for flight in flights:
                sql = "select * from flight_legs where flight_num = " + str(flight[0]) + ";"
                cur.execute(sql)
                for leg in cur.fetchall():
                        sql = "insert into leg_instance (date, flight_num, leg_num, tail_number, depart_time, arrival_time) values ('{}', {}, {}, {}, '{}', '{}');".format(date_str(date), leg[1], leg[0], planes.pop(), leg[4], leg[5])
                        cur.execute(sql)
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

def cancel_reservation(delete_date = None, pass_phone = None):
        sql="select column_name from information_schema.columns where table_name='{}';".format("reservations")
        cur.execute(sql)
        columns = cur.fetchall()
        names = []
        rows = []
        for name in columns:
                names.append(name[0])
        rows.append(names)        
        pass_phone = input("Enter customer phone number: ")
        sql = "SELECT * FROM reservations WHERE pass_phone = '{}';".format(pass_phone)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
                data = []
                i = 0
                for datum in row:
                        data.append(row[i])
                        i += 1
                rows.append(data)
        print_table(rows)
        
        delete_date = input("Enter date of reservation to cancel (yyyy-mm-dd): ")
        sql = "DELETE FROM reservations WHERE date = '{}' AND pass_phone = '{}'".format(delete_date, pass_phone)
        cur.execute(sql)

def change_reservation():
        sql="select column_name from information_schema.columns where table_name='{}';".format("reservations")
        cur.execute(sql)
        columns = cur.fetchall()
        names = []
        rows = []
        for name in columns:
                names.append(name[0])
        rows.append(names)        
        pass_phone = input("Enter customer phone number: ")
        sql = "SELECT * FROM reservations WHERE pass_phone = '{}';".format(pass_phone)
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
                data = []
                i = 0
                for datum in row:
                        data.append(row[i])
                        i += 1
                rows.append(data)
        print_table(rows)
        
        delete_date = input("Enter date of reservation to change (yyyy-mm-dd): ")
        sql = "SELECT * FROM reservations WHERE date = '{}' AND pass_phone = '{}'".format(delete_date, pass_phone)
        cur.execute(sql)
        results = cur.fetchall()[0]
        seat_num = results[1]
        flight_num = results[2]
        pass_phone = results[4]
        pass_name = results[5]
        sql = "SELECT * FROM flights WHERE flight_num = {};".format(flight_num)
        cur.execute(sql)
        results = cur.fetchall()[0]
        start_code = results[10]
        end_code = results[11]
        sql = "DELETE FROM reservations WHERE date = '{}' AND pass_phone = '{}';".format(delete_date, pass_phone)
        cur.execute(sql)
        new_date = input("Enter new date of reservation (yyyy-mm-dd): ")
        
        get_trip(start_code, end_code, new_date, pass_name, pass_phone)
        
        #flight = flight_num | monday | tuesday | wednesday | thursday | friday | saturday | sunday |  airline   | fare_code | start_point | end_point | index
        #reservations = | date | seat_num | flight_num | leg_num | pass_phone | pass_name | index |

while run:
        print("OPTIONS:\n1. Manual Entry\n2. View Data\n3. Plan Trip\n4. Plan Multi-Flight Trip\n5. Change Reservation\n6. Cancel Trip\n7. EXIT")

        option = input("Choose an option: ")

        if (str(option) == '1'):
                edit()
                input("Press Enter to continue...")
                print("\n")
                
        elif (str(option) == '2'):
                entry()
                input("Press Enter to continue...")
                print("\n")
                
        elif (str(option) == '3'):
                populate_week()
                create_reservation()
                input("Press Enter to continue...")
                print("\n")                
                
        elif (str(option) == '4'):
                populate_week()
                create_reservation(True)
                input("Press Enter to continue...")
                print("\n")                

        elif (str(option) == '5'):
                change_reservation()
                input("Press Enter to continue...")
                print("\n")    
                
        elif (str(option) == '6'):
                cancel_reservation()
                input("Press Enter to continue...")
                print("\n")                

        elif (str(option) == '7'):
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