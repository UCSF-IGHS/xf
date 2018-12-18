from xf.tests.xf_test_case_data import XFTestCaseData


class XFModelFormTestCase(XFTestCaseData):

    def test_is_new_entity(self):

        test_data = self._generate_permissions_test_data()
        saved_page = test_data['model_instance']

        modelform = test_data['model_form_instance']
        self.assertTrue(modelform.is_new_entity(), 'Expected True since form is new')

        modelform.instance = saved_page
        self.assertFalse(modelform.is_new_entity(), 'Expected False since page on form is already saved in database')
