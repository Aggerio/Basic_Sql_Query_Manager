import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import sys
import csv
import os
import pyfiglet
import time

users = ['trial']
passwords = ['password']
databases = []
table = ''
datab = ''
logo = pyfiglet.figlet_format("MYSQL FOR KIDS")
current_window = 0 
user_login = ''
passw = ''

def login():

	global mydb
	global mycursor,user_login,passw

	user_login = input("Please enter your username: ")

	if user_login.replace(" ", "") in users:
		pass
	else:
		print("the entered username is not a user please try again!!")
		login()

	passw = input("Please input your password: ")

	try:
		if passw.replace(" ", "") in passwords:
			mydb = mysql.connector.connect(
				host="localhost",
				user=user_login,
				password=passw,
				autocommit=True
			)
			mycursor = mydb.cursor()
		elif passw not in passwords:
			print("Wrong Password please try again")
			login()

		print("Successfully logged in Mysql ")
	
	except mysql.connector.errors.ProgrammingError:
		print("Wrong Password or username reverting back to main menu")
	


def Show_Main_Menu(cur_window):

	print(f"{logo}")

	if cur_window == 0:
		print("[0] Login to the database")
		print("[1] Show Available Databases ")  # --> Done
		print("[2] Create a new database ")  # --> Done
		print("[3] Use a database ")  # Done
		print("[4] Add a new user  ")  # --> Done
		print("[5] Delete a user")  # --> Done
		print("[6] Change your password")  # --> Done
		print("[7] Login again")  # --> Done
		print("[99] Exit the program")  # --> Done

	if cur_window == 1:
		print("[0] Show all the tables and choose a table")
		print("[1] See the full table")  # ---> Done
		print("[2] See selective columns from the table")  # --> Done
		print("[3] alter table")  # --> Done
		print("[4] desc table")  # --> Done
		print("[5] load a new table from csv")  # --> Done
		print("[6] make a bar graph of two columns from a single table")  # --> Done
		print("[99] Back to Main Menu")  # --> Done


def get_db():

	databases = []

	mycursor.execute("show databases;")

	db_list = mycursor.fetchall()

	for y in range(len(db_list)):
		if db_list[y] in databases:
			pass
		else:
			str = ''.join(db_list[y])
			databases.append(str)

	print("\n\nThe current databases are: ")
	for i in databases:
		print(i)


def create_db():
	db_name = input("Enter the name of the new database: ")
	sql = f"create database {db_name};"
	mycursor.execute(sql)

	print(mycursor.fetchall())

	print(f"New Databases Create with the name {db_name}")





def add_new_user():
	new_user = input("Enter the new username: ")
	
	exists = False

	sql = "select user from mysql.user;"
	users = pd.read_sql(sql, con = mydb)

	for i in range(len(users['user'])):
		


	    if users['user'][i] == new_user:

	        exists = True
    

	    else:
	        
	        exists = False


	if exists == True:
		pass

	else:
		users.append(new_user)

		pass_new = input("Enter the new password of the user: ")
		passwords.append(pass_new)

		sql = f"create user '{new_user}'@'localhost' identified by {pass_new};"
		mycursor.execute()

		sql = f"grant all privileges on *.* to {new_user}@localhost;"

		print("New user created pls login again to use the new user ")


def update_password():
	username = input("Enter your username: ")

	for i in range(len(users)):
		if users[i] == username:
			no = i
		else:
			print("User not found ")
			print("Would you like to try again")

	new_pass = input("Enter your new password: ")
	passwords[i] = new_pass

	sql = f"alter user {username}@localhost identified by {new_pass};"
	mycursor.execute(sql)

	sql = "FLUSH PRIVILEGES;"
	mycursor.execute(sql)

	print("Password updated successfully")


def delete_user():
	print("The currents users are:- ")
	for i in range(len(users)):
		print(f"[{i + 1}] {users[i]}")

	del_user = int(input("Enter the index of the user you want to delete: "))

	if del_user > 0 & del_user < len(users):

		users.pop(del_user - 1)
		passwords.pop(del_user - 1)
		sql = f"DROP USER {user[del_user - 1]}@localhost;"
		mycursor.execute(sql)
		print("user deleted")

	else:
		print("invalid id ")


def Exit():

	print("Bye!!")
	mycursor.commit()
	mycursor.close()
	sys.exit()

def BackToMainMenu():
	global current_window
	current_window = 1

class Table:

	# need to do the whole alter table commands

	global mydb, current_window, mycursor, table, datab
	global user_login, passw

	def show_available_tables():

		global table

		d = []
		sql = "show tables;"
		tb = pd.read_sql(sql, con = mydb)
		x = f"Tables_in_{datab}"
		d = tb[x]

		for i in range(len(d)):
			print(f"[{i+1}] {d[i]}")
	    	
		tb = int(input("Enter the table you want to perform actions upon: "))

		table = d[tb - 1]

	def See_full_table(table):

		print("The whole table is: ")
		sql = f"select * from {table};"
		df = pd.read_sql(sql, con = mydb)
		print(df)

	def alter_table(table):

		#do alter_table again 

		print("[1] Add a column")
		print("[2] Drop a column")
		print("[3] Modify a column")

		index = int(input("Enter the choice you want: "))

		if index == 1:
			
			dtype = ''
			new_name = input("Enter the name of the new table: ")

			print("Following are the three data types for the table: ")

			print("[1]For integer = int")
			print("[2]For string = varchar(1000)")
			print("[3]For date = DATE")

			inp = int(input("Input the datatype of the new table: "))

			if inp == 1:
				dtype = "int(100)"

			if inp == 2:
				dtype = "varchar(100)"

			if inp == 3:
				dtype = "DATE"

			else:
				Table.alter_table(table)

			sql = f"alter table {table} add {new_name} {dtype};"
			mycursor.execute(sql)

			print("New table created ")

		elif index == 2:

			print("The current columns are:- ")
			columns = pd.read_sql(f'select * from {table}', con = mydb)

			column = columns.columns

			col = []

			for i in range(len(column)):
				x = column[i]
				col.append(x)

			for i in range(len(col)):
				print(f"[{i+1}] {col[i]}")

			drop = int(input("Enter the number of the column you want to drop: "))

			sql = f"alter table {table} drop column {col[drop-1]};"
			mycursor.execute(sql)
			print("Dropped column")

		elif index == 3:

			print("The current columns are")
			columns = pd.read_sql(f'select * from {table}', con = mydb)

			column = columns.columns

			col = []

			for i in range(len(column)):
				x = column[i]
				col.append(x)

			for i in range(len(col)):
				print(f"[{i+1}] {col[i]}")

			mod = int(input("Enter the column you want to modify"))

			print("Choose a datatype ")

			print("[1]For integer = int")
			print("[2]For string = varchar(1000)")
			print("[3]For date = DATE")

			inp = int(input("Input the datatype of the altered table: "))

			if inp == 1:
				dtype = "int(100)"

			if inp == 2:
				dtype = "varchar(100)"

			if inp == 3:
				dtype = "DATE"

			sql = f"alter table {table} modify column {col[mod -1]} {dtype};"
			mycursor.execute(sql)
			print("Altered table see the changes by desc table")

		else:
			print("Not a valid index try again")
			alter_table()

	def desc_table(table):
			sql = f"desc {table}"
			res = pd.read_sql(sql, con = mydb)
			print(res)

	def Select_Column(datab):

		print("The current columns are:- ")
		columns = pd.read_sql(f'select * from {table}', con = mydb)

		column = columns.columns
		col = []

		for i in range(len(column)):
			x = column[i]
			col.append(x)

		for i in range(len(col)):
			print(f"[{i+1}] {col[i]}")

		Selected_column = input("Select the columns you want seperated by commas: ")
		sel_col = Selected_column.split(',')

		for i in range(len(sel_col)):
		    sel_col[i] = int(sel_col[i])

		for i in sel_col:
			
			if i <= len(col):
				pass
			else:
				print("entered column is not valid please try again")
				Select_Column()

		st1 = ''
		
		for i in range(len(sel_col)):
			if i < len(sel_col) - 1:
				st1 = st1 + col[i] + ','
			if i == len(sel_col) -1:
				st1 = st1 + col[i]

		sql = f"select {st1} from {table};"
		res = pd.read_sql(sql, con = mydb)
		print(f"The Columns you have select are {st1}")
		print(res)

	


	def bar_graph(table):

		print("The current columns are:- ")
		columns = pd.read_sql(f'select * from {table}', con = mydb)

		column = columns.columns

		col = []

		for i in range(len(column)):
			x = column[i]
			col.append(x)

		for i in range(len(col)):
			print(f"[{i+1}] {col[i]}")

		col_x = int(input("Enter the column you want to be the x axis of the bar graph: "))
		col_y = int(input("Enter the column you want to be the y axis of the bar graph: "))

		x = columns[column[col_x - 1]]
		x_cord = []

		for i in range(len(columns[column[col_x - 1]])):
		    n = columns[column[col_x - 1]][i]
		    x_cord.append(n)	

		y = columns[column[col_y - 1]]
		y_cord = []

		for i in range(len(columns[column[col_y - 1 ]])):
				n = columns[column[col_y -1]][i]
				y_cord.append(n)

		print("Making graph")

		plt.bar(x_cord,y_cord, width = 0.5)
		plt.show()

	def desc_graph(table):
		sql = f"desc {table}"
		desc = pd.read_sql(sql,con = mydb)
		print(desc)

	def load_table(table):

		csv_path = input("Enter the path to the file: ")

		if os.path.isfile(csv_path):
			pass

		else:
			print("invalid path please try again: ")
			load_table()

		new_name = input("Enter the name of the new table: ")

		import pymysql
		pymysql.install_as_MySQLdb()
		import pandas as pd
		from sqlalchemy import create_engine

		df = pd.read_csv(csv_path, sep = ',')

		engine = create_engine(f'mysql://{user_login}:{passw}@localhost/{datab}')
		
		with engine.begin() as connection:
			df.to_sql(name = new_name, con = connection, if_exists = 'replace', index = False)


def main():

	#only have to debug add a new user and delete a user 

	global current_window,datab
	global table
	
	try:


		if current_window == 0:
			
			Show_Main_Menu(current_window)

	
			try:	
			
				inp = int(input("Enter the choice you want: "))

			except ValueError:

				print("Enter the index of the option you want to choose not a string")

				time.sleep(2)

			if inp == 0:
				login()
				time.sleep(2)

			try:


				if inp == 1:
					get_db()
					time.sleep(2)

				elif inp == 2:
					create_db()
					time.sleep(2)

				elif inp == 3:
					print("The current databases are:-")

					mycursor.execute("show databases;")

					databases = []

					db_list = mycursor.fetchall()

					for y in range(len(db_list)):
						if db_list[y] in databases:
							pass
						else:
							str = ''.join(db_list[y])
							databases.append(str)

					for i in range(len(databases)):
						print(f"[{i + 1}] {databases[i]}")

					db = int(input("Enter the databases you want: "))

					sql = f"use {databases[db-1]}"
					mycursor.execute(sql)

					print(f"Using database {databases[db-1]}")

					datab = databases[db - 1]

					current_window = 1
					time.sleep(2)

				elif inp == 4:
					add_new_user()
					time.sleep(2)

				elif inp == 5:
					delete_user()
					time.sleep(2)

				elif inp == 6:
					update_password()
					time.sleep(2)

				elif inp == 7:
					login()
					time.sleep(2)

				elif inp == 99:
					print("Bye !!")
					sys.exit()
			
			except NameError:
				print("Please login in a database first")
				time.sleep(2)		
		
		if current_window == 1:

			Show_Main_Menu(current_window)

	
			try:	
			
				inp = int(input("Enter the choice you want: "))

			except ValueError:

				print("Enter the index of the option you want to choose not a string")

				time.sleep(2)

			if inp == 0:
				Table.show_available_tables()
				time.sleep(2)

			if inp == 5:
					# load a new table from csv
					Table.load_table(table)
					print("Table Created")
					time.sleep(2)
			
			if inp == 99:
					current_window = 0
		
				
			if inp == 1:

				if len(table) == 0:
				
					print("No table chosen if you want to perform operations on table please ")
					print("go through show available tables and set a table")
					time.sleep(2)

				elif len(table) != 0:

					Table.See_full_table(table)
					time.sleep(2)

			if inp == 2:
				# see the table contents
				if len(table) == 0:
				
					print("No table chosen if you want to perform operations on table please ")
					print("go through show available tables and set a table")
					time.sleep(2)

				elif len(table) != 0:
					
					Table.Select_Column(table)
					time.sleep(2)

			if inp == 3:
				# alter table
				if len(table) == 0:
				
					print("No table chosen if you want to perform operations on table please ")
					print("go through show available tables and set a table")
					time.sleep(2)

				elif len(table) != 0:
					
					Table.alter_table(table)
					time.sleep(2)

			if inp == 4:
				# desc table
				if len(table) == 0:
				
					print("No table chosen if you want to perform operations on table please ")
					print("go through show available tables and set a table")
					time.sleep(2)

				elif len(table) != 0:
					Table.desc_table(table)
					time.sleep(2)

			

			if inp == 6:
				# make a bar graph of two columns from a single table
				if len(table) == 0:
				
					print("No table chosen if you want to perform operations on table please ")
					print("go through show available tables and set a table")
					time.sleep(2)

				elif len(table) != 0:
					Table.bar_graph(table)
					time.sleep(2)

	
	except (ValueError ,UnboundLocalError) as e:
		print("Invalid value please try again!!")

if __name__ == '__main__':

	while True:
		main()

