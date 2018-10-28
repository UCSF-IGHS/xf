from django.test import TestCase

from xf.tests.permission_tests.permissions_tests import XFPermissionsTestCase
from xf.xf_crud.model_forms import XFModelForm


class XFModelFormTestCase(XFPermissionsTestCase):

    def test_is_new_entity(self):

        test_data = self._generate_test_data()
        saved_page = test_data['model_instance']

        modelform = test_data['model_form_instance']
        self.assertTrue(modelform.is_new_entity(), 'Expected True since form is new')

        modelform.instance = saved_page
        self.assertFalse(modelform.is_new_entity(), 'Expected False since page on form is already saved in database')
