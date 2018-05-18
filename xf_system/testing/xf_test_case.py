from django.core.exceptions import ValidationError
from django.test import TestCase

class XFTestCase(TestCase):

    def assertFieldClean(self, class_type, field_name, value, message = None):
        field_message = "%s - %s" % (field_name, message)
        self.assertModelClean(class_type, {field_name : value}, {field_name}, field_message)

    def assertFieldNotClean(self, class_type, field_name, value, message=None):
        field_message = "%s - %s" % (field_name, message)
        expected_clean_field = {field_name}
        self.assertModelNotClean(class_type, {field_name : value}, expected_clean_field, message=field_message)

    def assertModelClean(self, class_type, model_values, expected_clean_fields = None, message = None):
        '''
        Asserts that a model is clean. You need to specify which fields you expect to be clean. This method
        will succeed as long as those fields are clean, even if other fields don't validate.
        :param class_type: The model to assert
        :param model_values: A dictionary setting the fields and values to be tested
        :param expected_clean_fields: The fields that are expected to be clean
        :param message: Any message to display if the test fails.
        :return:
        '''

        # Non-expected-field-errors contains a list of fields that we expect should NOT throw an error
        # So, if we pass field_a, then we expect field_a not to throw an error here
        # If field_a does throw an error, then we have a problem
        # So, it is basically a list of fields that we expect to be clean

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        try:
            model.clean()
        except ValidationError as ex:
            if expected_clean_fields is None:
                self.fail(message if message is not None else
                          "Clean raised ValidationError unexpectedly and no fields were expected to throw an error")
            else:
                for key in ex.message_dict:
                    if key in expected_clean_fields:
                        self.fail(message if message is not None else
                                  "Clean raised ValidationError unexpectedly for %s" % (key))

    def assertModelNotClean(self, class_type, model_values, expected_field_errors = None, message = None):
        '''
        Asserts that a model is not clean.
        :param class_type: The model to assert
        :param model_values: A dictionary setting the fields and values to be tested
        :param expected_field_errors: The fields that are expected to be not clean
        :param message: Any message to display if the test fails
        :return:
        '''

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        if expected_field_errors is None:
            expected_field_errors = model_values.keys()

        with self.assertRaises(ValidationError, msg = message) as ex:
            model.clean()

        for field_name in expected_field_errors:
            self.assertIn(field_name, ex.exception.message_dict, message)

    def assertFieldRequired(self, model_class_type, field_name, message=None):
        '''
        Asserts that a field is required. Rather, it asserts that a ValidationError of any kind if produced
        if the field_name on model_class_type is set to None
        :param model_class_type: The model to assert
        :param field_name: The field to be tested for None
        :param message: Any message to display if the test fails
        :return:
        '''

        model = model_class_type()
        setattr(model, field_name, None)

        # Expect a ValidtionError
        with self.assertRaises(ValidationError, msg = message) as ex:
            model.full_clean()

        # Make sure we have a ValidationError for our specific field
        self.assertIn(field_name, ex.exception.message_dict, message)

