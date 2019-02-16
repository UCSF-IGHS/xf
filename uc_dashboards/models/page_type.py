import uuid
from django.db import models


class PageTypeManager(models.Manager):

    def get_by_natural_key(self, code):
        return self.get(code=code)


class PageType(models.Model):
    objects = PageTypeManager()
    name = models.CharField(max_length=150)
    url_section = models.CharField(max_length=150, blank=True)
    code = models.CharField(max_length=50,
                            help_text='User-defined code for this page type',
                            blank=False,
                            null=False
                            )

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name
