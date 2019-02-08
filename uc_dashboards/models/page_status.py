from django.db import models

from xf.uc_dashboards.models.widget import Widget


class PageStatusManager(models.Manager):

    def get_by_natural_key(self, code):
        return self.get(code=code)


class PageStatus(models.Model):
    objects = PageStatusManager()
    code = models.CharField(
        max_length=50,
        help_text='Code of the status.',
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=150,
        help_text='Name of the status.')

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name
