
import modeltranslation
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import TextInput, Textarea
from django.db import models
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from modeltranslation.admin import TranslationAdmin

from xf.uc_dashboards.models import HTMLField, GroupProfile, UserProfile, NavigationSection, Page, Template, PageType, \
    PageStatus, PageSection, Widget, Tag
from xf.uc_dashboards.models.dataset import DataSet
from xf.uc_dashboards.models.perspective import Perspective
from xf.uc_dashboards.models.xf_viz_site_settings import XFVizSiteSettings
from xf.xf_system.models import XFSiteSettings


class NavigationSectionAdmin(TranslationAdmin):
    list_display  = ('caption', 'index', 'parent_section')

class TagAdmin(admin.ModelAdmin):
    pass

class PageStatusAdmin(TranslationAdmin):
    pass

class PerspectivesInline(admin.TabularInline):
    model = Perspective.pages.through

class PageAdmin(TranslationAdmin):
    list_display = ('title', 'main_title', 'slug', 'section', 'allow_anonymous', 'template', 'page_type', 'navigation_section', 'page_id', 'index')
    list_filter = ('tags', 'template', 'page_type', 'navigation_section')
    save_as = True;
    formfield_overrides = {HTMLField: {'widget': forms.Textarea(attrs={'class': 'ckeditor'})}, }
    inlines = [PerspectivesInline,]

    class Media:
        js = ('gla/more/configuration-ckeditor.js',)




class PageSectionAdmin(TranslationAdmin):
    list_display = ('title',)

class GroupProfileAdmin(admin.ModelAdmin):
    pass

class PageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_section')




class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'template_source', 'template_path')
    list_filter = ('tags', 'template_type', 'template_source')
    save_as = True;

class PerspectiveAdmin(TranslationAdmin):
    list_display = ('name', 'code', 'slug')
    list_filter = ('tags', )
    save_as = True;

#class GroupPerspectiveAdmin(admin.ModelAdmin):
#    list_display = ('name', 'group', 'perspective')
#    list_filter = ('tags', )
#    save_as = True;


class DataSetAdmin(admin.ModelAdmin):

    list_display = ('name', 'code', 'dataset_type', 'database_key')
    list_filter = ('dataset_type',)
    save_as = True
    formfield_overrides = {HTMLField: {'widget': forms.Textarea(attrs={'class': 'ckeditor'})}, }
    fieldsets = (
        ('General', {
            'fields': ('name', 'code', 'dataset_type', 'custom_daset_loader', 'permissions_to_view', 'allow_anonymous', 'external_source_url', )
        }),
        ('SQL', {
            'classes': ('collapse',),
            'fields': ('database_key', 'sql_query', )
        }),

        ('Data', {
            'classes': ('collapse',),
            'fields': ('filters', 'data_columns',)
        }),

        ('Other', {
            'classes': ('collapse',),
            'fields': ('custom_attributes',),
        }),
    )



class WidgetTypeAdmin(TranslationAdmin):

    list_display = ('title', 'slug', 'allow_anonymous', 'template', 'widget_type', 'widget_id', 'code')
    list_filter = ('tags', 'template', 'widget_type')
    save_as = True;
    formfield_overrides = {HTMLField: {'widget': forms.Textarea(attrs={'class': 'ckeditor'})}, }
    fieldsets = (
        ('General', {
            'fields': ('title', 'slug', 'code', 'permissions_to_view', 'allow_anonymous', 'widget_id', 'template', 'widget_type', 'user_description', 'view_details_url', 'tags')
        }),
        ('SQL', {
            'classes': ('collapse',),
            'fields': ('dataset', 'sql_query', 'filters', 'database_key')
        }),

        ('Data', {
            'classes': ('collapse',),
            'fields': ('data_columns', 'sub_text', 'data_point_column', 'label_column',)
        }),

        ('Other', {
            'classes': ('collapse',),
            'fields': ('text', 'custom_attributes'),
        }),
    )

    class Media:
        js = ('gla/more/configuration-ckeditor.js',)

# config.allowedContent = true;

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'group profile'

# Define a new User admin
class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupProfileInline, )
    list_filter = ('profile__tags', )


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_filter = ('profile__tags', )

# Define a new XF SIte settings admin
class XFSiteSettingsAdmin(admin.ModelAdmin):
    model = XFSiteSettings


class XFVizSiteSettingsInline(admin.StackedInline):
    model = XFVizSiteSettings
    can_delete = False
    verbose_name_plural = 'dashboard settings'


# Define a new User admin
class XFVizSiteSettingsAdmin(XFSiteSettingsAdmin):
    inlines = (XFVizSiteSettingsInline, )

# Register your models here.
admin.site.register(NavigationSection, NavigationSectionAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(PageType, PageTypeAdmin)
admin.site.register(PageStatus, PageStatusAdmin)
admin.site.register(PageSection, PageSectionAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(Widget, WidgetTypeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Perspective, PerspectiveAdmin)
#admin.site.register(GroupPerspective, GroupPerspectiveAdmin)
#admin.site.register(GroupProfile, TagAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(XFSiteSettings)
admin.site.register(XFSiteSettings, XFVizSiteSettingsAdmin)
