from django.core.exceptions import ValidationError
from django.test import TestCase

class XFTestCase(TestCase):

    def assertFieldClean(self, class_type, field_name, value, message = None):
        field_message = "%s - %s" % (field_name, message)
        self.assertModelClean(class_type, {field_name : value}, {field_name}, field_message)

    def assertFieldNotClean(self, class_type, field_name, value, message = None):
        field_message = "%s - %s" % (field_name, message)
        self.assertModelNotClean(class_type, {field_name : value}, None, field_message)


    def assertModelClean(self, class_type, model_values, not_expected_field_errors = None, message = None):

        # Non-expected-field-errors contains a list of fields that we expect should NOT thrown an error
        # So, if we pass field_a, then we expect field_a not to throw an error here
        # If field_a does throw an error, then we have a problem

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        try:
            model.clean()
        except ValidationError as ex:
            if not_expected_field_errors is None:
                self.fail(message if message is not None else
                          "Clean raised ValidationError unexpectedly and no fields were expected to throw an error")
            else:
                for key in ex.message_dict:
                    if key in not_expected_field_errors:
                        self.fail(message if message is not None else
                                  "Clean raised ValidationError unexpectedly for %s" % (key))

    def assertModelNotClean(self, class_type, model_values, expected_field_errors = {}, message = None):

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        if expected_field_errors is None:
            expected_field_errors = model_values.keys()

        with self.assertRaises(ValidationError, msg = message) as ex:
            model.clean()

        for field_name in expected_field_errors:
            self.assertIn(field_name, ex.exception.message_dict, message)

