# dashboard/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .firebase_service import FirebaseRepository
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from firebase_admin import firestore
from django.http import JsonResponse

def is_admin(user):
    return user.is_superuser


#  Dashboard View (already exists)
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    repo = FirebaseRepository()
    stats = {
        'total_plants': sum(1 for _ in repo.get_all_plants()),
        'total_users': sum(1 for _ in repo.get_all_users()),
        'total_user_plants': sum(1 for _ in repo.get_all_user_plants()),
        'total_communities': sum(1 for _ in repo.get_all_communities()),
    }
    return render(request, 'dashboard/dashboard.html', {'stats': stats})


# -------------------- PLANTS --------------------

@login_required
@user_passes_test(is_admin)
def plant_list(request):
    repo = FirebaseRepository()
    
    # Handle plant creation on POST
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'details': request.POST.get('details'),
            'max_temp': request.POST.get('max_temp'),
            'min_temp': request.POST.get('min_temp'),
            'min_humid': request.POST.get('min_humid'),
            'max_humid': request.POST.get('max_humid'),
            'min_light': request.POST.get('min_light'),
            'max_light': request.POST.get('max_light'),
            'min_soil': request.POST.get('min_soil'),
            'max_soil': request.POST.get('max_soil'),
            'norm_air': request.POST.get('norm_air'),
            'smoke_air': request.POST.get('smoke_air'),
        }
        repo.add_plant(data)
        return redirect('plant-list')
    
    # Fetch and display all plants
    plants = [{'id': p.id, **p.to_dict()} for p in repo.get_all_plants()]
    return render(request, 'dashboard/plants/list.html', {'plants': plants})

@login_required
@user_passes_test(is_admin)
def plant_create(request):
    repo = FirebaseRepository()
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'details': request.POST.get('details'),
            'min_temp': request.POST.get('min_temp'),
            'max_temp': request.POST.get('max_temp'),
            'min_humid': request.POST.get('min_humid'),
            'max_humid': request.POST.get('max_humid'),
            'min_light': request.POST.get('min_light'),
            'max_light': request.POST.get('max_light'),
            'min_soil': request.POST.get('min_soil'),
            'max_soil': request.POST.get('max_soil'),
            'norm_air': request.POST.get('norm_air'),
            'smoke_air': request.POST.get('smoke_air'),
        }
        repo.add_plant(data)
        return redirect('plant-list')
    
    return render(request, 'dashboard/plants/form.html', {'title': 'Add New Plant'})

@login_required
@user_passes_test(is_admin)
def plant_update(request, plant_id):
    repo = FirebaseRepository()
    plant = repo.get_plant(plant_id)
    
    if not plant.exists:
        return redirect('plant-list')

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'details': request.POST.get('details'),
            'max_temp': request.POST.get('max_temp'),
            'min_temp': request.POST.get('min_temp'),
            'min_humid': request.POST.get('min_humid'),
            'max_humid': request.POST.get('max_humid'),
            'min_light': request.POST.get('min_light'),
            'max_light': request.POST.get('max_light'),
            'min_soil': request.POST.get('min_soil'),
            'max_soil': request.POST.get('max_soil'),
            'norm_air': request.POST.get('norm_air'),
            'smoke_air': request.POST.get('smoke_air'),
        }
        repo.update_plant(plant_id, data)
        return redirect('plant-list')
    
    return render(request, 'dashboard/plants/form.html', {
        'title': 'Edit Plant', 'plant': {'id': plant.id, **plant.to_dict()}
    })

@login_required
@user_passes_test(is_admin)
def plant_delete(request, plant_id):
    repo = FirebaseRepository()
    plant = repo.get_plant(plant_id)
    
    if not plant.exists:
        return redirect('plant-list')

    if request.method == 'POST':
        repo.delete_plant(plant_id)
        return redirect('plant-list')

    return render(request, 'dashboard/plants/confirm_delete.html', {'plant_id': plant_id})


# -------------------- USERS --------------------

@login_required
@user_passes_test(is_admin)
def user_list(request):
    repo = FirebaseRepository()
    users = [{'id': u.id, **u.to_dict()} for u in repo.get_all_users()]
    return render(request, 'dashboard/users/list.html', {'users': users})



@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        repo = FirebaseRepository()
        user_data = {
            'email': request.POST.get('email'),
            'name': request.POST.get('name'),
            'role': request.POST.get('role', 'user'),
            'status': 'active',
            'createdAt': datetime.now().isoformat()
        }
        try:
            repo.add_user(user_data)
            messages.success(request, 'User created successfully')
            return redirect('user-list')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'dashboard/users/form.html')

@login_required
@user_passes_test(is_admin)
def user_update(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    
    if not user.exists:
        messages.error(request, 'User not found')
        return redirect('user-list')

    if request.method == 'POST':
        user_data = {
            'name': request.POST.get('name'),
            'role': request.POST.get('role'),
        }
        try:
            repo.update_user(user_email, user_data)
            messages.success(request, 'User updated successfully')
            return redirect('user-list')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')

    return render(request, 'dashboard/users/form.html', {
        'title': 'Edit User', 
        'user': {'id': user_email, **user.to_dict()}
    })

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    
    if not user.exists:
        messages.error(request, 'User not found')
        return redirect('user-list')

    if request.method == 'POST':
        try:
            repo.delete_user(user_email)
            messages.success(request, 'User deleted successfully')
            return redirect('user-list')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')

    return render(request, 'dashboard/users/delete.html', {
        'user': {'id': user_email, **user.to_dict()}
    })

@login_required
@user_passes_test(is_admin)
def user_block(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    
    if not user.exists:
        messages.error(request, 'User not found')
        return redirect('user-list')

    user_data = {'id': user.id, **user.to_dict()}

    if request.method == 'POST':
        try:
            repo.block_user(user_email)
            messages.success(request, f'User {user_email} has been blocked successfully')
            return redirect('user-list')
        except Exception as e:
            messages.error(request, f'Error blocking user: {str(e)}')
            return redirect('user-list')

    return render(request, 'dashboard/users/confirm_block.html', {
        'user': user_data,
        'action': 'block'
    })

@login_required
@user_passes_test(is_admin)
def user_unblock(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    
    if not user.exists:
        messages.error(request, 'User not found')
        return redirect('user-list')

    user_data = {'id': user.id, **user.to_dict()}

    if request.method == 'POST':
        try:
            repo.unblock_user(user_email)
            messages.success(request, f'User {user_email} has been unblocked successfully')
            return redirect('user-list')
        except Exception as e:
            messages.error(request, f'Error unblocking user: {str(e)}')
            return redirect('user-list')

    return render(request, 'dashboard/users/confirm_block.html', {
        'user': user_data,
        'action': 'unblock'
    })


# -------------------- COMMUNITIES --------------------

@login_required
@user_passes_test(is_admin)
def community_list(request):
    repo = FirebaseRepository()
    communities = [{'id': comm.id, **comm.to_dict()} for comm in repo.get_all_communities()]
    return render(request, 'dashboard/communities/list.html', {'communities': communities})



@login_required
@user_passes_test(is_admin)
def community_create(request):
    
    
    repo = FirebaseRepository()
    if request.method == 'POST':
        
        
        # Get current user email from session or request
        current_user_email = request.user.email if request.user.is_authenticated else 'anonymous'
        
        community_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description', ''),
            'profileImageUrl': request.POST.get('profileImageUrl', ''),
            'createdAt': datetime.now().isoformat(),
            'createdBy': "Plantify Admin",
            'status': request.POST.get('status', 'active'),
        }
        
        # Add community document first
        community_ref = repo.add_community(community_data)
        
        # Create empty subcollections for Members and BannedUsers
        community_id = community_ref.id
        repo.db.collection('Communities').document(community_id).collection('Members').document('placeholder').set({'exists': False})
        repo.db.collection('Communities').document(community_id).collection('BannedUsers').document('placeholder').set({'exists': False})
        
        # Add creator as first member
        # repo.join_community(current_user_email, community_id)
        
        return redirect('community-list')

    return render(request, 'dashboard/communities/form.html', {
        'title': 'Create New Community',
        'default_email': request.user.email if request.user.is_authenticated else ''
    })

# @login_required
# @user_passes_test(is_admin)
# def block_community(request, community_id):
#     if request.method == 'POST':
#         repo = FirebaseRepository()
#         try:
#             repo.block_community(community_id, request.user.email)
#             messages.success(request, "Community has been blocked successfully")
#         except Exception as e:
#             messages.error(request, f"Error blocking community: {str(e)}")
#     return redirect('community-list')

# @login_required
# @user_passes_test(is_admin)
# def unblock_community(request, community_id):
#     if request.method == 'POST':
#         repo = FirebaseRepository()
#         try:
#             repo.db.collection('Communities').document(community_id).update({
#                 'status': 'active',
#                 'unblockedAt': datetime.now().isoformat(),
#                 'unblockedBy': request.user.email
#             })
#             messages.success(request, "Community has been unblocked successfully")
#         except Exception as e:
#             messages.error(request, f"Error unblocking community: {str(e)}")
#     return redirect('community-list')

@login_required
@user_passes_test(is_admin)
def block_community(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        try:
            # First verify the community exists
            community_ref = repo.db.collection('Communities').document(community_id)
            community = community_ref.get()
            
            if not community.exists:
                messages.error(request, "Community not found")
                return redirect('community-list')
            
            current_status = community.to_dict().get('status', 'active')
            
            if current_status == 'blocked':
                messages.warning(request, "Community is already blocked")
                return redirect('community-list')
            
            # Update community status and add block info
            update_data = {
                'status': 'blocked',
                'blockedAt': datetime.now().isoformat(),
                'blockedBy': request.user.email,
                'previousStatus': current_status  # Store previous status for restoration
            }
            
            # Add to blocked communities subcollection for tracking
            repo.db.collection('Communities').document(community_id)\
                .collection('blocked_history').document().set({
                    'action': 'blocked',
                    'by': request.user.email,
                    'at': datetime.now().isoformat(),
                    'reason': request.POST.get('reason', 'No reason provided')
                })
            
            community_ref.update(update_data)
            
            # Optional: Notify community members
            # notify_community_members(community_id, 'blocked')
            
            messages.success(request, "Community has been blocked successfully")
            
        except Exception as e:
            messages.error(request, f"Error blocking community: {str(e)}")
            # Log the full error for debugging
            print(f"Error blocking community {community_id}: {str(e)}")
    
    return redirect('community-list')

@login_required
@user_passes_test(is_admin)
def unblock_community(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        try:
            # Verify community exists
            community_ref = repo.db.collection('Communities').document(community_id)
            community = community_ref.get()
            
            if not community.exists:
                messages.error(request, "Community not found")
                return redirect('community-list')
            
            current_status = community.to_dict().get('status', 'active')
            
            if current_status != 'blocked':
                messages.warning(request, "Community is not blocked")
                return redirect('community-list')
            
            # Restore previous status or default to 'active'
            previous_status = community.to_dict().get('previousStatus', 'active')
            
            update_data = {
                'status': previous_status,
                'unblockedAt': datetime.now().isoformat(),
                'unblockedBy': request.user.email
            }
            
            # Add to unblock history
            repo.db.collection('Communities').document(community_id)\
                .collection('unblocked_history').document().set({
                    'action': 'unblocked',
                    'by': request.user.email,
                    'at': datetime.now().isoformat(),
                    'restoredStatus': previous_status
                })
            
            community_ref.update(update_data)
            
            # Optional: Notify community members
            # notify_community_members(community_id, 'unblocked')
            
            messages.success(request, f"Community has been unblocked and restored to {previous_status} status")
            
        except Exception as e:
            messages.error(request, f"Error unblocking community: {str(e)}")
            # Log the full error for debugging
            print(f"Error unblocking community {community_id}: {str(e)}")
    
    return redirect('community-list')



@login_required
@user_passes_test(is_admin)
def community_join(request, community_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    repo = FirebaseRepository()
    user_email = request.user.email
    
    try:
        # Check if community exists and is active
        community = repo.get_community(community_id)
        if not community.exists or community.to_dict().get('status') == 'blocked':
            messages.error(request, "This community is not available or has been blocked")
            return redirect('community-list')
        
        # Check if user is already a member
        member_ref = repo.db.collection('Communities').document(community_id).collection('Members').document(user_email).get()
        if member_ref.exists:
            messages.warning(request, "You are already a member of this community")
            return redirect('community-list')
        
        # Check if user is banned from this community
        banned_ref = repo.db.collection('Communities').document(community_id).collection('BannedUsers').document(user_email).get()
        if banned_ref.exists:
            messages.error(request, "You are banned from joining this community")
            return redirect('community-list')
        
        # Join the community
        repo.join_community(user_email, community_id)
        messages.success(request, "Successfully joined the community")
        
    except Exception as e:
        messages.error(request, f"Error joining community: {str(e)}")
    
    return redirect('community-list')


@login_required
@user_passes_test(is_admin)
def community_update(request, community_id):
    repo = FirebaseRepository()
    community = repo.get_community(community_id)
    
    if not community.exists:
        return redirect('community-list')

    if request.method == 'POST':
        # Get current user email from session or request
        current_user_email = request.user.email if request.user.is_authenticated else 'anonymous'
        
        community_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description', ''),
            'updatedAt': datetime.now().isoformat(),
            'updatedBy': current_user_email,
            'status': request.POST.get('status', 'active'),
           
        }
        
        repo.update_community(community_id, community_data)
        return redirect('community-list')

    # Convert community data to dictionary and prepare tags for form
    community_data = community.to_dict()
  
    
    return render(request, 'dashboard/communities/form.html', {
        'title': 'Edit Community',
        'community': community_data,
        'is_edit': True
    })


@login_required
@user_passes_test(is_admin)
def community_delete(request, community_id):
    repo = FirebaseRepository()
    community = repo.get_community(community_id)
    
    if not community.exists:
        return redirect('community-list')

    if request.method == 'POST':
        # Optional: Delete associated image from storage
        
        repo.delete_community(community_id)
        return redirect('community-list')

    return render(request, 'dashboard/communities/confirm_delete.html', {
        'community': community.to_dict()
    })              

@login_required
@user_passes_test(is_admin)
def community_detail(request, community_id):
    repo = FirebaseRepository()
    community = repo.get_community(community_id)
    
    if not community.exists:
        return redirect('community-list')

    community_data = community.to_dict()
    community_data['id'] = community_id
    
    # Get all members
    members = repo.get_community_members(community_id)
    members_data = []
    for member_email in members:
        user = repo.get_user(member_email)
        if user.exists:
            user_data = user.to_dict()
            user_data['email'] = member_email
            members_data.append(user_data)
    
    # Get banned users
    banned_users = repo.get_banned_users(community_id)
    banned_users_data = []
    for user_email in banned_users:
        user = repo.get_user(user_email)
        if user.exists:
            user_data = user.to_dict()
            user_data['email'] = user_email
            banned_users_data.append(user_data)
    
    # Get all users for adding new members
    all_users = []
    users_ref = repo.db.collection('Users').stream()
    for user in users_ref:
        user_data = user.to_dict()
        user_data['email'] = user.id
        all_users.append(user_data)
    
    return render(request, 'dashboard/communities/detail.html', {
        'community': community_data,
        'members': members_data,
        'banned_users': banned_users_data,
        'all_users': all_users,
        'title': f'Community: {community_data.get("name", "")}'
    })

@login_required
@user_passes_test(is_admin)
def add_member(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        user_email = request.POST.get('user_email')
        
        try:
            repo.join_community(user_email, community_id)
            messages.success(request, f"User {user_email} added to community successfully")
            return redirect('community-detail', community_id=community_id)  # Redirect to detail page after adding
        except Exception as e:
            messages.error(request, f"Error adding member: {str(e)}")
    
    # For GET requests, show the form (modal in our case)
    repo = FirebaseRepository()
    community = repo.get_community(community_id)
    if not community.exists:
        return redirect('community-list')

    # Get all needed data for the modal
    members = repo.get_community_members(community_id)
    banned_users = repo.get_banned_users(community_id)
    all_users = []
    users_ref = repo.db.collection('Users').stream()
    for user in users_ref:
        user_data = user.to_dict()
        user_data['email'] = user.id
        all_users.append(user_data)
    
    return render(request, 'dashboard/communities/detail.html', {
        'community': {'id': community_id, **community.to_dict()},
        'members': [{'email': m, **repo.get_user(m).to_dict()} for m in members if repo.get_user(m).exists],
        'banned_users': [{'email': b, **repo.get_user(b).to_dict()} for b in banned_users if repo.get_user(b).exists],
        'all_users': all_users,
        'title': f'Community: {community.to_dict().get("name", "")}'
    })

@login_required
@user_passes_test(is_admin)
def block_member(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        user_email = request.POST.get('user_email')
        
        try:
            # Remove from members
            repo.db.collection('Communities').document(community_id).collection('Members').document(user_email).delete()
            
            # Add to banned users
            repo.db.collection('Communities').document(community_id).collection('BannedUsers').document(user_email).set({
                'bannedAt': datetime.now().isoformat(),
                'bannedBy': request.user.email
            })
            
            # Remove from user's joined communities
            repo.db.collection('Users').document(user_email).update({
                f'joined_communities.{community_id}': firestore.DELETE_FIELD
            })
            
            messages.success(request, f"User {user_email} has been blocked from this community")
        except Exception as e:
            messages.error(request, f"Error blocking member: {str(e)}")
        
    return redirect('community-detail', community_id=community_id)

@login_required
@user_passes_test(is_admin)
def unblock_user(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        user_email = request.POST.get('user_email')
        
        try:
            # Remove from banned users
            repo.db.collection('Communities').document(community_id).collection('BannedUsers').document(user_email).delete()
            messages.success(request, f"User {user_email} has been unblocked")
        except Exception as e:
            messages.error(request, f"Error unblocking user: {str(e)}")
        
    return redirect('community-detail', community_id=community_id)

@login_required
@user_passes_test(is_admin)
def remove_member(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        user_email = request.POST.get('user_email')
        
        try:
            # Remove from members
            repo.db.collection('Communities').document(community_id).collection('Members').document(user_email).delete()
            
            # Remove from user's joined communities
            repo.db.collection('Users').document(user_email).update({
                f'joined_communities.{community_id}': firestore.DELETE_FIELD
            })
            
            messages.success(request, f"User {user_email} has been removed from this community")
        except Exception as e:
            messages.error(request, f"Error removing member: {str(e)}")
        
    return redirect('community-detail', community_id=community_id)

@login_required
def send_community_message(request, community_id):
    if request.method == 'POST':
        repo = FirebaseRepository()
        try:
            # Verify the community exists
            community_ref = repo.db.collection('Communities').document(community_id)
            if not community_ref.get().exists:
                return JsonResponse({'status': 'error', 'message': 'Community not found'}, status=404)
            
            # Create message with user and community info
            message_data = {
                'text': request.POST.get('text'),
                'sender_id': request.user.email,
                'sender_name': request.user.get_full_name(),
                'sender_avatar': request.user.profile_image_url,
                'community_id': community_id,  
                'createdAt': datetime.now().isoformat(),
                'reply_to': request.POST.get('reply_to', None),
                
            }
            
            # Add to SPECIFIC community's Messages subcollection
            community_ref.collection('Messages').add(message_data)
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def get_community_messages(request, community_id):
    repo = FirebaseRepository()
    try:
        messages = []
        messages_ref = repo.db.collection('Communities').document(community_id)\
            .collection('Messages')\
            .order_by('createdAt', direction=firestore.Query.DESCENDING)\
            .limit(50)\
            .stream()
            
        for msg in messages_ref:
            msg_data = msg.to_dict()
            msg_data['id'] = msg.id
            messages.append(msg_data)
        
        return JsonResponse({'status': 'success', 'messages': messages})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# @login_required
# @user_passes_test(is_admin)
# def send_community_message(request, community_id):
#     if request.method == 'POST':
#         repo = FirebaseRepository()
#         try:
#             message_data = {
#                 'text': request.POST.get('text'),
#                 'sender_id': request.user.email,
#                 'sender_name': request.user.get_full_name(),
#                 'sender_avatar': request.user.profile_image_url,  # Adjust based on your user model
#                 'timestamp': datetime.now().isoformat(),
#                 'reply_to': request.POST.get('reply_to', None),
                
#             }
            
#             # Add new message document with auto-generated ID
#             repo.db.collection('Communities').document(community_id)\
#                 .collection('Messages').add(message_data)
                
#             return JsonResponse({'status': 'success'})
            
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# -------------------- USER PLANTS --------------------

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .firebase_service import FirebaseRepository  

@login_required
@user_passes_test(is_admin)
def user_plant_list(request):
    repo = FirebaseRepository()
    user_plants = [{'id': p.id, **p.to_dict()} for p in repo.get_all_user_plants()]
    return render(request, 'dashboard/user_plants/list.html', {'user_plants': user_plants})


@login_required
@user_passes_test(is_admin)
def user_plant_create(request):
    repo = FirebaseRepository()
    if request.method == 'POST':
        data = {
            'userEmail': request.POST.get('userEmail'),
            'plantName': request.POST.get('plantName'),
            'plant_Type': request.POST.get('plant_Type'),
            'temperature': request.POST.get('temperature'),
            'humidity': request.POST.get('humidity'),
            'lightIntensity': request.POST.get('lightIntensity'),
            'soilMoisture': request.POST.get('soilMoisture'),
            'airQuality': request.POST.get('airQuality'),
        }
        repo.add_user_plants(data)
        return redirect('user-plant-list')

    return render(request, 'dashboard/user_plants/form.html', {'title': 'Add User Plant'})


@login_required
@user_passes_test(is_admin)
def user_plant_update(request, user_email):
    repo = FirebaseRepository()
    user_plant = next(repo.get_user_plants(user_email), None)

    if not user_plant:
        return redirect('user-plant-list')

    if request.method == 'POST':
        data = {
            'userEmail': request.POST.get('userEmail'), 
            'plantName': request.POST.get('plantName'),
            'plant_Type': request.POST.get('plant_Type'),
            'temperature': request.POST.get('temperature'),
            'humidity': request.POST.get('humidity'),
            'lightIntensity': request.POST.get('lightIntensity'),
            'soilMoisture': request.POST.get('soilMoisture'),
            'airQuality': request.POST.get('airQuality'),
        }
        repo.update_user_plants(user_email, data)
        return redirect('user-plant-list')

    return render(request, 'dashboard/user_plants/form.html', {
        'title': 'Edit User Plant',
        'user_plant': {'id': user_plant.id, **user_plant.to_dict()}
    })


@login_required
@user_passes_test(is_admin)
def user_plant_delete(request, user_email):
    repo = FirebaseRepository()
    user_plant = next(repo.get_user_plants(user_email), None)

    if not user_plant:
        return redirect('user-plant-list')

    if request.method == 'POST':
        repo.delete_user_plants(user_email)
        return redirect('user-plant-list')

    return render(request, 'dashboard/user_plants/confirm_delete.html', {'user_email': user_email})


# -------------------- COMMUNITIES --------------------
@login_required
@user_passes_test(is_admin)
def community_list(request):
    repo = FirebaseRepository()
    communities = [{'id': comm.id, **comm.to_dict()} for comm in repo.get_all_communities()]
    return render(request, 'dashboard/communities/list.html', {'communities': communities})


from django.utils import timezone
from datetime import datetime



# -------------------- DISEASES --------------------
@login_required
@user_passes_test(is_admin)
def disease_list(request):
    repo = FirebaseRepository()
    diseases = [{'id': d.id, **d.to_dict()} for d in repo.get_all_diseases()]
    return render(request, 'dashboard/diseases/list.html', {'diseases': diseases})

@login_required
@user_passes_test(is_admin)
def disease_create(request):
    repo = FirebaseRepository()
    if request.method == 'POST':
        data = {
            'cause': request.POST.get('cause'),
            'class_id': request.POST.get('class_id'),
            'cure': request.POST.get('cure'),
            'disease': request.POST.get('disease'),
            'information': request.POST.get('information'),
            'plant': request.POST.get('plant'),
            'type': request.POST.get('type'),
        }
        repo.add_disease(data)
        return redirect('disease-list')
    
    return render(request, 'dashboard/diseases/form.html', {'title': 'Add New Disease'})

@login_required
@user_passes_test(is_admin)
def disease_update(request, disease_id):
    repo = FirebaseRepository()
    disease = repo.get_disease(disease_id)

    if not disease.exists:
        return redirect('disease-list')

    if request.method == 'POST':
        data = {
            'cause': request.POST.get('cause'),
            'class_id': request.POST.get('class_id'),
            'cure': request.POST.get('cure'),
            'disease': request.POST.get('disease'),
            'information': request.POST.get('information'),
            'plant': request.POST.get('plant'),
            'type': request.POST.get('type'),
        }
        repo.update_disease(disease_id, data)
        return redirect('disease-list')

    return render(request, 'dashboard/diseases/form.html', {
        'title': 'Edit Disease',
        'disease': {'id': disease.id, **disease.to_dict()}
    })

@login_required
@user_passes_test(is_admin)
def disease_delete(request, disease_id):
    repo = FirebaseRepository()
    disease = repo.get_disease(disease_id)

    if not disease.exists:
        return redirect('disease-list')

    if request.method == 'POST':
        repo.delete_disease(disease_id)
        return redirect('disease-list')

    return render(request, 'dashboard/diseases/confirm_delete.html', {'disease_id': disease_id})

