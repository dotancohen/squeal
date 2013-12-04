#!/usr/bin/python2

import MySQLdb
import sys
import time

from pprint import pprint

host = 'localhost'
username = 'root'
password = 'brunoMysql42' # I don't mind this password showing up in Github!
database = 'phpfox'



squeal_version = '0.1'
prompt = '>> '



class Table(object):

	def __init__(self, name, records=None):

		self.name = name
		self.records = records

		self.engine = None

		# Note that this is available only when an 'insert' field is identified.
		self.insert_frequency = None # Per day
		# Note that this is available only when an 'update' field is identified.
		self.update_frequency = None # Per day.
		# Note that this is available only when a 'delete' field is identified.
		self.delete_frequency = None # Per day.



def main():

	global prompt, squeal_version, host, username, password, database

	print("\nWelcome to Squeal version %s!" % (squeal_version, ))

	conn = MySQLdb.connect(host=host, user=username, passwd=password, db=database)
	cursor = conn.cursor()
	all_tables = populate_tables(conn, cursor)

	menu_title = "20 largest tables"
	menu_tables = sort_tables(all_tables, 'desc', 20)
	show_menu = True

	while True:

		if show_menu:
			output_title(menu_title)
			i = 1
			for t in menu_tables:
				print("%s: %s (%s)" % (i, t.name, t.records,))
				i +=1

			print("\nPlease select an operation:")
			print("--------------------------")
			print(" #. Enter a table number to see details.")
			print(" A. Show all tables sorted by size decending")
			print(" B. Show all tables sorted by size ascending")
			print(" C. Show all tables sorted alphabetically")
			print(" -. Exit")

		else:
			show_menu = True

		operation = raw_input(prompt)

		if operation.isdigit():
			operation = int(operation)
			if 0<operation and operation<=len(menu_tables):
				show_table_details(conn, cursor, prompt, menu_tables[operation-1])
			else:
				print("\nInvalid input!")
				show_menu = False

		else:
			operation = operation.lower().strip()

			if operation == '-':
				sys.exit()
			elif operation == 'a':
				menu_title = "All tables sorted by size decending"
				menu_tables = sort_tables(all_tables, 'desc')
			elif operation == 'b':
				menu_title = "All tables sorted by size ascending"
				menu_tables = sort_tables(all_tables, 'asc')
			elif operation == 'c':
				menu_title = "All tables sorted alphabetically"
				menu_tables = sort_tables(all_tables, 'alph')
			else:
				print("\nInvalid input!")
				show_menu = False

	return True



def output_title(text):

	print('')
	print('   %s' % (text,))
	print('   ' + '-'*len(text))

	return True



def populate_tables(conn, cursor):

	table_names = []
	tables = []

	sql = "SHOW TABLES"
	cursor.execute(sql)
	conn.commit()

	for row in cursor.fetchall():
		table_names.append(row[0])

	for t in table_names:
		sql = "SELECT count(*) FROM %s" % (t, )
		cursor.execute(sql)
		conn.commit()
		records = cursor.fetchone()[0] # Fetch first column of first row
		tables.append(Table(t, records))

	"""
	# This is inaccurate on InnoDB!

	tables = []

	sql = "SELECT table_name,table_rows FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(db)s"
	cursor.execute(sql, {'db': database})
	conn.commit()

	for row in cursor.fetchall():
		tables.append(Table(row[0], row[1],))
	"""

	return tables



def sort_tables(tables, order='alph', limit=None):

	legal_orders = ['alph', 'asc', 'desc']

	if limit == None:
		limit = len(tables)

	if not order in legal_orders:
		return False

	if order=='alph':
		return sorted(tables, key=lambda k: k.name)

	sorted_size = sorted(tables, key=lambda k: k.records)

	if order=='asc':
		return sorted_size[:limit]

	if order=='desc':
		return sorted_size[::-1][:limit]

	"""
	print("\nShow 3 largest tables")
	for i in range(20):
		print("%s: %s" % (tables_sorted_size[-1-i].name, tables_sorted_size[-1-i].records,))

	print("\nShow 3 smallest tables")
	for i in range(3):
		print("%s: %s" % (tables_sorted_size[i].name, tables_sorted_size[i].records,))
	"""

	return True



def show_table_details(conn, cursor, prompt, table):

	output_title("Showing table %s" % (table.name,))

	sql = "DESCRIBE %s" % (table.name,)
	output_table_from_sql(conn, cursor, sql)

	return True



def output_table_from_sql(conn, cursor, sql, data=None):

	cursor.execute(sql, data)
	conn.commit()
	results = cursor.fetchall()

	widths = []
	columns = []
	tavnit = '|'
	separator = '+'

	for cd in cursor.description:
		widths.append(max(cd[2], len(cd[0])))
		columns.append(cd[0])

	for w in widths:
		tavnit += " %-"+"%ss |" % (w,)
		separator += '-'*w + '--+'

	# Now print!

	print(separator)
	print(tavnit % tuple(columns))

	print(separator)
	for row in results:
		print(tavnit % row)

	print(separator)


	return True



if __name__ == '__main__':
	main()



"""
	for row in results:
		print(row[0])


	for t in table_names:
		sql = "SELECT count(*) FROM %s" % (t, )
		cursor.execute(sql)
		conn.commit()
		records = cursor.fetchone()[0] # Fetch first column of first row
		tables.append(Table(t, records))
"""
