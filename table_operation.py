import psycopg2
import pandas as pd
def truncate_table():
    table_name = input("Enter name of table: ")
    try:
        conn = psycopg2.connect(dbname="assignmentdb", user="postgres", password="795472", host="localhost",
                                port="5432")
    except psycopg2.Error as e:
        print(e)
    else:
        cursor = conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table_name};")
        conn.commit()
        # print(f"Table {table_name} created successfully")
        cursor.close()
        print(f"The contents of table {table_name} deleted successfully")


def create_table(table_name, nos_field):
    i = 1
    fields_list = []
    while nos_field >= i:
        fields_list.append(input(f"Enter name of {i} field: ") + "  " + input("Enter type of field. text/int: "))
        i += 1
    print(fields_list)
    col = ", ".join(fields_list)
    try:
        conn = psycopg2.connect(dbname="assignmentdb", user="postgres", password="795472", host="localhost",
                                port="5432")
    except psycopg2.Error as e:
        print(e)
    else:
        cursor = conn.cursor()
        cursor.execute(f"create table {table_name}({col});")
        conn.commit()
        #print(f"Table {table_name} created successfully")
        cursor.close()
        print(f"Table {table_name} created Successfully")


def drop_table():
    table_name = input("Enter name of table: ")
    try:
        conn = psycopg2.connect(dbname="assignmentdb", user="postgres", password="795472", host="localhost",
                                port="5432")
    except psycopg2.Error as e:
        print(e)
    else:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        # print(f"Table {table_name} created successfully")
        cursor.close()
        print(f"Table {table_name} deleted successfully")


def insert_data():
    while True:
        try:
            conn = psycopg2.connect(dbname="assignmentdb", user="postgres", password="795472", host="localhost",
                                    port="5432")
        except psycopg2.Error as e:
            print(e)
        else:
            cursor = conn.cursor()
            with cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE';
                """)
                tables = cursor.fetchall()
                for table in tables:
                    print(f"{table[0]}")
                u_table_input = input("Enter Table Name: ")
                cursor.execute("""
                    SELECT column_name,data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                    """, (u_table_input,))
                fields = cursor.fetchall()

                value_data = []
                field_name = [field[0] for field in fields]
                column = ", ".join(field_name)

                for field in field_name:
                    value_data.append(input(f"Enter {field}: "))
                value_data = tuple(value_data)
                sql = f"insert into {u_table_input}({column}) values{value_data}"
                try:
                    cursor.execute(sql, field_name)
                except psycopg2.Error as e:
                    print(e)
                else:
                    conn.commit()
                    print(f"Data inserted Successfully in the table {u_table_input}")
                    print(sql)
                    user_choice = input("Do you want to continue? (y/n): ")
                    if user_choice == "y":
                        continue
                    else:
                        break

            cursor.close()


def update_data():
    conn = psycopg2.connect(dbname="assignmentdb",
                            user="postgres",
                            password="795472",
                            host="localhost",
                            port="5432")
    sql_showtable = """SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE';"""
    cur = conn.cursor()
    cur.execute(sql_showtable)
    tables = cur.fetchall()
    slno = 1
    table_dic = {}
    print(f'There are {len(tables)} tables in the database.')
    for table in tables:
        print(f"{slno} -  {table[0]}")
        table_dic.update({slno: table[0]})
        slno += 1
    x = int(input("Enter your choice: "))
    sql_field = """SELECT column_name,data_type
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position;"""
    cur.execute(sql_field,(table_dic[x],))

    fields = cur.fetchall()
    field_name = [field[0] for field in fields]
    column = ", ".join(field_name)
    print(f'There are {len(field_name)} columns in the table {table_dic[x]}.')
    col_slno = 1
    col_dic = {}
    for col in field_name:
        print(f"{col_slno} -  {col}")
        col_dic.update({col_slno: col})
        col_slno += 1
    y = int(input("Enter your choice: "))
    s_param = input("Enter parameteric Value")
    sql_findrecord = f"""SELECT * FROM {table_dic[x]} WHERE {col_dic[y]} = '{s_param}';"""
    cur.execute(sql_findrecord)

    #print(fetched_record.__len__())
    try:
        fetched_record = cur.fetchall()


    except psycopg2.Error as e:
        print(e)
    else:
        if fetched_record.__len__() == 0:
            print(f"There are no records in the table {table_dic[x]}")
        else:
            df = pd.DataFrame(fetched_record,columns=field_name)
            print(df)
            print("What do you want? Delete Or Update! Kindly enter d for delete, u for update or any key for exit")
            update_choice = input("Enter Choice: ")
            if update_choice == "d":
                sql_del = f"""
                            DELETE FROM {table_dic[x]} WHERE {col_dic[y]} = '{s_param}'; 
                            """
                cur.execute(sql_del)
                conn.commit()
                print("The record deleted successfully")
            elif update_choice == "u":

                value = {}
                for field in field_name:
                    value.update({field:input(f"Enter new {field} : ")})
                print(value)
                set_value = []
                for field in field_name:
                    if value[field] == '':
                        value.__delitem__(field)

                i = 0
                for field in field_name:
                    if  field in value:
                        v_set = field + "=" + f"'{value[field]}'"

                        set_value.append(v_set)
                    else:
                        print("Value is empty")
                    i += 1

                set_param = ", ".join(set_value)
                print(set_param)
                sql_update = f"""
                                UPDATE {table_dic[x]} SET {set_param} WHERE {col_dic[y]} = '{s_param}';
                            """

                cur.execute(sql_update)
                conn.commit()
                print("The record updated successfully")
            else:
                exit
    cur.close()
def view_content():
    while True:
        try:
            conn = psycopg2.connect(dbname="assignmentdb", user="postgres", password="795472", host="localhost",
                                    port="5432")
        except psycopg2.Error as e:
            print(e)
        else:
            # cursor = conn.cursor()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE';
                """)
                tables = cursor.fetchall()
                print(f'There are following {len(tables)} tables in the database. Which table data you want to view')
                for table in tables:
                    print(f"{table[0]}")
                u_table_input = input("Enter Table Name: ")
                cursor.execute("""
                    SELECT column_name,data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                    """, (u_table_input,))
                fields = cursor.fetchall()

                field_name = []
                for i in fields:
                    field_name.append(i[0])

                sql = f"SELECT * FROM {u_table_input}"
                try:
                    cursor.execute(sql)
                    x = cursor.fetchall()
                except psycopg2.Error as e:
                    print(e)
                else:
                    df = pd.DataFrame(x,columns=field_name)
                    print(df)

                    user_choice = input("Do you want to continue? (y/n): ")
                    if user_choice == "y":
                        continue
                    else:
                        break
            conn.commit()
            cursor.close()
print("Welcome to Table Operation")
while True:
    print("1 to inserting data\n2 to View Data\n"
          "3 to modify the data\n4 for creating new table\n"
          "5 to delete the table\n6 to delete the content of the table\n7 to exit the program")
    try:
        x= int(input("Enter your choice: "))
    except psycopg2.Error as e:
        print(e)
    else:
        if x == 1:
            insert_data()
        elif x == 2:
            view_content()
        elif x == 3:
            update_data()
        elif x == 4:
            x = input("Enter name of table: ")
            n_fields = int(input("Enter number of fields: "))
            create_table(x, n_fields)
        elif x == 5:
            drop_table()
        elif x == 6:
            truncate_table()
        elif x == 7:
            break
        else:
            yes_no = input("Do you want to continue? (y/n): ")
            if yes_no == "y":
                continue
            else:
                break

