from rest_framework import permissions

from .groups import AdminGroup, DeveloperGroup, StaffGroup


class CBasePermission(permissions.BasePermission):
    def get_groups_ids(self, request) -> list:
        groups = request.user.groups.all()
        return [item.id for item in groups]


class IsStaff(CBasePermission):
    def has_permission(self, request, view):
        groups_ids = self.get_groups_ids(request)
        return (StaffGroup.id in groups_ids)


class IsDeveloper(CBasePermission):
    def has_permission(self, request, view):
        groups_ids = self.get_groups_ids(request)
        return (DeveloperGroup.id in groups_ids)


class IsAdmin(CBasePermission):
    def has_permission(self, request, view):
        groups_ids = self.get_groups_ids(request)
        return (AdminGroup.id in groups_ids)


class IsAdminOrStaffOrDevloper(CBasePermission):
    def has_permission(self, request, view):
        groups_ids = self.get_groups_ids(request)
        return (StaffGroup.id in groups_ids) or (DeveloperGroup.id in groups_ids) or (AdminGroup.id in groups_ids)


__all__ = ('IsAdmin', 'IsDeveloper', 'IsStaff', 'IsAdminOrStaffOrDevloper')
