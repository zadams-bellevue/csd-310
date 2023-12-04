#!/usr/bin/env python3

"""Assignment 8.2"""

from os import getenv
import mysql.connector
from mysql.connector import errorcode

DB = None
try:
	db_config = {
		"user": getenv("MYSQL_USER"),
		"password": getenv("MYSQL_PASS"),
		"host": getenv("MYSQL_HOST"),
		"database": "pysports",
		"raise_on_warnings": True,
	}
	DB = mysql.connector.connect(**db_config)

	print(f"Connected to database {db_config['database']} on host {db_config['host']} with user {db_config['user']}")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Database error: Access denied")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database error: pysports database does not exist")
	else:
		print(err)
finally:
	if DB is not None:
		DB.close()
