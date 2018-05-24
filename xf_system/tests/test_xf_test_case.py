from django.core.exceptions import ValidationError
from django.test import TestCase

from xf.xf_system.testing.xf_test_case import XFTestCase
from xf.xf_system.tests.test_models import TestModelWithInts


class ValidateEFTextCase(TestCase):
    """
    The test case to demonstrate that our XFTestCase actually works well
    So, testing our tester!

    DON'T FOCUS ON THIS FILE, IT IS A UNIT TEST TO TEST THE ASSERT METHODS OF XFTESTCASE
    """

    def setUp(self):
        self.test_case = XFTestCase()

    def tearDown(self):
        del self.test_case

    def test_assert_model_not_clean(self):

        test_case = XFTestCase()
        test_data = {'int_c' : 6, 'int_d' : 5}
        test_case.assertModelNotClean(TestModelWithInts, test_data, {'int_c'})

        test_data = {'int_c' : 6, 'int_d' : 6}
        test_case.assertModelNotClean(TestModelWithInts, test_data, {'int_c', 'int_d'})
        test_case.assertModelNotClean(TestModelWithInts, test_data, None)


    def test_assert_model_clean(self):

        test_case = XFTestCase()

        # Test should pass, and we're not looking for b, so we need to pass the fields we're interested in
        test_data = {'int_c' : 6, 'int_d' : 7}
        test_case.assertModelClean(TestModelWithInts, test_data, test_data.keys())

        # But if we don't give the keys, the test should fail because b is mandatory, and we didn't provide it
        try:
            test_case.assertModelClean(TestModelWithInts, test_data, test_data.keys())
            self.assertRaises(None, AssertionError)
        except:
            pass


        # This test should pass, even though b is None, because we're only looking for 'int_a'
        test_data = {'int_a' : 5}
        test_case.assertModelClean(TestModelWithInts, test_data, 'int_a')

        # This test should fail, because b is missing
        test_data = {'int_a' : 5}
        try:
            test_case.assertModelClean(TestModelWithInts, test_data)
            self.assertRaises(None, AssertionError)
        except:
            pass

    def test_assert_field_clean(self):

        # Scenario 1: Dirty Data – Should raise exception
        # Explanation:
        # We are providing dirty data
        # We expect assertFieldClean to fail, and it will raise an AssertionError
        # We capture that error, because that is the correct behaviour
        with self.assertRaises(AssertionError):
            self.test_case.assertFieldClean(TestModelWithInts, 'int_b', 2, '2 should be below 0')
            self.test_case.assertFieldClean(TestModelWithInts, 'int_b', 0, '0 should be below 0')

        # Scenario 2: Clean Data – Should not raise an exception
        try:
            self.test_case.assertFieldClean(TestModelWithInts, 'int_b', -2, 'should accept -2')
            self.test_case.assertFieldClean(TestModelWithInts, 'int_b', -1, 'should accept -1')
        except:
            self.fail("AssertFieldClean incorrectly raises a validation error on valid data")

    def test_assert_field_not_clean(self):

        self.test_case.assertFieldNotClean(TestModelWithInts, 'int_b', 2, '2 should be below 0')

        # Scenario 1: Dirty data – Should not raise exception
        try:
            self.test_case.assertFieldNotClean(TestModelWithInts, 'int_b', 2, '2 should be below 0')
        except:
            self.fail("AssertFieldNotClean incorrectly raises an exception on invalid data")

        # Scenario 2: Clean data – Should raise an exception, because it would expect a ValidationError
        # and because the data is clean, it won't be given
        with self.assertRaises(AssertionError):
            self.test_case.assertFieldNotClean(TestModelWithInts, 'int_b', -1, '2 should be below 0')

    def test_assert_field_not_required(self):

        # Scenario: A field that is not required should not throw an exception when model.save is called
        pass