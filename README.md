SQueaL
======

Database explorer with a focus on breadth, not depth.



FAQ
===

Why do we need yet another database explorer?
---------------------------------------------

All of today's well-developed database explorers make it easy to do the things that are already easy to do in SQL, namely to dig down to the details of a single table's rows and column configuration. SQueaL is designed for a different task: to show the breadth of a database structure, not the depth. With SQueaL one can see which tables were the last to update, which update the most often, which data is typical of each table, and other tasks to get a 'feeling' for the database.



Why on Earth might someone need such a silly tool?
--------------------------------------------------

SQueaL is useful for developers new to an existing project to become acquainted with the database being used. We already have profiling tools for code, but nothing currently useful for large database examination.



Why the silly name?
-------------------

The name 'SQueaL' is bookended by the letters SQL, symbolically it shows you what is 'inside' the SQL. Also, the verb 'to squeal' means 'to snitch' or 'to inform', implying that this application reveals information which is otherwise not so easily accessible and concise.



What specific information does SQueaL provide?
----------------------------------------------

### Tables

* Table names
* Number of records
* Creation time, size on disk
* Estimate: Frequency of inserts, updates, and deletes
* Sort on metrics

### Records

* Column names and types
* Average, maximum, and minimum size of column values, and standard deviation
* Typical or representative values for each column
* View random records
* Sort on metrics



What dependencies does SQueaL have?
-----------------------------------

Just the Python2 core library and the Python MySQL connector. Try one of the following:

### Ubuntu

    $ sudo aptitude install python python-mysqldb
    $ sudo aptitude install python python-mysql.connector

### RHEL / CentOS

	# yum install mysql-connector-python



Why no Python3 support?
-----------------------

There is no MySQL connector for Python3 yet.



Who to contact for feature requests, bugs, patches, praise, or blame?
----------------------------------------------------------------

### Squeal project homepage (feature requests, bugs, and patches)

http://github.com/dotancohen/squeal

### Squeal author and maintainer (praise and blame)

Dotan Cohen  
http://dotancohen.com  
You can find my email address and other contact information in your favorite search engine!
