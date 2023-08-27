from firebase_admin import credentials, firestore_async
from dotenv import load_dotenv
import firebase_admin
import os
import json
import os

load_dotenv()

RAW_FIREBASE_CONFIG = os.getenv("FIREBASE")
PARSED_FIREBASE_CONFIG = json.loads(RAW_FIREBASE_CONFIG)

cred = credentials.Certificate(PARSED_FIREBASE_CONFIG)

app = firebase_admin.initialize_app(cred)

db = firestore_async.client()