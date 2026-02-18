#this is read only,
# concerned for all the 
# crud, the get will work for all since its available for listing to everyone except buyers, 
# put only by field officers authenticated as, then 
# delete and update also by logged in auth field officers 
# also , put and delete cannot be deleted by other field officers if I animal vet cannot edit 
# also what if when a field officer wants too update a field and not all fields will be updated as well
from rest_framework.permissions import BasePermission

class IsFieldOfficer(BasePermission):
    '''
    Custom Permission IsFieldOfficer
    '''
    #to create a post one must be a field officer
    def has_permission(self, request, view):
        #deny access to buyers
        if not request.user.is_authenticated or request.user.role == 'buyer':
            return False
        
        #only field officers can create services
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.role == 'field_officer'
        return True
    
    #only the person who created the service can view it
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.provider == request.user
        return True