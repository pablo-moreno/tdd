from rest_framework.permissions import BasePermission


class ArticlePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ('update', 'partial_update'):
            return obj.user == request.user
        return True
