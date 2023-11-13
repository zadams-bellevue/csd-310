#!/usr/bin/env python3

"""Assignment 5.3"""

from pymongo import MongoClient

URL = "mongodb+srv://admin:admin@cluster0.uvpueeb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URL)
db = client.pytech

if __name__ == "__main__":
	new_students = [
		{
			"student_id": 1007,
			"first_name": "Kaladin",
			"last_name": "Stormblessed",
		},
		{
			"student_id": 1008,
			"first_name": "Jasnah",
			"last_name": "Kholin",
		},
		{
			"student_id": 1009,
			"first_name": "Shallan",
			"last_name": "Davar",
		},
	]

	for student in new_students:
		new_id = db.students.insert_one(student).inserted_id
		print(f"Inserted student record {student['first_name']} {student['last_name']} into the students collection with document_id {new_id}")
