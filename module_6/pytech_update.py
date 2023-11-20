#!/usr/bin/env python3

"""Assignment 6.2"""

from typing import TypedDict
from pymongo import MongoClient

URL = "mongodb+srv://admin:admin@cluster0.uvpueeb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URL)
db = client.pytech

StudentType = TypedDict("StudentType", {"student_id": str, "first_name": str, "last_name": str})
def print_student(student: StudentType) -> None:
	"""Print a student to stdout."""
	print(
		f"Student ID: {student['student_id']}\n"
		+ f"First Name: {student['first_name']}\n"
		+ f"Last Name: {student['last_name']}\n"
	)

if __name__ == "__main__":
	print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
	for s in db.students.find({}):
		print_student(s)

	db.students.update_one({"student_id": 1007}, {"$set": {"last_name": "Son of Tanavast"}})
	print("\n-- DISPLAYING STUDENT DOCUMENT 1007 --")
	print_student(db.students.find_one({"student_id": 1007}))
