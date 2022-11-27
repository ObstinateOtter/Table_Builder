import mysql.connector as sql
from tabulate import tabulate

sqlcon = sql.connect(user = 'root', password='pwd')
Mysql = sqlcon.cursor()

if sqlcon.is_connected():
    print('Successfully connected to MySQL')
else:
    print('Connection Error')
    exit()


def build_table():
    db_name = input("Enter the name of your database: ")
    Mysql.execute(f'CREATE DATABASE IF NOT EXISTS {db_name};')
    con = sql.connect(user = 'root', password='SQL#785%', database= f'{db_name}')
    cur = con.cursor()
    print(f"Using {db_name}")

    tb_name = input("Enter the name of your table: ")
    comp_col = input('Enter the name of the coloumn[leave blank to view table description]: ')
    if comp_col != '':
        comp_dt= input('Enter the datatype: ')
        cur.execute(f'CREATE TABLE {tb_name}({comp_col} {comp_dt});')
        print(f"Created table {tb_name}")

        while True:
            col = input('Enter the name of the coloumn[leave blank to exit]: ')
            if col == '':
                break
            datatype = input('Enter the datatype: ')
            cur.execute(f'ALTER TABLE {tb_name} ADD {col} {datatype};')
            print('\n Coloumn added Successfully \n')
            cur.execute(f'DESC {tb_name}')
            lst = cur.fetchall()
            print(lst)
            print(tabulate(lst,headers=['Field','Type','Null','Key','Default','Extra'],tablefmt='pretty'))
        cur.execute(f'DESC {tb_name}')
        lst = cur.fetchall()
        print(lst)
        print(tabulate(lst,headers=['Field','Type','Null','Key','Default','Extra'],tablefmt='pretty'))


def add_values():
    db_name = input("Enter the name of your database: ")
    con = sql.connect(user = 'root', password='SQL#785%', database= f'{db_name}')
    cur = con.cursor()
    print(f"Using {db_name}")

    table = input('Enter Table name: ')
    cur.execute(f'DESC {table}')
    lst = cur.fetchall()
    print('\n',tabulate(lst,headers=['Field','Type','Null','Key','Default','Extra'],tablefmt='pretty'),'\n')

    tst = []
    for i in range(len(lst)):
        tst.append(lst[i][0])

    a = 1
    while a > 0:
        cmd = []
        view = []
        f_view = []
        for i in range(len(lst)):       #type: ignore
            print(f'{len(lst)-i} coloumn(s) left to enter\n')
            val = input("Enter your Values: ")
            if val == '':
                a -= 1
                break

            try:
                num = int(val)
                cmd.append(num)
            except:
                cmd.append(val)
            view.append(val)

        if a == 0:
            break

        cur.execute(f'INSERT INTO {table} VALUES{tuple(cmd)};')

        f_view.append(view)
        print(tabulate(f_view,headers=tst,tablefmt='pretty'))

        print("\n Enter next set of values \n")
    con.commit()

def display():
    pass

def manual():
    cmd = input('Enter your query: ')
    if cmd != '':
        if cmd[-1] != ';':
            cmd += ';'
        Mysql.execute(cmd)
        print(f'\n "{cmd}" Successfully Executed \n')
        for i in Mysql:     #type: ignore
            print(i)
        sqlcon.commit()
        manual()

while True:
    ch = int(input("""
1.build table
2.add values
3.display table
4.manually enter commands
5.exit
Enter Choice: """))
    if ch == 1:
        build_table()
    if ch == 2:
        add_values()
    if ch == 3:
        display()
    if ch == 4:
        manual()
    if ch == 5:
        exit()
    else:
        print('\n Invalid Input!!! \n')
