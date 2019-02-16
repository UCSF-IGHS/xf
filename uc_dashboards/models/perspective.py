from django.db import models

from xf.uc_dashboards.models.page import Page
from xf.uc_dashboards.models.tag import Tag


class PerspectiveManager(models.Manager):

    def get_by_natural_key(self, code):
        return self.get(code=code)


class Perspective(models.Model):
    objects = PerspectiveManager()
    name = models.CharField(
        max_length=255,
        help_text='The name of this perspective.')
    code = models.CharField(
        max_length=128,
        help_text='A code for this perspective. The code will be used to preset filters.',
        blank=True)
    pages = models.ManyToManyField(
        Page,
        related_name='perspectives',
        blank=True,
        help_text='The pages that are part of this perspective.')
    slug = models.SlugField(
        max_length=150,
        null=True, blank=True,
        help_text='This field identifies part of the URL that makes it friendly')
    default_page = models.ForeignKey(
        Page,
        help_text='The default page that will be displayed when a user logs on.')
    comment = models.TextField(
        blank=True,
        help_text='Any comment.')
    tags = models.ManyToManyField(Tag, related_name='perspectives', blank=True)

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name
