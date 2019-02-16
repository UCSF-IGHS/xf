import uuid

from django.core.exceptions import ValidationError
from django.db import models

from xf.uc_dashboards.models.tag import Tag


class NavigationSectionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class NavigationSection(models.Model):
    objects = NavigationSectionManager()
    caption = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    parent_section = models.ForeignKey(
        'self', related_name='child_sections', blank=True, null=True,
        help_text='Specify a parent navigation section, or leave it empty if it is a top section')
    icon = models.CharField(
        max_length=50,
        blank=True)
    tags = models.ManyToManyField(Tag, related_name='navigation_sections', blank=True)
    code = models.CharField(max_length=50,
                            default=uuid.uuid4,
                            help_text='User-defined code for this template',
                            null=False,
                            blank=False)

    def clean(self):
        if self.parent_section:
            if self.parent_section.parent_section:
                raise ValidationError('Nested navigation items are not currently supported beyond one level.')

    def __str__(self):
        return self.caption

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)
