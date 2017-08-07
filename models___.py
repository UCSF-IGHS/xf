from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group


class Tag(models.Model):

    text = models.CharField(max_length=255)

    def __unicode__(self):
        return self.text

class NavigationLink(models.Model):
    caption = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    icon = models.CharField(
        max_length=50,
        blank=True)
    tags = models.ManyToManyField(Tag, related_name='navigation_links', blank=True)
    parent_navigation_link = models.ForeignKey(
        'self', related_name='child_navigation_links', blank=True, null=True,
        help_text='Specify a parent navigation section, or leave it empty if it is a top section')


    def __unicode__(self):
        return self.caption





class NavigationSection(models.Model):
    caption = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    parent_section = models.ForeignKey(
        'self', related_name='child_sections', blank=True, null=True,
        help_text='Specify a parent navigation section, or leave it empty if it is a top section')
    icon = models.CharField(
        max_length=50,
        blank=True)
    index = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='navigation_sections', blank=True)

    def clean(self):
        if self.parent_section:
            if self.parent_section.parent_section:
                raise ValidationError('Nested navigation items are not currently supported beyond one level.')

    def __unicode__(self):
        return self.caption