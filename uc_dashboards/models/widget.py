from django.contrib.auth.models import Group
from django.db import models

from xf.uc_dashboards.models.dataset import DataSet
from xf.uc_dashboards.models.html_field import HTMLField
from xf.uc_dashboards.models.tag import Tag
from xf.uc_dashboards.models.template import Template


class WidgetManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Widget(models.Model):
    objects = WidgetManager()

    PIE = '1'
    TABLE = '2'
    TILES = '3'
    EASY_PIE = '4'
    LINE_GRAPH = '5'
    BAR_GRAPH = '6'
    DOUGHNUT_GRAPH = '7'
    MAP = '8'
    TEXT_BLOCK = '9'
    PROGRESS_CIRCLE = '10'
    FILTER_DROP_DOWN = '11'
    BAR_GRAPH_HORIZONTAL = '12'
    GAUGE = '13'
    STACKED_BAR_GRAPH = '14'
    PAGED_TABLE = '15'
    OTHER = '0'

    WIDGET_TYPE_CHOICES = (
        (PIE, 'Pie'),
        (TABLE, 'Table'),
        (PAGED_TABLE, 'Paged table'),
        (TILES, 'Tiles'),
        (EASY_PIE, 'Easy pie'),
        (LINE_GRAPH, 'Line graph'),
        (BAR_GRAPH, 'Bar graph Vertical'),
        (BAR_GRAPH_HORIZONTAL, 'Bar graph Horizontal'),
        (DOUGHNUT_GRAPH, 'Doughnut graph'),
        (PROGRESS_CIRCLE, 'Progress circle'),
        (MAP, 'Map'),
        (TEXT_BLOCK, 'Text block'),
        (FILTER_DROP_DOWN, 'Filter drop down'),
        (GAUGE, 'Gauge'),
        (STACKED_BAR_GRAPH, 'Stacked bar graph'),
        (OTHER, 'Other'),
    )

    title = models.CharField(
        max_length=150,
        help_text='Title of the widget.')
    slug = models.SlugField(
        max_length=150,
        help_text='This field identifies part of the URL that makes it friendly')

    permissions_to_view = models.ManyToManyField(
        Group, blank=True,
        help_text='Specifies the groups that may view this widget')
    allow_anonymous = models.BooleanField(
        blank=True,
        help_text='Specifies whether anonymous browsing is allowed for this widget')
    widget_id = models.CharField(
        max_length=50,
        help_text="Can be used in the view to load a specific set of context data",
        blank=True, null=True)
    template = models.ForeignKey(
        Template,
        help_text='The template to be used to render this widget. May be overridden by the view.')
    widget_type = models.CharField(
        max_length=2,
        choices=WIDGET_TYPE_CHOICES,
        default=OTHER,
        help_text='The type of widget'
    )
    dataset = models.ForeignKey(
        DataSet, blank=True, null=True,
        help_text='A previously prepared dataset that will be used to load the data.')
    sql_query = models.TextField(
        blank=True,
        help_text='Tables/Pie: The SQL query to run with this widget'
    )
    filters = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Quoted and comma-separated list of string values with filter names from the query string"
    )
    data_columns = models.TextField(
        blank=True,
        help_text="Tables/Pie: Data columns to use. One per line. Must be a Python dictionary format."
    )
    sub_text = models.TextField(
        blank=True,
        help_text="Pie: text to show below the pie."
    )
    data_point_column = models.TextField(
        blank=True,
        help_text="Pie: the column that has the data points for a pie. Must be a Python dictionary format."
    )
    label_column = models.TextField(
        blank=True,
        help_text="Pie: the column that has the labels to be shown in the pie"
    )
    text = HTMLField(
        blank=True,
        help_text='If this is a text widget, the text will be displayed in the widget. Useful for static widgets.'
    )
    database_key = models.CharField(
        max_length=150,
        help_text='The key from the settings file to use for the data connection for this widget.')
    custom_attributes = models.TextField(
        blank=True,
        help_text='Any custom attributes. Must be a Python dictionary format.'
    )
    view_details_url = models.CharField(
        max_length=255,
        blank=True,
        help_text='A URL specifiying a details link. This could be another dashboard, or a JasperReport. '
    )
    code = models.CharField(
        max_length=255,
        blank=True,
        help_text='A code that can be used to identify this widget. The code will be displayed in the "About this widget" box.'
    )
    user_description = HTMLField(
        blank=True,
        help_text='A description that helps the user understand what this widget shows. It will be shown in a pop-up window. '
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='widgets',
        blank=True
    )

    class Meta:
        unique_together = (('slug',),)

    def natural_key(self):
        return (self.slug,)
