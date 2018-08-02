from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class XFCodeTableManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class XFCodeTable(models.Model):
    objects = XFCodeTableManager()

    code = models.IntegerField(null=False, blank=False, unique=True,
                               validators=[
                                   MaxValueValidator(1000),
                                   MinValueValidator(0)
                               ],
                               )
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return "(%s - %s)" % (self.code, self.name)

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('code'),)

    def natural_key(self):
        return (self.code,)
