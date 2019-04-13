from datetime import date
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class XFCodeTableManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)

    def get_activated(self, deactivated_at: date):
        is_new = deactivated_at is None

        _queryset = super().get_queryset()
        _filter = Q(deactivated_at__isnull=True)

        if not is_new:
            _filter.add((Q(deactivated_at__gte=deactivated_at)), Q.OR)

        return _queryset.filter(_filter)


class XFCodeTable(models.Model):
    objects = XFCodeTableManager()

    code = models.IntegerField(null=False, blank=False, unique=True,
                               validators=[
                                   MaxValueValidator(1000),
                                   MinValueValidator(0)
                               ],
                               )
    name = models.CharField(max_length=255, null=False, blank=False)
    deactivated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return "(%s - %s)" % (self.code, self.name)

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('code'),)

    def natural_key(self):
        return (self.code,)
