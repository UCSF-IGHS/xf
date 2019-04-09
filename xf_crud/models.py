from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class XFCodeTableManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class XFCodeTable(models.Model):
    objects = XFCodeTableManager()
    all_choices = models.Manager()

    code = models.IntegerField(null=False, blank=False, unique=True,
                               validators=[
                                   MaxValueValidator(1000),
                                   MinValueValidator(0)
                               ],
                               )
    name = models.CharField(max_length=255, null=False, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "(%s - %s)" % (self.code, self.name)

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('code'),)

    def natural_key(self):
        return (self.code,)
