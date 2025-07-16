from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom Permission:
    - If not post author then read only,
    - else all permission(delete,update post)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
    
class IsAuthor(BasePermission):
    """
    Custom Permission:
    - Checks for the person requested the action is author of post/comment or not
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False