#!/usr/bin/env python3

"""WhatABook Final Assignment"""

from os import getenv
import mysql.connector
from mysql.connector import errorcode, MySQLConnection

def main_menu(c: MySQLConnection) -> None:
	"""Print and handle the main menu"""
	while True:
		match input(
			"View Books (B)\n"
			+ "View Store Locations (S)\n"
			+ "My Account (A)\n"
			+ "Quit (Q)\n"
		).lower():
			case "b":
				print_books(c)
			case "s":
				print_locations(c)
			case "a":
				account_menu(c)
			case "q":
				return

def print_books(c: MySQLConnection, user_id: int|None = None, exclude_wishlist: bool = True) -> None:
	"""Print books 5 at a time. Optionally print only books from a wishlist, or all books except a wishlist."""
	offset = 0
	limit = 5
	while True:
		# Python's prepared statement support appears to just prepare a new statement unless the statement is the same
		# as the previously executed statement, so there's no need to prepare the statement beforehand.
		# Unfortunately using a cursor with prepared statements isn't working for me, and I don't have the time to debug it
		# cursor = c.cursor(prepared=True, named_tuple=True)
		cursor = c.cursor(named_tuple=True)
		if user_id is None:
			cursor.execute("SELECT * FROM book ORDER BY book_id DESC LIMIT %s, %s", [offset, limit])
		else:
			include_or_exclude = "NOT IN" if exclude_wishlist else "IN"
			# Using string interpolation for SQL queries is usually a bad idea, but here we're setting the string to
			# a specific value and it doesn't include user input, so it's safe.
			cursor.execute(f"""
				SELECT *
				FROM book b
				WHERE b.book_id {include_or_exclude} (
					SELECT b2.book_id
					FROM book b2
					INNER JOIN wishlist w2 ON w2.book_id = b2.book_id
					WHERE w2.user_id = %s
				) ORDER BY b.book_name ASC LIMIT %s, %s""", [user_id, offset, limit])
		offset += limit
		exists = False
		for book in cursor:
			exists = True
			print(
				f"Book ID: {book.book_id}\n"
				+ f"Author: {book.author}\n"
				+ f"Title: {book.book_name}\n"
				+ f"Details: {book.details}\n"
			)
		cursor.close()
		if not exists:
			print("No more books!\n")
			break
		while True:
			match input("Continue [c]; Stop [q]: ").lower():
				case "c":
					break
				case "q":
					print()
					return

def print_locations(c: MySQLConnection) -> None:
	"""Print store locations"""
	cursor = c.cursor(named_tuple=True)
	cursor.execute("SELECT * FROM store")
	print("Store Locations:")
	for store in cursor:
		print(f"{store.locale}")
	cursor.close()
	print()

def account_menu(c: MySQLConnection) -> None:
	"""User account menu"""
	cursor = c.cursor(named_tuple=True)

	while True:
		account_id_s = input("Enter your account ID: ")
		try:
			account_id = int(account_id_s)
			cursor.execute("SELECT * FROM user WHERE user_id = %s", [account_id])
			user_account = cursor.fetchone()
			if user_account is None:
				print("Invalid account ID")
				continue
			break
		except ValueError:
			print("Invalid account ID")
	cursor.close()

	print(f"{user_account.first_name} {user_account.last_name}'s Account:")

	while True:
		match input(
			"Manage Wishlist (W)\n"
			+ "Main Menu (M)\n"
		).lower():
			case "w":
				wishlist_menu(c, user_account.user_id)
			case "m":
				return

def wishlist_menu(c: MySQLConnection, user_id: int) -> None:
	"""Wishlist menu"""
	while True:
		match input(
			"Show Wishlist (W)\n"
			+ "Add to Wishlist (A)\n"
			+ "User Account Menu (U)\n"
		).lower():
			case "w":
				print_books(c, user_id, False)
			case "a":
				print("\nAvailable books:\n")
				print_books(c, user_id)
				while True:
					match input("Book ID (or cancel (C)): ").lower():
						case "c":
							break
						case book_id_s:
							try:
								book_id = int(book_id_s)
							except ValueError:
								print("Invalid book ID")
								continue
							cursor = c.cursor(named_tuple=True)
							try:
								cursor.execute("INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)", [user_id, book_id])
								c.commit()
							except mysql.connector.Error as e:
								if e.errno == errorcode.ER_DUP_ENTRY:
									print("That book is already on your wishlist!")
									continue
								if e.errno in (errorcode.ER_NO_REFERENCED_ROW, errorcode.ER_NO_REFERENCED_ROW_2):
									print("Invalid book ID")
									continue
							finally:
								cursor.close()

							cursor = c.cursor(named_tuple=True)
							cursor.execute("SELECT book_name FROM book WHERE book_id = %s", [book_id])
							book_name = cursor.fetchone().book_name
							cursor.close()
							print(f"{book_name} has been added to your wishlist!")
							break
			case "u":
				return

if __name__ == "__main__":
	CONNECTION = None
	try:
		db_config = {
			"user": getenv("MYSQL_USER"),
			"password": getenv("MYSQL_PASS"),
			"host": getenv("MYSQL_HOST"),
			"database": "whatabook",
			"raise_on_warnings": True,
		}
		CONNECTION = mysql.connector.connect(**db_config)
		main_menu(CONNECTION)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Database error: Access denied")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database error: whatabook database does not exist")
		else:
			print(err)
	finally:
		if CONNECTION is not None:
			CONNECTION.close()
