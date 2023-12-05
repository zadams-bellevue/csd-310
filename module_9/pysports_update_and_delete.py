#!/usr/bin/env python3

"""Assignment 9.3"""

from os import getenv
import mysql.connector
from mysql.connector import errorcode, MySQLConnection

def display_players(db: MySQLConnection) -> None:
	"""Run a query and print players with their teams"""
	cursor = db.cursor(named_tuple=True)
	cursor.execute("""
		SELECT p.player_id, p.first_name, p.last_name, t.team_name
		FROM player p
		INNER JOIN team t ON t.team_id = p.team_id
		ORDER BY p.player_id ASC
	""")
	for row in cursor:
		print(
			f"Player ID: {row.player_id}\n"
			+ f"First Name: {row.first_name}\n"
			+ f"Last Name: {row.last_name}\n"
			+ f"Team Name: {row.team_name}\n"
		)
	cursor.close()

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
	CURSOR.execute("INSERT INTO player (first_name, last_name, team_id) VALUES ('Smeagol', 'Shire Folk', 1)")
	CURSOR.close()
	print("-- DISPLAYING PLAYERS AFTER INSERT --")
	display_players(DB)

	CURSOR = DB.cursor(named_tuple=True)
	CURSOR.execute("UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = 'Smeagol'")
	CURSOR.close()
	print("-- DISPLAYING PLAYERS AFTER UPDATE --")
	display_players(DB)

	CURSOR = DB.cursor(named_tuple=True)
	CURSOR.execute("DELETE FROM player WHERE first_name = 'Gollum'")
	CURSOR.close()
	print("-- DISPLAYING PLAYERS AFTER DELETE --")
	display_players(DB)

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
