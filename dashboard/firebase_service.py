# dashboard/firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
import os

class FirebaseRepository:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseRepository, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        if not firebase_admin._apps:
            # Get private key properly from settings
            private_key = settings.FIREBASE_PRIVATE_KEY
            if isinstance(private_key, tuple):
                private_key = private_key[0]  # Take first element if it's a tuple
            
            # Ensure proper newline formatting
            private_key = private_key.replace('\\n', '\n')
            
            firebase_creds = {
                "type": settings.FIREBASE_TYPE,
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
                "private_key": private_key,
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "client_id": settings.FIREBASE_CLIENT_ID,
                "auth_uri": settings.FIREBASE_AUTH_URI,
                "token_uri": settings.FIREBASE_TOKEN_URI,
                "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_CERT_URL,
                "client_x509_cert_url": settings.FIREBASE_CLIENT_CERT_URL
            }
            
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    # ... rest of your FirebaseRepository methods ...
    
    # Plants Collection
    def get_all_plants(self):
        return self.db.collection('Plants').stream()
    
    def get_plant(self, plant_id):
        return self.db.collection('Plants').document(plant_id).get()
    
    def update_plant(self, plant_id, data):
        self.db.collection('Plants').document(plant_id).update(data)
    
    # Users Collection
    def get_all_users(self):
        return self.db.collection('Users').stream()
    
    def get_user(self, user_email):
        return self.db.collection('Users').document(user_email).get()
    
    # Users_Plants Collection
    def get_all_user_plants(self):
        return self.db.collection('Users_Plants').stream()
    
    def get_user_plants(self, user_email):
        return self.db.collection('Users_Plants').where('userEmail', '==', user_email).stream()
    
    # Communities Collection
    def get_all_communities(self):
        return self.db.collection('Communities').stream()
    
    def get_community(self, community_id):
        return self.db.collection('Communities').document(community_id).get()
    
    # Class_Labels Collection
    def get_all_diseases(self):
        return self.db.collection('Class_Labels').stream()
    
    def get_disease(self, disease_id):
        return self.db.collection('Class_Labels').document(disease_id).get()