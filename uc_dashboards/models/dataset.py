from django.contrib.auth.models import Group
from django.db import models


class DataSetManager(models.Manager):

    def get_by_natural_key(self, code):
        return self.get(code=code)


class DataSet(models.Model):

    SQL = '1'
    CUSTOM = '2'

    DATASET_TYPE_CHOICES = (
        (SQL, 'SQL'),
        (CUSTOM, 'Custom built'),
    )

    name = models.CharField(
        max_length=150,
        help_text='Name of the dataset. Shows in dropdown lists'
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        help_text='A code that can be used to uniquely identify this dataset.'
    )
    dataset_type = models.CharField(
        max_length=2,
        choices=DATASET_TYPE_CHOICES,
        default=SQL,
        help_text='The type of dataset'
    )
    custom_daset_loader = models.CharField(
        max_length=255,
        blank=True,
        help_text='Only for complex datasets that are built in code. Provide a fully qualified class that implements '
                  'XFCustomDataSetLoaderBase'
    )
    permissions_to_view = models.ManyToManyField(
        Group, blank=True,
        help_text='Specifies the groups that may access this dataset'
    )
    allow_anonymous = models.BooleanField(
        blank=True,
        help_text='Specifies whether anonymous access is allowed for this dataset'
    )
    external_source_url = models.CharField(
        max_length=255,
        blank=True,
        help_text='A URL specifiying a REST API link. Use this if data will be queried externally'
    )
    sql_query = models.TextField(
        blank=True,
        help_text='The SQL query to run to get the data. Use this if data will be queried from database specified by '
                  'the database key below'
    )
    filters = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Quoted and comma-separated list of string values with filter names from the query string"
    )
    data_columns = models.TextField(
        blank=True,
        help_text="All columns in this dataset. One per line. Must be a Python dictionary format."
    )
    database_key = models.CharField(
        max_length=150, blank=True,
        help_text='The key from the settings file to use for the data connection for this widget.'
    )
    custom_attributes = models.TextField(
        blank=True,
        help_text='Any custom attributes. Must be a Python dictionary format.'
    )

    class Meta:
        unique_together = (('code',),)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name
