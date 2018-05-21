from django.core.exceptions import ValidationError
from django.db import models

from xf.xf_crud.models import XFCodeTable


class SomeCodes(XFCodeTable):
    pass

    class Meta:
        managed = False

class TestModelWithInts(models.Model):
    int_a = models.IntegerField(blank=True, null=True)
    int_b = models.IntegerField(blank=True, null=True)
    int_c = models.IntegerField(blank=True, null=True)
    int_d = models.IntegerField(blank=True, null=True)
    int_e = models.IntegerField(blank=False, null=False)
    some_codes = models.ForeignKey(SomeCodes, blank=False, null=False)
    
    int_f = models.IntegerField(blank=True, null=True)

    def clean(self):

        validation_errors = {}

        if self.int_a is not None:
            if self.int_a < 0 or self.int_a > 100:
                validation_errors['int_a'] = "a should be between 0 and 100"

        if self.int_b  is not None:
            if self.int_b >= 0:
                validation_errors['int_b'] = "b should be below 0"

        if self.int_b is None:
            validation_errors['int_b'] = "b is required"

        if self.int_c  is not None and self.int_d  is not None:
            if self.int_c > self.int_d:
                validation_errors['int_c'] = "c cannot be greater than d"

            if self.int_c == self.int_d:
                validation_errors['int_c'] = "c cannot be equal to d"
                validation_errors['int_d'] = "d cannot be equal to c"

        if self.int_e == 6:
            if self.int_f is None:
                validation_errors['int_f'] = "F is required"

        if validation_errors:
            raise ValidationError(validation_errors)

        super().clean()

    class Meta:
        managed = False