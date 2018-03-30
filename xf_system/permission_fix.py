#from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# TO RUN THIS SCRIPT, OPEN A PYTHON CONSOLE FROM WITHIN PYCHARM
# THEN TYPE:
# from xf.xf_system.permission_fix import add_view_permissions
# add_view_permissions(None)
# add_list_permissions(None)


# make sure to use the right settings file so that you can do this on the correct db


def add_view_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a view permission too all our
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            print("Added view permission for %s" % content_type.name)

def add_list_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a view permission too all our
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "list_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can list %s" % content_type.name)
            print("Added list permission for %s" % content_type.name)
