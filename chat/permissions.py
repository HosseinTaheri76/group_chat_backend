from rest_framework.permissions import BasePermission


class NotAlreadyMember(BasePermission):
    message = 'already_joined'

    def has_object_permission(self, request, view, obj):
        return not obj.members.filter(user_id=request.user.id).exists()
