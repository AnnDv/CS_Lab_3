# create_key.py

import os
from pathlib import Path
from secrets import token_bytes

from bson import json_util
from bson.binary import STANDARD
from bson.codec_options import CodecOptions
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts


# Generate a secure 96-byte secret key:
key_bytes = token_bytes(96)


# Configure a single, local KMS provider, with the saved key:
kms_providers = {"local": {"key": key_bytes}}
csfle_opts = AutoEncryptionOpts(
   kms_providers=kms_providers, key_vault_namespace="lab7.__keystore"
)

# Connect to MongoDB with the key information generated above:
with MongoClient("mongodb+srv://security:secrip003@cluster0.quxiy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", auto_encryption_opts=csfle_opts) as client:
   print("Resetting demo database & keystore ...")
   client.drop_database("lab7")

   # Create a ClientEncryption object to create the data key below:
   client_encryption = ClientEncryption(
      kms_providers,
      "lab7.__keystore",
      client,
      CodecOptions(uuid_representation=STANDARD),
   )

   print("Creating key in MongoDB ...")
   key_id = client_encryption.create_data_key("local", key_alt_names=["example"])



Path("key_bytes.bin").write_bytes(key_bytes)



schema = {
  "bsonType": "object",
  "properties": {
      "idnp": {
         "encrypt": {
            "bsonType": "string",
            # Change to "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic" in order to filter by idnp value:
            "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
            "keyId": [key_id],  # Reference the key
         }
      },
   },
}

json_schema = json_util.dumps(
   schema, json_options=json_util.CANONICAL_JSON_OPTIONS, indent=2
)
Path("json_schema.json").write_text(json_schema)