from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group

from django.db.models.signals import post_save, pre_init, post_init
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

@receiver(post_init, sender=User)
def create_user_profile_on_post_init(sender, instance, **kwargs):
    # If, for some reason, the user doesn't have a profile, create one on the fly
    if not hasattr(instance, 'profile'):
        instance.profile = UserProfile()



class HTMLField(RichTextUploadingField):
    pass


# Create your models here.

### Navigation models

class Tag(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

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

    def __str__(self):
        return self.caption



class Template(models.Model):
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


    def __str__(self):
        return self.name


### Content models

class PageSection(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class PageType(models.Model):
    name = models.CharField(max_length=150)
    url_section = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

class PageStatus(models.Model):
    code = models.CharField(
        max_length=50,
        help_text='Code of the status.')
    name = models.CharField(
        max_length=150,
        help_text='Name of the status.')

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(
        max_length=150,
        help_text='Title of the page. Also appears in the navigation bar.')
    main_title = models.CharField(
        max_length=150,
        help_text='Main title on top of the page')
    text = HTMLField(blank=True)
        #text = HTMLField('Approve place', null=True, blank=True)

    slug = models.SlugField(
        max_length=150,
        help_text='This field identifies part of the URL that makes it friendly')
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

    show_filter_bar = models.BooleanField(blank=True, help_text='Check this field if you want to display the filter bar. Otherwise it will be hidden.')
    index = models.IntegerField(blank=True, default=0, help_text='Pages with a lower index will be added to the navigation tree before those with a higher index. This is used to sort the navigation tree.')
    tags = models.ManyToManyField(Tag, related_name='pages', blank=True)
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



    def __str__(self):
        return self.title


class Perspective(models.Model):
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

    def __str__(self):
        return self.name




class Widget(models.Model):
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
    OTHER = '0'

    WIDGET_TYPE_CHOICES = (
        (PIE, 'Pie'),
        (TABLE, 'Table'),
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
        help_text = 'A URL specifiying a details link. This could be another dashboard, or a JasperReport. '
    )
    code = models.CharField(
        max_length=255,
        blank=True,
        help_text = 'A code that can be used to identify this widget. The code will be displayed in the "About this widget" box.'
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


### Extensions of the user and groups model



class GroupProfile(models.Model):
    '''
    A group profile extends the normal Django group with extra fields. A 1:1 relationship exists here, and a
    custom admin has been defined to make this show up in the admin interface.
    '''
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="profile")
    perspectives = models.ManyToManyField(
        Perspective,
        related_name='group_perspectives',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='group_profiles',
        blank=True
    )
    preset_filters = models.TextField(
        blank=True,
        help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives'
    )
    comment = models.TextField(
        blank=True,
        help_text='Any comment.'
    )

    def save(self, *args, **kwargs):
    #See https://stackoverflow.com/questions/6117373/django-userprofile-m2m-field-in-admin-error/6117457#6117457

        print("user profile saved")
        if not self.pk:
            try:
                p = GroupProfile.objects.get(group=self.group)
                self.pk = p.pk
            except GroupProfile.DoesNotExist:
                pass

        super(GroupProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=Group)
def create_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)

@receiver(post_save, sender=Group)
def save_group_profile(sender, instance, **kwargs):
    instance.profile.save()



class UserProfile(models.Model):
    '''
    Extends the standard user profile
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    tags = models.ManyToManyField(
        Tag,
        related_name='user_profiles',
        blank=True
    )
    preset_filters = models.TextField(
        blank=True,
        help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives'
    )
    default_perspective = models.ForeignKey(
        Perspective,
        null= True,
        blank = True,
        help_text='The default perspective for this user. May be null if the user only has one perspective from their groups. If the perspective is not part of a group, the default perspective will be added.')
    comment = models.TextField(
        blank=True,
        help_text='Any comment.'
    )

    def save(self, *args, **kwargs):
    #See https://stackoverflow.com/questions/6117373/django-userprofile-m2m-field-in-admin-error/6117457#6117457

        print("user profile saved")
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass

        super(UserProfile, self).save(*args, **kwargs)