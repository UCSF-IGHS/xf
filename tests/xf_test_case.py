import uuid
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.db.models import Model
from django.test import TestCase, RequestFactory
from tokenize import String


class XFTestCase(TestCase):
    """
    Serves as a base class with methods that can help you generate your test data
    """

    fixtures = ['default_pages_and_perspectives_data.json']

    def generate_user(self, username: str=None, password: str=None, first_name: str=None, last_name: str=None,
                      email: str=None):
        """
        Generates a user and adds extension methods on this user to assist in easily performing the following
        1. assigning model permission to the user:
            call this method user.assign_model_permission(permission: String, model: Model)
        2. assign a permission token to a user:
            call user.assign_token(token_name: String, tokens_model: Model). Tokens are special permissions for access
            to particular areas in your application. They are generally prefixed with token_ e.g. token_ui_cd4
        3. remove token:
            call user.remove_token(token_name: String)
        4. assign a user to a group: call user.assign_to(group: Group)

        :param username: Optional
        :param password: Optional
        :param first_name: Optional
        :param last_name: Optional
        :param email: Optional
        :return:
        """
        user = User.objects.create_user(
            username=str(uuid.uuid4()) if username is None else username,
            email=email,
            password='empty' if password is None else password,
            first_name="first" if first_name is None else first_name,
            last_name="last" if last_name is None else last_name,
        )
        user.save()

        def assign_model_permission(self, permission_to_assign: String, model: Model):
            permission_to_assign = '{}_{}'.format(permission_to_assign, model._meta.model_name)
            content_type, created = ContentType.objects.get_or_create(app_label=model._meta.app_label,
                                                                      model=model._meta.model_name)
            permission, created = Permission.objects.get_or_create(
                codename=permission_to_assign,
                content_type=content_type,
                defaults={'name': 'Can list records'},
            )
            self.user_permissions.add(permission)
            reloaded_user = User.objects.get(pk=self.pk)
            return reloaded_user

        def assign_token(self, token: String, model):
            content_type, created = ContentType.objects.get_or_create(
                app_label=model._meta.app_label,
                model=model._meta.model_name
            )
            permission, created = Permission.objects.get_or_create(
                codename=token,
                content_type=content_type,
                defaults={'name': token.replace('_', ' ')},

            )
            self.user_permissions.add(permission)
            reloaded_user = User.objects.get(pk=self.pk)
            return reloaded_user

        def remove_token(self, token: String):
            self.user_permissions.remove(Permission.objects.get(codename=token))
            reloaded_user = User.objects.get(pk=self.pk)
            return reloaded_user

        def assign_to_group(self, group: Group):
            self.groups.add(group)
            reloaded_user = User.objects.get(pk=self.pk)
            return reloaded_user

        User.assign_model_permission = assign_model_permission
        User.assign_token = assign_token
        User.remove_token = remove_token
        User.assign_to = assign_to_group

        return user

    def setup_request(self, request, user: User, session_data: dict=None):
        request.user = user

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        if session_data is not None:
            for key, value in session_data:
                request.session[key] = value
                request.session.save()
        return request

    def generate_request(self, path: str=None, user: User=None):
        factory = RequestFactory()
        request = factory.get('/' if path is None else path)
        if user:
            request.user = user
        return request
