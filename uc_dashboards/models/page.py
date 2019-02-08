from django.contrib.auth.models import Group
from django.db import models

from xf.uc_dashboards.models.html_field import HTMLField
from xf.uc_dashboards.models.navigation_section import NavigationSection
from xf.uc_dashboards.models.page_section import PageSection
from xf.uc_dashboards.models.page_status import PageStatus
from xf.uc_dashboards.models.page_type import PageType
from xf.uc_dashboards.models.tag import Tag
from xf.uc_dashboards.models.template import Template


class PageManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Page(models.Model):
    objects = PageManager()
    title = models.CharField(
        max_length=150,
        help_text='Title of the page. Also appears in the navigation bar.')
    main_title = models.CharField(
        max_length=150,
        help_text='Main title on top of the page')
    text = HTMLField(blank=True)
    # text = HTMLField('Approve place', null=True, blank=True)

    slug = models.SlugField(
        max_length=150,
        help_text='This field identifies part of the URL that makes it friendly'
    )
    permissions_to_view = models.ManyToManyField(
        Group, blank=True,
        help_text='Specifies the groups that may view this page')
    allow_anonymous = models.BooleanField(
        blank=True,
        help_text='Specifies whether anonymous browsing is allowed for this page')
    section = models.ForeignKey(
        PageSection,
        help_text='Taxonomy classification of this page. Helps to form a pretty URL.')
    navigation_section = models.ForeignKey(
        NavigationSection, blank=True, null=True,
        related_name='page',
        help_text='Specifies the navigation item to link this item to. Do not specify this if a parent page is set')
    parent_page = models.ForeignKey(
        "Page", blank=True, null=True,
        related_name='childma_page',
        help_text='Specifies a parent page for this item. Leave this empty if a page is immediately below a navigation section ')

    page_id = models.CharField(
        max_length=50,
        help_text="Can be used in the view to load a specific set of context data, e.g. a dashboard",
        blank=True, null=True)
    template = models.ForeignKey(Template,
                                 help_text='The template to be used to render this page. May be overridden by the view.')
    page_type = models.ForeignKey(PageType, default=1,
                                  help_text='Determines if this is a normal page, or a dashboard')

    show_filter_bar = models.BooleanField(blank=True,
                                          help_text='Check this field if you want to display the filter bar. Otherwise it will be hidden.')
    index = models.IntegerField(blank=True, default=0,
                                help_text='Pages with a lower index will be added to the navigation tree before those with a higher index. This is used to sort the navigation tree.')
    tags = models.ManyToManyField(Tag, related_name='pages', blank=True, null=True)
    page_status = models.ForeignKey(
        PageStatus, blank=True, null=True,
        related_name='page_status',
        help_text='Specifies a the status of this page')
    data_sources = HTMLField(blank=True, null=True,
                             help_text='Specify the data sources for this page, if applicable.')
    about = HTMLField(blank=True, null=True,
                      help_text='Allows you to specify "about" information for this page, e.g. methods.')

    widgets = models.TextField(
        blank=True,
        help_text='A python dictionary specifiying widget slugs for this template.'
    )

    custom_attributes = models.TextField(
        blank=True,
        help_text='Any custom attributes, which may be forwarded to the template. Must be a Python dictionary format.'
    )

    class Meta:
        unique_together = (('slug',),)

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.title
