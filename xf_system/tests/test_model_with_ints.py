from xf.xf_system.testing.xf_test_case import XFTestCase
from xf.xf_system.tests.test_models import TestModelWithInts


class ValidateTestModelWithInts(XFTestCase):

    def test_model_is_clean(self):

        # Test should pass, and we're not looking for b, so we need to pass the fields we're interested in
        test_data = {'int_c' : 6, 'int_d' : 7}
        self.assertModelClean(TestModelWithInts, test_data, test_data.keys())

        # Test should pass, and we're not looking for b
        test_data = {'int_b' : -2}
        self.assertModelClean(TestModelWithInts, test_data)

        # This test should pass, even though b is None, because we're only looking for 'int_a'
        test_data = {'int_a' : 5}
        self.assertModelClean(TestModelWithInts, test_data, 'int_a')


    def test_model_is_not_clean(self):

        test_data = {'int_c' : 6, 'int_d' : 5}
        self.assertModelNotClean(TestModelWithInts, test_data, {'int_c'})

        test_data = {'int_c' : 4, 'int_d' : 5}
        self.assertModelNotClean(TestModelWithInts, test_data)

        test_data = {'int_c' : 6, 'int_d' : 6}
        self.assertModelNotClean(TestModelWithInts, test_data, {'int_c', 'int_d'})
        self.assertModelNotClean(TestModelWithInts, test_data, None)

    def test_int_a(self):
        self.assertFieldClean(TestModelWithInts, 'int_a', 0)
        self.assertFieldClean(TestModelWithInts, 'int_a', None)
        self.assertFieldClean(TestModelWithInts, 'int_a', 1)
        self.assertFieldClean(TestModelWithInts, 'int_a', 5)
        self.assertFieldClean(TestModelWithInts, 'int_a', 100)
        self.assertFieldNotClean(TestModelWithInts, 'int_a', -2)
        self.assertFieldNotClean(TestModelWithInts, 'int_a', 101)

    def test_int_b(self):
        self.assertFieldNotClean(TestModelWithInts, 'int_b', 0)
        self.assertFieldNotClean(TestModelWithInts, 'int_b', None)
        self.assertFieldClean(TestModelWithInts, 'int_b', -1)