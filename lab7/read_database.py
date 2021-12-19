import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from pymongo.errors import EncryptionError
from bson import json_util


def is_correct_log_in(username_x, password_x):
	
	if username_x == 'security' and password_x == 'seccrip003':
		return True

	return False

def read_data(username_x, password_x):

	if username_x == 'security' and password_x == 'seccrip003':
		# Load the master key from 'key_bytes.bin':
		key_bin = Path("key_bytes.bin").read_bytes()

		# Load the 'person' schema from "json_schema.json":
		collection_schema = json_util.loads(Path("json_schema.json").read_text())


		# Configure a single, local KMS provider, with the saved key:
		kms_providers = {"local": {"key": key_bin}}

		# Create a configuration for PyMongo, specifying the local master key,
		# the collection used for storing key data, and the json schema specifying
		# field encryption:
		csfle_opts = AutoEncryptionOpts(
		   kms_providers,
		   "lab7.__keystore",
		   schema_map={"lab7.people": collection_schema},
		)

		username = 'security'
		password = 'seccrip003'

		with MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.quxiy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", auto_encryption_opts=csfle_opts) as client:
			#print("Encrypted find() results: ")
			#print(client.lab7.people.find_one())
		
			post_count = client.lab7.people.count_documents({})
		
			# Decrypted results
			list_persons = []
			results = client.lab7.people.find({})
			for result in results:
				list_persons.append(result)

		return 	post_count, list_persons		