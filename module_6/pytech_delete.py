#!/usr/bin/env python3

"""Assignment 6.3"""

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

	new_id = db.students.insert_one({
		"student_id": 1010,
		"first_name": "Dalinar",
		"last_name": "Kholin",
	}).inserted_id
	print(f"Inserted student record into the students collection with document_id {new_id}")
	print("-- DISPLAYING STUDENT TEST DOC --")
	print_student(db.students.find_one({"student_id": 1010}))

	db.students.delete_one({"student_id": 1010})

	print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
	for s in db.students.find({}):
		print_student(s)
