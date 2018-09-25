from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.test import TestCase, RequestFactory
from tokenize import String

from xf.uc_dashboards.models import Page
from xf.xf_crud.permission_mixin import XFPermissionMixin


class XFPermissionsTestCase(TestCase):

    fixtures = ['default_pages_and_perspectives_data.json']

    @classmethod
    def _generate_test_data(cls):

        test_data = {}

        class TestClassExtendsMixin(XFPermissionMixin):
            def __init__(self, model: Model):
                self.request =  RequestFactory().get('/')
                self.context = {}
                self.model = model
            def set_requesting_user(self, user: User):
                self.request.user = user
            class Meta:
                model = Page

        test_data['model_class'] = Page
        test_data['model_instance'] = Page.objects.first()
        test_data['permission_mixin_class'] = TestClassExtendsMixin
        test_data['user'] = cls._generate_user()
        test_data['user_group'], created = Group.objects.get_or_create(name='Test')
        test_data['user_group_1'], created = Group.objects.get_or_create(name='Test 1')
        test_data['user_group_2'], created = Group.objects.get_or_create(name='Test 2')
        test_data['class_instance'] = TestClassExtendsMixin(Page)
        test_data['model_content_type'] = ContentType.objects.filter(model='page', app_label='uc_dashboards').first()
        test_data['model_delete_permission'], created = Permission.objects.get_or_create(
            content_type=test_data['model_content_type'],
            codename='delete_page',
            defaults={'name': "Can delete page"},
        )

        return test_data


    @classmethod
    def _generate_user(cls):

        def assign_model_permission(self, permission_to_assign: String, model: Model):
            content_type, created = ContentType.objects.get_or_create(app_label=model._meta.app_label,
                                                                      model=model._meta.model_name)
            permission, created = Permission.objects.get_or_create(
                codename=permission_to_assign,
                content_type=content_type,
                defaults={'name': 'Can list client'},
            )
            self.user_permissions.add(permission)

        def assign_to_group(self, group: Group):
            self.groups.add(group)

        User.assign_model_permission = assign_model_permission
        User.assign_to = assign_to_group

        return User.objects.create_user(
            username="test",
            email="test@test.com",
            password="test"
        )


    @classmethod
    def _assign_permission(cls, user: User, permission_to_assign: Permission):
        user.user_permissions.add(permission_to_assign)
        user.save()