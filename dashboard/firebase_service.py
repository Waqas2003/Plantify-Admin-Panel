# dashboard/firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
import os
from datetime import datetime
import re

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
    
    def update_user(self, user_email, data):
        self.db.collection('Users').document(user_email).update(data)
        
    def add_user(self, data):
        # Using email as document ID
        user_ref = self.db.collection('Users').document(data['email'])
        user_ref.set(data)
        return user_ref
    
    def delete_user(self, user_email):
        self.db.collection('Users').document(user_email).delete()
    
    def _escape_email(self, email):
        """Escape email for Firestore field paths"""
        # Replace special characters with Firestore-safe equivalents
        return re.sub(r'[.@]', lambda x: {'@': '_at_', '.': '_dot_'}[x.group()], email)

    def block_user(self, user_email):
        try:
            escaped_email = self._escape_email(user_email)
            batch = self.db.batch()
            user_ref = self.db.collection('Users').document(user_email)
            
            # 1. Remove from all communities
            communities = self.db.collection('Communities')\
                               .where(f'members.{escaped_email}', '==', True)\
                               .stream()
            
            for community in communities:
                comm_ref = self.db.collection('Communities').document(community.id)
                batch.update(comm_ref, {
                    f'members.{escaped_email}': firestore.DELETE_FIELD,
                    f'bannedUsers.{escaped_email}': True
                })
            
            # 2. Update user status
            batch.update(user_ref, {
                'status': 'blocked',
                'lastBlockedAt': datetime.now().isoformat()
            })
            
            batch.commit()
            return True
            
        except Exception as e:
            print(f"Error blocking user: {str(e)}")
            raise e

    def unblock_user(self, user_email):
        self.db.collection('Users').document(user_email).update({
            'status': 'active',
            'lastUnblockedAt': datetime.now().isoformat()
        })
        
    # ========== COMMUNITY METHODS ==========
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

    def join_community(self, user_email, community_id):
        # Check if user exists and is not blocked
        user = self.get_user(user_email)
        if not user.exists:
            raise Exception("User does not exist")
        if user.to_dict().get('status') == 'blocked':
            raise Exception("User is blocked and cannot join communities")
        
        # Check if community exists and is not blocked
        community = self.get_community(community_id)
        if not community.exists:
            raise Exception("Community does not exist")
        if community.to_dict().get('status') == 'blocked':
            raise Exception("Community is blocked and cannot be joined")
        
        # Check if user is banned from this community
        banned_ref = self.db.collection('Communities').document(community_id).collection('BannedUsers').document(user_email).get()
        if banned_ref.exists:
            raise Exception("User is banned from this community")
        
        # Add to community members subcollection
        self.db.collection('Communities').document(community_id).collection('Members').document(user_email).set({
            'joinedAt': datetime.now().isoformat(),
            'status': 'active'
        })
        
        # Update user's joined communities
        self.db.collection('Users').document(user_email).update({
            f'joined_communities.{community_id}': True
        })
    
    def get_community_members(self, community_id):
        members = []
        members_ref = self.db.collection('Communities').document(community_id).collection('Members').stream()
        for member in members_ref:
            if member.id != 'placeholder':
                members.append(member.id)
        return members
    
    def get_banned_users(self, community_id):
        banned_users = []
        banned_ref = self.db.collection('Communities').document(community_id).collection('BannedUsers').stream()
        for user in banned_ref:
            if user.id != 'placeholder':
                banned_users.append(user.id)
        return banned_users

    
    
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

    