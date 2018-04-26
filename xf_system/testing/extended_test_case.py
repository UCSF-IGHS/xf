from django.core.exceptions import ValidationError
from django.test import TestCase

class ExtendedTestCase(TestCase):
    pass

    def assertClean(self, class_type, field_name, value):

        model = class_type()
        setattr(model, field_name, value)

        try:
            model.clean()
        except ValidationError:
            self.fail("Clean raised ValidationError unexpectedly")
        pass


    def assertNotClean(self, class_type, field_name, value):

        model = class_type()
        setattr(model, field_name, value)

        with self.assertRaises(ValidationError) as ex:
            model.clean()
        self.assertIn(field_name, ex.exception.message_dict)