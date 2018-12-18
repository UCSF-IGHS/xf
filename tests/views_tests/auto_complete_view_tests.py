from django.contrib.auth.models import User
from django.test import RequestFactory

from xf.tests.xf_test_case_data import XFTestCaseData
from xf.xf_crud.views.auto_complete_view import XFAutoCompleteView


class AutoCompleteViewTestCase(XFTestCaseData):

    def test_process_forwarded_parameters(self):

        view = XFAutoCompleteView()
        view.forwarded = {
            "_user_model": "auth.User",
            "_user_search_field": "username"
        }

        view.process_forwarded_parameters()

        self.assertEqual(view.model, User, 'Expected model to be User')
        self.assertEqual(view.model_field_name, 'username', "Expected the search model_field_name to be 'username'")


    def test_get_queryset(self):

        test_data = self._generate_permissions_test_data()

        view = XFAutoCompleteView()
        view.forwarded = {
            "_user_model": "auth.User",
            "_user_search_field": "username"
        }

        request = RequestFactory().get('/')
        request.user = test_data['user']
        view.request = request
        view.q = 'test'

        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1, "Expecting one user with username starting with 'test'")
        self.assertEqual(queryset.first().username, 'test', "Expecting one user with username 'test'")

