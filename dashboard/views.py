# dashboard/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .firebase_service import FirebaseRepository
from django.urls import reverse
from datetime import datetime

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
            'status': request.POST.get('status', 'active'),
            'createdAt': datetime.now().isoformat()  # optional: store creation time
        }
        repo.add_user(user_data)
        return redirect('user-list')


    return render(request, 'dashboard/users/form.html')

@login_required
@user_passes_test(is_admin)
def user_update(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    if not user.exists:
        return redirect('user-list')

    if request.method == 'POST':
        user_data = {
            'email': request.POST.get('email'),
            'name': request.POST.get('name'),
            'role': request.POST.get('role'),
            'status': request.POST.get('status'),
        }
        repo.update_user(user_email, user_data)  # Assuming a method to update user in Firebase
        return redirect('user-list')

    return render(request, 'dashboard/users/form.html', {
        'title': 'Edit User', 'user': {'id': user.id, **user.to_dict()}
    })
    
@login_required
@user_passes_test(is_admin)
def user_delete(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    if not user.exists:
        return redirect('user-list')

    if request.method == 'POST':
        repo.delete_user(user_email)
        return redirect('user-list')

    return render(request, 'dashboard/users/delete.html', {
        'user': {'id': user.id, **user.to_dict()}
    }
    # return render(request, 'dashboard/users/delete.html', {'user_id': user.id})
    )              

@login_required
@user_passes_test(is_admin)
def user_block(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    if not user.exists:
        return redirect('user-list')

    if request.method == 'POST':
        repo.block_user(user_email)  # Assuming a method to block user in Firebase
        return redirect('user-list')

    return render(request, 'dashboard/users/block.html', {
        'user': {'id': user.id, **user.to_dict()}
    })

# -------------------- USER PLANTS --------------------
# @login_required
# @user_passes_test(is_admin)
# def user_plant_list(request):
#     repo = FirebaseRepository()
#     user_plants = [{'id': up.id, **up.to_dict()} for up in repo.get_all_user_plants()]
#     return render(request, 'dashboard/user_plants/list.html', {'user_plants': user_plants})

# @login_required
# @user_passes_test(is_admin)
# def user_plant_detail(request, plant_id):
#     repo = FirebaseRepository()
#     user_plant = repo.db.collection('Users_Plants').document(plant_id).get()
#     if not user_plant.exists:
#         return redirect('user-plant-list')

#     if request.method == 'POST' and 'delete' in request.POST:
#         repo.delete_user_plant(plant_id)
#         return redirect('user-plant-list')

#     return render(request, 'dashboard/user_plants/detail.html', {
#         'user_plant': {'id': user_plant.id, **user_plant.to_dict()}
#     })

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

# @login_required
# @user_passes_test(is_admin)
# def community_detail(request, community_id):
#     repo = FirebaseRepository()
#     community = repo.get_community(community_id)
#     if not community.exists:
#         return redirect('community-list')

#     if request.method == 'POST' and 'delete' in request.POST:
#         repo.delete_community(community_id)
#         return redirect('community-list')

#     members = list(repo.db.collection('Communities').document(community_id).collection('Members').stream())

#     return render(request, 'dashboard/communities/detail.html', {
#         'community': {'id': community.id, **community.to_dict()},
#         'members': [m.to_dict() for m in members]
#     })

# @login_required
# @user_passes_test(is_admin)
# def community_create(request):
#     if request.method == 'POST':
#         repo = FirebaseRepository()
#         user_data = {
#             'email': request.POST.get('email'),
#             'name': request.POST.get('name'),
#             'role': request.POST.get('role', 'user'),
#             'status': request.POST.get('status', 'active'),
#             'createdAt': datetime.now().isoformat()  # optional: store creation time
#         }
#         repo.add_user(user_data)
#         return redirect('user-list')


#     return render(request, 'dashboard/users/form.html')

from django.utils import timezone
from datetime import datetime

@login_required
@user_passes_test(is_admin)
def community_create(request):
    if request.method == 'POST':
        repo = FirebaseRepository()
        
        # Get current user email from session or request
        current_user_email = request.user.email if request.user.is_authenticated else 'anonymous'
        
        community_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description', ''),
            'profileImageUrl': request.POST.get('profileImageUrl', ''),
            'createdAt': datetime.now().isoformat(),
            'createdBy': current_user_email,
            'members': {  # Initial members structure
                'placeholder': True  # As seen in your Firebase structure
            },
            'bannedUsers': {  # Initial banned users structure
                'placeholder': True  # As seen in your Firebase structure
            },
            'status': request.POST.get('status', 'active'),
           
        }
        
        repo.add_community(community_data)
        return redirect('community-list')

    return render(request, 'dashboard/communities/form.html', {
        'title': 'Create New Community',
        'default_email': request.user.email if request.user.is_authenticated else ''
    })

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

# @login_required
# @user_passes_test(is_admin)
# def community_block(request, user_email):
#     repo = FirebaseRepository()
#     user = repo.get_user(user_email)
#     if not user.exists:
#         return redirect('user-list')

#     if request.method == 'POST':
#         repo.block_user(user_email)  # Assuming a method to block user in Firebase
#         return redirect('user-list')

#     return render(request, 'dashboard/users/block.html', {
#         'user': {'id': user.id, **user.to_dict()}
#     })



# -------------------- DISEASES --------------------
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
# from .firebase_service import FirebaseRepository

# def is_admin(user):
#     return user.is_authenticated and user.is_staff

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

