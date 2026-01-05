from rest_framework.permissions import BasePermission, SAFE_METHODS

soft_actions = ["POST", "PATCH"]


class BaseReadOnlyPermission(BasePermission):
    """Base permission that allows read access to everyone"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return self.has_write_permission(request, view)

    def has_write_permission(self, request, view):
        """Override this method in subclasses"""
        raise NotImplementedError


class BaseObjectPermission(BaseReadOnlyPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return self.has_write_permission_object(request, view, obj)

    def has_write_permission_object(self, request, view, obj):
        """Override this method in subclasses"""
        raise NotImplementedError

    def has_write_permission(self, request, view):
        return True


class BaseHardPermission(BaseObjectPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if view.action == "add_file":
            return True
        if request.user.is_anonymous:
            return False
        if not request.user.is_full_editor:
            return False
        return self.has_write_permission_object(request, view, obj)


class IsFullEditorOrReadOnly(BaseReadOnlyPermission):
    def has_write_permission(self, request, view):
        return request.user.is_full_editor


class IsAdminOrReadOnly(BaseReadOnlyPermission):
    def has_write_permission(self, request, view):
        return request.user.is_admin


class IsEditorOrCreateOrRead(BaseHardPermission):

    def has_write_permission_object(self, request, view, obj):

        if request.method in soft_actions and obj.status_validation.open_editor:
            return True

        if obj.status_validation.open_editor:
            return request.user.is_full_editor

        return request.user.is_admin


class DynamicCatalogPermission(BaseHardPermission):

    def has_write_permission_object(self, request, view, obj):

        medium_actions = ["POST", "PATCH", "PUT"]
        if request.method in medium_actions:
            return True

        if obj.status_validation.open_editor:
            return request.user.is_full_editor

        return request.user.is_admin

