# dashboard/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .firebase_service import FirebaseRepository
from django.urls import reverse

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from dashboard.firebase_service import FirebaseRepository

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


# @login_required
# @user_passes_test(is_admin)
# def plant_list(request):
#     repo = FirebaseRepository()
#     if request.method == 'POST':
#         data = {
#             'name': request.POST.get('name'),
#             'details': request.POST.get('details'),
#             'max_temp': request.POST.get('max_temp'),
#             'min_temp': request.POST.get('min_temp'),
#         }
#         repo.add_plant(data)
#         return redirect('plant-list')
    
#     plants = [{'id': p.id, **p.to_dict()} for p in repo.get_all_plants()]
#     return render(request, 'dashboard/plants/list.html', {'plants': plants})

# @login_required
# @user_passes_test(is_admin)
# def plant_detail(request, plant_id):
#     repo = FirebaseRepository()
#     plant = repo.get_plant(plant_id)
#     if not plant.exists:
#         return redirect('plant-list')

#     if request.method == 'POST':
#         if 'delete' in request.POST:
#             repo.delete_plant(plant_id)
#             return redirect('plant-list')
#         else:
#             data = {
#                 'name': request.POST.get('name'),
#                 'details': request.POST.get('details'),
#                 'max_temp': request.POST.get('max_temp'),
#                 'min_temp': request.POST.get('min_temp'),
#             }
#             repo.update_plant(plant_id, data)
#             return redirect('plant-detail', plant_id=plant_id)

#     return render(request, 'dashboard/plants/detail.html', {
#         'plant': {'id': plant.id, **plant.to_dict()}
#     })

# -------------------- USERS --------------------
@login_required
@user_passes_test(is_admin)
def user_list(request):
    repo = FirebaseRepository()
    users = [{'id': u.id, **u.to_dict()} for u in repo.get_all_users()]
    return render(request, 'dashboard/users/list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_email):
    repo = FirebaseRepository()
    user = repo.get_user(user_email)
    if not user.exists:
        return redirect('user-list')

    if request.method == 'POST' and 'delete' in request.POST:
        repo.delete_user(user_email)
        return redirect('user-list')

    return render(request, 'dashboard/users/detail.html', {
        'user': {'id': user.id, **user.to_dict()}
    })

# -------------------- USER PLANTS --------------------
@login_required
@user_passes_test(is_admin)
def user_plant_list(request):
    repo = FirebaseRepository()
    user_plants = [{'id': up.id, **up.to_dict()} for up in repo.get_all_user_plants()]
    return render(request, 'dashboard/user_plants/list.html', {'user_plants': user_plants})

@login_required
@user_passes_test(is_admin)
def user_plant_detail(request, plant_id):
    repo = FirebaseRepository()
    user_plant = repo.db.collection('Users_Plants').document(plant_id).get()
    if not user_plant.exists:
        return redirect('user-plant-list')

    if request.method == 'POST' and 'delete' in request.POST:
        repo.delete_user_plant(plant_id)
        return redirect('user-plant-list')

    return render(request, 'dashboard/user_plants/detail.html', {
        'user_plant': {'id': user_plant.id, **user_plant.to_dict()}
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
def community_detail(request, community_id):
    repo = FirebaseRepository()
    community = repo.get_community(community_id)
    if not community.exists:
        return redirect('community-list')

    if request.method == 'POST' and 'delete' in request.POST:
        repo.delete_community(community_id)
        return redirect('community-list')

    members = list(repo.db.collection('Communities').document(community_id).collection('Members').stream())

    return render(request, 'dashboard/communities/detail.html', {
        'community': {'id': community.id, **community.to_dict()},
        'members': [m.to_dict() for m in members]
    })

# -------------------- DISEASES --------------------
@login_required
@user_passes_test(is_admin)
def disease_list(request):
    repo = FirebaseRepository()
    diseases = [{'id': d.id, **d.to_dict()} for d in repo.get_all_diseases()]
    return render(request, 'dashboard/diseases/list.html', {'diseases': diseases})

@login_required
@user_passes_test(is_admin)
def disease_detail(request, disease_id):
    repo = FirebaseRepository()
    disease = repo.get_disease(disease_id)
    if not disease.exists:
        return redirect('disease-list')

    if request.method == 'POST' and 'delete' in request.POST:
        repo.delete_disease(disease_id)
        return redirect('disease-list')

    return render(request, 'dashboard/diseases/detail.html', {
        'disease': {'id': disease.id, **disease.to_dict()}
    })



# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.shortcuts import render, redirect
# from .firebase_service import FirebaseRepository

# def is_admin(user):
#     return user.is_superuser

# # Dashboard View (already exists)
# @login_required
# @user_passes_test(is_admin)
# def dashboard(request):
#     repo = FirebaseRepository()
#     stats = {
#         'total_plants': sum(1 for _ in repo.get_all_plants()),
#         'total_users': sum(1 for _ in repo.get_all_users()),
#         'total_user_plants': sum(1 for _ in repo.get_all_user_plants()),
#         'total_communities': sum(1 for _ in repo.get_all_communities()),
#     }
#     return render(request, 'dashboard/dashboard.html', {'stats': stats})

# # Plant Views (already exists)
# @login_required
# @user_passes_test(is_admin)
# def plant_list(request):
#     repo = FirebaseRepository()
#     plants = [{'id': plant.id, **plant.to_dict()} for plant in repo.get_all_plants()]
#     return render(request, 'dashboard/plants/list.html', {'plants': plants})

# @login_required
# @user_passes_test(is_admin)
# def plant_detail(request, plant_id):
#     repo = FirebaseRepository()
#     plant = repo.get_plant(plant_id)
#     if not plant.exists:
#         return redirect('plant-list')
    
#     if request.method == 'POST':
#         data = {
#             'name': request.POST.get('name'),
#             'details': request.POST.get('details'),
#             'max_temp': request.POST.get('max_temp'),
#             'min_temp': request.POST.get('min_temp'),
#         }
#         repo.update_plant(plant_id, data)
#         return redirect('plant-detail', plant_id=plant_id)
    
#     return render(request, 'dashboard/plants/detail.html', {
#         'plant': {'id': plant.id, **plant.to_dict()}
#     })

# # User Views
# @login_required
# @user_passes_test(is_admin)
# def user_list(request):
#     repo = FirebaseRepository()
#     users = [{'id': user.id, **user.to_dict()} for user in repo.get_all_users()]
#     return render(request, 'dashboard/users/list.html', {'users': users})

# @login_required
# @user_passes_test(is_admin)
# def user_detail(request, user_email):
#     repo = FirebaseRepository()
#     user = repo.get_user(user_email)
#     if not user.exists:
#         return redirect('user-list')
    
#     if request.method == 'POST':
#         # Handle user updates if needed
#         pass
    
#     return render(request, 'dashboard/users/detail.html', {
#         'user': {'id': user.id, **user.to_dict()}
#     })

# # User Plants Views
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
    
#     return render(request, 'dashboard/user_plants/detail.html', {
#         'user_plant': {'id': user_plant.id, **user_plant.to_dict()}
#     })

# # Community Views
# @login_required
# @user_passes_test(is_admin)
# def community_list(request):
#     repo = FirebaseRepository()
#     communities = [{'id': comm.id, **comm.to_dict()} for comm in repo.get_all_communities()]
#     return render(request, 'dashboard/communities/list.html', {'communities': communities})

# @login_required
# @user_passes_test(is_admin)
# def community_detail(request, community_id):
#     repo = FirebaseRepository()
#     community = repo.get_community(community_id)
#     if not community.exists:
#         return redirect('community-list')
    
#     # Get members
#     members = list(repo.db.collection('Communities').document(community_id)
#                           .collection('Members').stream())
    
#     return render(request, 'dashboard/communities/detail.html', {
#         'community': {'id': community.id, **community.to_dict()},
#         'members': [m.to_dict() for m in members]
#     })

# # Disease Views
# @login_required
# @user_passes_test(is_admin)
# def disease_list(request):
#     repo = FirebaseRepository()
#     diseases = [{'id': disease.id, **disease.to_dict()} for disease in repo.get_all_diseases()]
#     return render(request, 'dashboard/diseases/list.html', {'diseases': diseases})

# @login_required
# @user_passes_test(is_admin)
# def disease_detail(request, disease_id):
#     repo = FirebaseRepository()
#     disease = repo.get_disease(disease_id)
#     if not disease.exists:
#         return redirect('disease-list')
    
#     return render(request, 'dashboard/diseases/detail.html', {
#         'disease': {'id': disease.id, **disease.to_dict()}
#     })