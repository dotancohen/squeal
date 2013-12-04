#!/usr/bin/python2

import MySQLdb

host = 'localhost'
username = 'root'
password = 'brunoMysql42' # I don't mind this password showing up in Github!
database = 'phpfox'



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
	global host, username, password, database

	conn = MySQLdb.connect(host=host, user=username, passwd=password, db=database)
	cursor = conn.cursor()

	tables = populate_tables(conn, cursor)

	"""
	print(len(tables))

	for i in range(10):
		print("%s: %s" % (tables[i].name, tables[i].records ))
	# numrows = int(cursor.rowcount)
	"""


	tables_sorted_size = sorted(tables, key=lambda k: k.records)

	print("\nShow 3 largest tables")
	for i in range(3):
		print("%s: %s" % (tables_sorted_size[-1-i].name, tables_sorted_size[-1-i].records,))

	print("\nShow 3 smallest tables")
	for i in range(3):
		print("%s: %s" % (tables_sorted_size[i].name, tables_sorted_size[i].records,))



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



def show_tables(envm, tables, order='alph', limit=None):

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



if __name__ == '__main__':
	main()
