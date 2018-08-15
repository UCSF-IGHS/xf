from django.contrib.auth.models import User, AnonymousUser

from xf.uc_dashboards.models import Perspective, XFVizSiteSettings
from xf.xf_system.models import XFSiteSettings


def user_load_perspectives(self):
    """
    This method loads all perspectives for a given user. If a user is a super user, all perspectives are loaded
    automatically, and no checks will be done.
    """

    self.perspectives = []

    # Load all perspectives if a super user
    if self.is_superuser:
        for perspective in Perspective.objects.all():
            self.perspectives.append(perspective)

    # Only load the group perspectives for the groups that the user belongs to
    elif self.is_authenticated and self.profile is not None:
        for group in self.groups.all():
            for perspective in group.profile.perspectives.all():
                self.perspectives.append(perspective)

                # Users not logged in should have the anonymous perspective if it exists
    elif self.is_anonymous is not None:
        settings = XFSiteSettings.objects.first()
        if settings:
            xf_viz_settings = XFVizSiteSettings.objects.filter(settings=settings).first()
            if xf_viz_settings:
                self.perspectives.append(xf_viz_settings.anonymous_perspective)

    if self.is_authenticated and self.profile:
        if self.profile.default_perspective:
            if not self.profile.default_perspective in self.perspectives:
                self.perspectives.append(self.profile.default_perspective)


def user_load_perspective(self, perspective, useCache):
    """
    Checks if a user needs to load perspectives, and if so, loads it.
    :param self:
    :param perspective:
    :return:
    """

    # Load perspectives if not already loaded, or if explitcely not to use the cache for this user
    if not hasattr(self, 'perspectives') or not useCache:
        self.load_perspectives()

    if not self.perspectives:
        return None

    if not perspective:
        return None

    if perspective in self.perspectives:
        return perspective

    return None

    pass


# Add a method to the User class that is implemented by the method above
User.load_perspectives = user_load_perspectives
User.load_perspective = user_load_perspective
AnonymousUser.load_perspectives = user_load_perspectives
AnonymousUser.load_perspective = user_load_perspective
