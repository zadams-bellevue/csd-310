#!/usr/bin/env python3

"""Assignment 9.2"""

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

	CURSOR = DB.cursor(named_tuple=True)
	print("-- DISPLAYING PLAYER RECORDS --")
	CURSOR.execute("SELECT p.player_id, p.first_name, p.last_name, t.team_name FROM player p INNER JOIN team t ON t.team_id = p.team_id")
	for row in CURSOR:
		print(
			f"Player ID: {row.player_id}\n"
			+ f"First Name: {row.first_name}\n"
			+ f"Last Name: {row.last_name}\n"
			+ f"Team Name: {row.team_name}\n"
		)
	CURSOR.close()
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
