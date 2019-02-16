import uuid

from django.db import models

from xf.uc_dashboards.models.tag import Tag


class TemplateManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Template(models.Model):
    objects = TemplateManager()

    PAGE = '1'
    DASHBOARD = '2'
    WIDGET = '3'
    OTHER = '0'

    FILE = '1'
    DATABASE = '2'

    TEMPLATE_TYPE_CHOICES = (
        (PAGE, 'Page'),
        (DASHBOARD, 'Dashboard'),
        (WIDGET, 'Widget'),
        (OTHER, 'Other'),
    )

    TEMPLATE_SOURCE_CHOICES = (
        (FILE, 'File system'),
        (DATABASE, 'From database')
    )

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50,
                            help_text='User-defined code for this template',
                            blank=False,
                            null=False
                            )

    template_type = models.CharField(
        max_length=2,
        choices=TEMPLATE_TYPE_CHOICES,
        default=PAGE,
        help_text='The type of template'
    )
    template_source = models.CharField(
        max_length=2,
        choices=TEMPLATE_SOURCE_CHOICES,
        default=FILE,
        help_text='Specifies whether the template should be loaded from the file system, or from the database.'
    )
    template_path = models.CharField(max_length=255, blank=True)
    template_text = models.TextField(blank=True,
                                     help_text='Allows you to specificy the content of a template.')

    tags = models.ManyToManyField(Tag, related_name='templates', blank=True)
    built_in = models.BooleanField(
        blank=True,
        default=False,
        help_text='Specifies whether this is a built-in template, which should not be modified')

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name
