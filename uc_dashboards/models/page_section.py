import uuid

from django.db import models


class PageSectionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class PageSection(models.Model):
    objects = PageSectionManager()
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50,
                            default=uuid.uuid4,
                            help_text='User-defined code for this template',
                            blank=False,
                            null=False, )

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.title
