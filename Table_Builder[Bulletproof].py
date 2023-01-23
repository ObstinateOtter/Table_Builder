import mysql.connector as sql
from tabulate import tabulate

user_pwd = input('Enter SQL password for authorization: ')

try:
    sqlcon = sql.connect(user = 'root', password= user_pwd)
    Mysql = sqlcon.cursor()
    print('\nSuccessfully connected to MySQL\n')
except:
    print('\nConnection Error!!!')
    input('Access Denied.\n')
    exit()


def build_table():
    db_name = input("Enter the name of your database: ")
    Mysql.execute(f'CREATE DATABASE IF NOT EXISTS {db_name};')
    con = sql.connect(user = 'root', password= user_pwd, database= f'{db_name}')
    cur = con.cursor()

    print(f"Using {db_name}")

    tb_name = input("Enter the name of your table: ")
    comp_col = input('Enter the name of the coloumn: ')
    comp_dt= input('Enter the datatype: ')
    try:
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
    except:
        print(f'Table `{tb_name}` already exists!')

def add_values():
    db_name = input("Enter the name of your database: ")
    try:
        con = sql.connect(user = 'root', password= user_pwd, database= f'{db_name}')
        cur = con.cursor()
        print(f"Using {db_name}")
        table = input('Enter Table name: ')
        try:
            cur.execute(f'DESC {table}')
            lst = cur.fetchall()
            print('\n',tabulate(lst,headers=['Field','Type','Null','Key','Default','Extra'],tablefmt='pretty'),'\n')    

            tst = []            #lst = [('col1','int',None,None,None),('col2','varchar(30)','YES',None,None,None)]
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
            cur.execute(f'SELECT * FROM {table};')
            all_val = cur.fetchall()
            print(tabulate(all_val,headers=tst,tablefmt='pretty'))  #type:ignore
            con.commit()
        except:
            print(f'Table `{table}` does not exist!')
    except:
        print(f'Database `{db_name}` does not exist!')

def manual():
    cmd = input('\nEnter your query: ')
    if cmd != '':
        if cmd[-1] != ';':
            cmd += ';'
        try:
            Mysql.execute(cmd)
            print(f'\n "{cmd}" Successfully Executed')
            for i in Mysql:     
                print(i)
            sqlcon.commit()
        except:
            print('\nCommand Syntax Error!!!')
        manual()

def main():
    ch = input("""\n
1.Build a table
2.Add values to your table
3.Manually enter your commands
4.Exit
Enter Choice: """)

    if ch == '1':
        build_table()
    elif ch == '2':
        add_values()
    elif ch == '3':
        manual()
    elif ch == '4':
        input('Exited\n')
        exit()
    else:
        print('\n\t Invalid Input!!! \n')
    main()

main()
