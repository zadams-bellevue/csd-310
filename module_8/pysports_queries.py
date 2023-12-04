#!/usr/bin/env python3

"""Assignment 8.3"""

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
	print("-- DISPLAYING TEAM RECORDS --")
	CURSOR.execute("SELECT team_id, team_name, mascot FROM team")
	for team in CURSOR:
		print(
			f"Team ID: {team.team_id}\n"
			+ f"Team Name: {team.team_name}\n"
			+ f"Mascot: {team.mascot}\n"
		)
	CURSOR.close()

	CURSOR = DB.cursor(named_tuple=True)
	print("\n-- DISPLAYING PLAYER RECORDS --")
	CURSOR.execute("SELECT player_id, first_name, last_name, team_id FROM player")
	for player in CURSOR:
		print(
			f"Player ID: {player.player_id}\n"
			+ f"First Name: {player.first_name}\n"
			+ f"Last Name: {player.last_name}\n"
			+ f"Team ID: {player.team_id}\n"
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
