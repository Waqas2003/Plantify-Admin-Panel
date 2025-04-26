from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .firebase_service import FirebaseRepository

class FirestoreModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view_link')
    exclude = ('id',)  # Hide ID field in add/change forms
    
    def get_queryset(self, request):
        # Return empty queryset since we're not using Django ORM
        return []
    
    def view_link(self, obj):
        return format_html('<a href="{}">View in Firestore</a>', reverse('plant-detail', args=[obj.id]))
    
    def save_model(self, request, obj, form, change):
        # Handle saving to Firestore instead of Django DB
        repo = FirebaseRepository()
        data = {field.name: getattr(obj, field.name) for field in obj._meta.fields if field.name != 'id'}
        if change:
            repo.update_plant(obj.id, data)
        else:
            # For adding new documents, you'd need to implement this
            pass
    
    def delete_model(self, request, obj):
        # Handle Firestore deletion
        repo = FirebaseRepository()
        repo.db.collection('Plants').document(obj.id).delete()

# # Register placeholder admin models
# admin.site.register(PlantType, FirestoreModelAdmin)
# admin.site.register(User, FirestoreModelAdmin)
# Register other models similarly