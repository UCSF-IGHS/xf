import uuid
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model
from django.test import TestCase
from tokenize import String

from xf.uc_dashboards.models import Page
from xf.xf_services import XFModelState, XFModelStateMixIn


class XFServicesTestCase(TestCase):

    fixtures = ['default_pages_and_perspectives_data.json']

    @classmethod
    def _generate_model_state_test_data(cls):

        test_data = {}

        class TestModelState(XFModelState):
            STATE_11 = 11
            STATE_12 = 12
            STATE_13 = 13
            STATE_14 = 14
            class Meta:
                managed = False

        class TestModel(XFModelStateMixIn):
            def __init__(self):
                super().__init__()
                self.pk = str(uuid.uuid4()).replace("-", "_")
            class Meta:
                managed = False


        test_data['model_class'] = Page
        test_data['model_instance'] = Page.objects.first()
        test_data['model_states'] = TestModelState
        test_data['dummy_stateful_model'] = TestModel
        test_data['dummy_stateful_model_instance'] = TestModel()
        test_data['user'] = cls._generate_user()
        test_data['model_content_type'] = ContentType.objects.filter(model='page', app_label='uc_dashboards').first()
        test_data['model_delete_permission'], created = Permission.objects.get_or_create(
            content_type=test_data['model_content_type'],
            codename='delete_page',
            defaults={'name': "Can delete page"},
        )

        def add_state(self, state: TestModelState):
            self._add_state(state)

        TestModel.add_state = add_state

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

        User.assign_model_permission = assign_model_permission

        return User.objects.create_user(
            username="test",
            email="test@test.com",
            password="test"
        )


    @classmethod
    def _assign_permission(cls, user: User, permission_to_assign: Permission):
        user.user_permissions.add(permission_to_assign)
        user.save()