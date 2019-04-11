from xf.tests.xf_test_case_data import XFTestCaseData
from xf.xf_crud.model_forms import XFModelForm


class XFModelFormTestCase(XFTestCaseData):

    def test_is_new_entity(self):

        test_data = self._generate_permissions_test_data()
        saved_page = test_data['model_instance']

        modelform = test_data['model_form_instance']
        self.assertTrue(modelform.is_new_entity(), 'Expected True since form is new')

        modelform.instance = saved_page
        self.assertFalse(modelform.is_new_entity(), 'Expected False since page on form is already saved in database')


    def test_child_is_a_derived_class_of_grandparent(self):
        test_data = self._generate_derived_class_test_data()

        grand_parent_class = test_data['grand_parent_class']
        child_class = test_data['child_class']

        self.assertFalse(child_class is grand_parent_class, 'Expected False')
        self.assertTrue(XFModelForm.is_a(child_class, grand_parent_class),
                        'Expected child class to be derived class of grand parent class')
