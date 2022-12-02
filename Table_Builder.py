import mysql.connector as sql
from tabulate import tabulate

pwd = '' #Enter your SQL-root password

try:
    sqlcon = sql.connect(user = 'root', password='pwd')
    Mysql = sqlcon.cursor()
    print('\nSuccessfully connected to MySQL')
except:
    print('\nConnection Error!!!')
    print('Check if you have given the correct SQL-root password.')
    exit()


def build_table():
    db_name = input("Enter the name of your database: ")
    Mysql.execute(f'CREATE DATABASE IF NOT EXISTS {db_name};')
    con = sql.connect(user = 'root', password='pwd', database= f'{db_name}')
    cur = con.cursor()

    print(f"Using {db_name}")

    tb_name = input("Enter the name of your table: ")
    comp_col = input('Enter the name of the coloumn: ')
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
        print(tabulate(lst,headers=['Field','Type','Null','Key','Default','Extra'],tablefmt='pretty'))


def add_values():
    db_name = input("Enter the name of your database: ")
    con = sql.connect(user = 'root', password='pwd', database= f'{db_name}')
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
        for i in range(len(lst)):
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

        if len(cmd) == 1:
            f_cmd = str(tuple(cmd)).replace(",)",')')
        else:
            f_cmd = str(tuple(cmd))
        
        cur.execute(f'INSERT INTO {table} VALUES{f_cmd};')
        f_view.append(view)
        print(tabulate(f_view,headers=tst,tablefmt='pretty'))

        print("\n Enter next set of values \n")
    con.commit()


def manual():
    cmd = input('Enter your query: ')
    if cmd != '':
        if cmd[-1] != ';':
            cmd += ';'
        try:
            Mysql.execute(cmd)
            print(f'\n "{cmd}" Successfully Executed \n')
            for i in Mysql:
                print(i)
            sqlcon.commit()
        except:
            print('Command Syntax Error!!!')
        manual()


while True:
    ch = input("""\n
1.build table
2.add values
3.manually enter commands
4.exit
Enter Choice: """)
    if ch == '1':
        build_table()
    elif ch == '2':
        add_values()
    elif ch == '3':
        manual()
    elif ch == '4':
        exit()
    else:
        print('\n\t Invalid Input!!! \n')
