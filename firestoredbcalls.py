from google.cloud.firestore_v1.base_query import FieldFilter
import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreDBCalls:
    def __init__(self): 
        cred = credentials.Certificate("cert.json") # Replace with your key file path
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_user(self, username, password, email,role):
        doc_ref = self.db.collection('user').document()
        doc_ref.set({
            'username': username,
            'password': password,
            'Email': email,
            'role': role
        })
