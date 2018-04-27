from django.core.exceptions import ValidationError
from django.test import TestCase

class XFTestCase(TestCase):

    def assertFieldClean(self, class_type, field_name, value):
        self.assertModelClean(class_type, {field_name : value}, {field_name})

    def assertFieldNotClean(self, class_type, field_name, value):
        self.assertModelNotClean(class_type, {field_name : value})

    def assertModelClean(self, class_type, model_values, not_expected_field_errors = None):

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        try:
            model.clean()
        except ValidationError as ex:
            if not_expected_field_errors is None:
                self.fail("Clean raised ValidationError unexpectedly and no non-expected field errors were provided")
            else:
                for key in ex.message_dict:
                    if key in not_expected_field_errors:
                        self.fail("Clean raised ValidationError unexpectedly for %s" % (key))

    def assertModelNotClean(self, class_type, model_values, expected_field_errors = {}):

        model = class_type()
        for (field_name, value) in model_values.items():
            setattr(model, field_name, value)

        if expected_field_errors is None:
            expected_field_errors = model_values.keys()

        with self.assertRaises(ValidationError) as ex:
            model.clean()

        for field_name in expected_field_errors:
            self.assertIn(field_name, ex.exception.message_dict)

