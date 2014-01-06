#!/usr/bin/python2

import MySQLdb
import random
import sys
import time

from pprint import pprint

host = 'localhost'
username = 'root'
password = 'brunoMysql42' # I don't mind this password showing up in Github!
database = 'phpfox'



squeal_version = '0.2 Beta'
prompt = '>> '


class Column(object):

	def __init__(self, field, typ, null, key, default, extra):

		# Using name typ instead of type due to Python keyword

		self.field = field
		self.typ = typ
		self.null = null
		self.key = key
		self.default = default
		self.extra = extra



	def __str__(self):

		output = "field: %s\n" % (self.field,)
		output+= "typ: %s\n" % (self.typ,)
		output+= "null: %s\n" % (self.null,)
		output+= "key: %s\n" % (self.key,)
		output+= "default: %s\n" % (self.default,)
		output+= "extra: %s\n" % (self.extra,)

		return output



class Table(object):

	def __init__(self, name, records=None):

		self.name = name
		self.records = records

		self.engine = None
		self.columns = []

		# Note that this is available only when an 'insert' field is identified.
		self.insert_frequency = None # Per day
		# Note that this is available only when an 'update' field is identified.
		self.update_frequency = None # Per day.
		# Note that this is available only when a 'delete' field is identified.
		self.delete_frequency = None # Per day.



	def add_column(self, column):

		self.columns.append(column)
		return True



	def show_columns(self):

		for c in self.columns:
			print(c)

		return True



def main():

	global prompt, squeal_version, host, username, password, database

	print("\nWelcome to Squeal version %s!" % (squeal_version, ))

	conn = MySQLdb.connect(host=host, user=username, passwd=password, db=database)
	cursor = conn.cursor()
	all_tables = populate_tables(conn, cursor)

	menu_title = "20 largest tables"
	menu_tables = sort_tables(all_tables, 'desc')
	show_menu = True
	tables_to_show = 20
	records_to_show = 10

	while True:

		if show_menu:
			output_title(menu_title)
			for i,t in enumerate(menu_tables[:tables_to_show]):
				print(" %s: %s  (%s)" % (i+1, t.name, t.records,))

			output_title("Please select an operation:", 1)
			print("   #. Enter a table number to see details.")
			print("   A. Show all tables sorted by size decending")
			print("   B. Show all tables sorted by size ascending")
			print("   C. Show all tables sorted alphabetically")
			#print("   N. Show next tables")
			print(" S #. Set number of tables to show in summary")
			print(" R #. Set number of records to show in tables")
			print("   -. Exit")

		else:
			show_menu = True

		user_input = raw_input(prompt).split(' ')
		operation = user_input[0]

		if 1<len(user_input):
			if not user_input[1].isdigit():
				print("\nQuantity must be a number!")
				show_menu = False
				continue
			quantity = int(user_input[1])
		else:
			quantity = None


		# We have input, now do something with it!

		if operation.isdigit():
			operation = int(operation)

			if 0<operation and operation<=len(menu_tables):
				show_table_details(conn, cursor, prompt, menu_tables[operation-1], records_to_show)

			else:
				print("\nInput out of range!")
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

			elif operation == 's':
				show_menu = False
				if quantity==None:
					print("\nNeed quantity!")
					continue

				tables_to_show = quantity
				print("\nTables to show set as %i" % (tables_to_show,) )

			elif operation == 'r':
				show_menu = False
				if quantity==None:
					print("\nNeed quantity!")
					continue

				records_to_show = quantity
				print("\nRecords to show set as %i" % (records_to_show,) )

			else:
				print("\nInvalid input!")
				show_menu = False

	return True



def output_title(text, leading_newlines=3):

	if leading_newlines<1:
		raise IndexError

	print('\n'*(leading_newlines-1))
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
		sql = "SELECT count(*) FROM `%s`" % (t, )
		cursor.execute(sql)
		conn.commit()
		records = cursor.fetchone()[0] # Fetch first column of first row

		new_table = Table(t, records)

		sql = "DESCRIBE `%s`" % (t, )
		cursor.execute(sql)
		conn.commit()
		for row in cursor.fetchall():
			new_table.add_column(Column(row[0], row[1], row[2], row[3], row[4], row[5]))

		tables.append(new_table)
		new_table = None

	return tables



def sort_tables(tables, order='alph'):

	legal_orders = ['alph', 'asc', 'desc']

	if not order in legal_orders:
		return False

	if order=='alph':
		return sorted(tables, key=lambda k: k.name)

	sorted_size = sorted(tables, key=lambda k: k.records)

	if order=='asc':
		return sorted_size

	if order=='desc':
		return sorted_size[::-1]

	return True



def show_table_details(conn, cursor, prompt, table, random_values_to_show=10):

	output_title("Showing table %s" % (table.name,))

	# Describe table

	output_title("Describe table", 1)
	sql = "DESCRIBE `%s`" % (table.name,)
	output_table_from_sql(conn, cursor, sql)


	# Attempt to get primary key

	try:
		primary_key = [c.field for c in table.columns if c.key=='PRI'][0]
	except (TypeError, IndexError) as e:
		primary_key = False


	# Some random records

	output_title("Some random records", 1)
	if primary_key==False:
		sql = "SELECT * FROM `%s` ORDER BY RAND() LIMIT %s" % (table.name, random_values_to_show,)
		output_table_from_sql(conn, cursor, sql)

	else:
		random_keys = "','".join([str(random.randint(0,table.records)) for i in range(random_values_to_show*5)])
		random_keys = "'" + random_keys + "'"
		sql = "SELECT * FROM `%s` WHERE `%s` IN (%s) LIMIT %s" % (table.name, primary_key, random_keys, random_values_to_show)
		output_table_from_sql(conn, cursor, sql)


	# Complete last record

	if primary_key==False:
		output_title("No primary key, so cannot output last record!", 1)
	else:
		output_title("Complete last record", 1)
		sql = "SELECT * FROM `%s` ORDER BY `%s` DESC LIMIT 1" % (table.name, primary_key,)
		output_table_from_sql(conn, cursor, sql, vertical_format=True)

	return True



def output_table_from_sql(conn, cursor, sql, data=None, vertical_format=False):

	# TODO: Make this a configuration item, not hard-coded
	line_length = 115

	start = time.time()
	cursor.execute(sql, data)
	end = time.time()
	conn.commit()
	results = cursor.fetchall()

	if 0==len(results):
		print("No records returned!")
		return True

	if vertical_format:

		longest_description = 0
		for i in range(len(cursor.description)):
			longest_description = max(longest_description, len(cursor.description[i][0]))

		for i in range(len(cursor.description)):
			print("%s: %s" % (cursor.description[i][0].rjust(longest_description, ' '), results[0][i],))

	else:
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

		print(separator[:line_length])
		print((tavnit % tuple(columns))[:line_length])

		print(separator[:line_length])
		for row in results:
			print((tavnit % row)[:line_length])

		print(separator[:line_length])
		print("Time: %s" % (round(end-start, 4),))


	return True



if __name__ == '__main__':
	main()
