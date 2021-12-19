import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from pymongo.errors import EncryptionError
from bson import json_util


# Create data for database
data = {"_id" : ['1231', '5213', '4896', '12379', '7891', '4894', '6841',
						'7889', '1238', '6668'],
		"full_name" : ['Karli Gomez', 'Andrew Allison', 'Kiley Klein', 'Elijah Lutz',
 						'Jefferson Carrillo', 'Konnor Sheppard', 'Maren Estrada', 'Brooke Villa', 'Asia Williams',
 						 'Edwin Anthony'],
 		"idnp" : ['15603712290', '59067243312', '78105439337', '66111370666', '32312366054', '88565467430', '71844494498' ,
 				 '28804766735', '17068006006', '31750007018']}

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

# Add a new document to the "people" collection, and then read it back out
# to demonstrate that the idnp field is automatically decrypted by PyMongo:
with MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.quxiy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", auto_encryption_opts=csfle_opts) as client:
	client.lab7.people.delete_many({})

	for index in range(len(data['full_name'])):
		client.lab7.people.insert_one({
				"_id": data['_id'][index],
   			"full_name": data['full_name'][index],
   			"idnp": data['idnp'][index],
			})

