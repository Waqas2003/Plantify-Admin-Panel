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
                private_key = private_key[0]  
            
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
        
    def add_plant(self, data):
        return self.db.collection('Plants').add(data)
    
    def delete_plant(self, plant_id):
        self.db.collection('Plants').document(plant_id).delete()    
    
    # Users Collection
    def get_all_users(self):
        return self.db.collection('Users').stream()
        
    def get_user(self, user_email):
        return self.db.collection('Users').document(user_email).get()
    
    def update_user(self,user_email,data):
        self.db.collection('Users').document(user_email).update(data)
        
    def add_user(self, data):
        return self.db.collection('Users').add(data)
    
    def delete_user(self, user_email):
        self.db.collection('Users').document(user_email).delete()
    
    def block_user(self, user_email):
        self.db.collection('Users').document(user_email).update({'status': 'blocked'})
    
    
    
    # Users_Plants Collection
    def get_all_user_plants(self):
        return self.db.collection('Users_Plants').stream()
    
    def get_user_plants(self, user_email):
        return self.db.collection('Users_Plants').where('userEmail', '==', user_email).stream()
    
    def add_user_plants(self, data):
        user_email = data.get('userEmail') 
        if user_email:
            return self.db.collection('Users_Plants').document(user_email).set(data)

    def update_user_plants(self,user_email,data):
        self.db.collection('Users_Plants').document(user_email).update(data)
    
    def delete_user_plants(self, user_email):
        self.db.collection('Users_Plants').document(user_email).delete()
    
    # Communities Collection
    def get_all_communities(self):
        return self.db.collection('Communities').stream()
    
    def get_community(self, community_id):
        return self.db.collection('Communities').document(community_id).get()
    
    def update_community(self, community_id, data):
        self.db.collection('Communities').document(community_id).update(data)
        
    def add_community(self, data):
        return self.db.collection('Communities').add(data)
    
    def delete_community(self, community_id):
        self.db.collection('Communities').document(community_id).delete()    

    def block_community(self, community_id):
        self.db.collection('Communities').document(community_id).update({'status': 'blocked'})

    
    # Class_Labels Collection
    def get_all_diseases(self):
        return self.db.collection('Class_Labels').stream()
    
    def get_disease(self, disease_id):
        return self.db.collection('Class_Labels').document(disease_id).get()
    
    def update_disease(self, disease_id, data):
        self.db.collection('Class_Labels').document(disease_id).update(data)
        
    def add_disease(self, data):
        disease_name = data.get('disease')
        return self.db.collection('Class_Labels').document(disease_name).set(data)
    
    def delete_disease(self, disease_id):
        self.db.collection('Class_Labels').document(disease_id).delete()    

    