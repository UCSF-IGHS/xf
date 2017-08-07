
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden

class PermissionMixin(object):
    """
    Provides a basic security model for views.
    This class requirers cleanup.
    """

    def __user_has_model_perm(self, permission):
        """
        Returns whether the current user has a specific persmission.
        """
        return True
        #TODO Fix This
        return self.request.user.has_perm('%s.%s_%s' % (self.model._meta.app_label, permission, self.model._meta.module_name))

    def ensure_model_perm_or_403(self, permission):
        """
        Ensure that the user has the model permission. If not, a 403 is thrown.
        This method is currently IN USE.
        """
        return True
        #TODO Fix This

        if not self.request.user.has_perm('%s.%s_%s' % (self.model._meta.app_label, permission, self.model._meta.module_name)):
            raise PermissionDenied

    def ensure_set_context_perm(self, permission):
        """
        Prepares the context. Also ensures that the user has the permission.
        This method is currently IN USE
        """
        self.ensure_model_perm_or_403(permission)
        self.set_context_perm(permission)

    def set_context_perm(self, permission):
        """
        Prepares the context for a permission. Will not raise an exception if the user does not have the permission.
        This method is currently IN USE.
        """
        self.context[permission] = self.__user_has_model_perm(permission)

    def __ensure_perm_or_404_OBSOLETED(self, permission):
        """
        Ensures that a user has a certain permission. If the user does not have the permission, a 404 is thrown.
        """
        if not self.has_perm(permission):
            raise PermissionDenied()

    def has_perm(self, permission):
        """
        Returns a boolean that determines whether a user has a given permission. It also sets the context variable
        for the given permission to True.
        """

        self.context[permission] = False
        if hasattr(self, "Meta") or permission == "delete":
            self.model = self.Meta.model
        else:
            self.model = self.get_form_class().Meta.model
        if not self.request.user.has_perm("%s_%s" % (permission, self.model.__name__.lower())):
            return False
        self.context[permission] = True
        return True

    def ensure_group_or_403(self, group):
        """
        Ensures that a user is a member of a certain group. If not, a 403 is thrown.
        This method is currently IN USE.
        """

        # Disable the context for this group
        self.context[group] = False

        # Raise permission denied if permission not available
        if not (self.request.user.groups.filter(name=group).count() == 1 or \
           self.request.user.is_superuser):
            raise PermissionDenied

        # Set to true if permission is available
        self.context[group] = True

    def ensure_perm_or_403(self, permission, model_name):
        """
        Ensures a user has a certain permission for a certain model.
        """
        if not self.request.user.has_perm("%s_%s" % (permission, model_name.lower())):
            raise PermissionDenied

    @staticmethod
    def user_in_group(user, groups):

        if user.is_superuser:
            return True

        if not len(groups):
            return True

        for group in groups:
            if group in user.groups.all():
                return True

        return False