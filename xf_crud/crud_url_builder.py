from django.conf.urls import url

from xf.xf_crud.generic_crud_views import XFDetailView, XFUpdateView, XFDeleteView, XFCreateView
from xf.xf_crud.generic_list_views import XFListView, XFRelatedListView, XFCSVContentView
from xf.xf_crud.model_forms import XFModelForm
from xf.xf_crud.model_lists import XFModelList
from xf.xf_crud.xf_crud_helpers import mmodelform_factory


class XFException(Exception):
    """
    An exception that is raised by the XF Framework
    """
    pass


class XFCrudURLBuilder:

    def __init__(self, url_app_name, url_model_name, model_type):

        self.url_app_name = url_app_name
        self.url_model_name = url_model_name
        self.model_type = model_type

    def get_overview_url(self,
                         url_operation_name="overview",
                         view_class_type=None,
                         form_class_type=None,
                         ):
        """
        Used to generate an "overview" URL. You should specify an instance of a XFMasterChildView.
        """

        if view_class_type is None:
            raise XFException("You must specify an overview view class type. You cannot rely on the default class here.")

        return self._generate_form_instance_url(url_operation_name, view_class_type, form_class_type)
        pass

    def get_details_url(self,
                        url_operation_name="details",
                        view_class_type=XFDetailView,
                        form_class_type=None,
                        ):
        return self._generate_form_instance_url(url_operation_name, view_class_type, form_class_type)

    def get_edit_url(self,
                     url_operation_name="edit",
                     view_class_type=XFUpdateView,
                     form_class_type=XFModelForm,
                     ):
        return self._generate_form_instance_url(url_operation_name, view_class_type, form_class_type)

    def get_delete_url(self,
                       url_operation_name="delete",
                       view_class_type=XFDeleteView,
                       form_class_type=XFModelForm,
                       ):
        return self._generate_form_instance_url(url_operation_name, view_class_type, form_class_type)

    def get_new_url(self,
                    url_operation_name="new",
                    view_class_type=XFCreateView,
                    form_class_type=XFModelForm,
                    ):
        return url(r'^%s/%s/new' % (self.url_app_name, self.url_model_name),
                   view_class_type.as_view(model=self.model_type, form_class=form_class_type,
                                           success_url="%s/%s/" % (self.url_app_name, self.url_model_name),
                                           app_name=self.url_app_name, model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name))

    def get_new_add_to(self,
                    url_operation_name="add_to",
                    view_class_type=XFCreateView,
                    form_class_type=XFModelForm,
                    ):
        return url(r'^%s/%s/new' % (self.url_app_name, self.url_model_name),
                   view_class_type.as_view(model=self.model_type, form_class=form_class_type,
                                           success_url="%s/%s/" % (self.url_app_name, self.url_model_name),
                                           app_name=self.url_app_name, model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name))


    def get_relational_list_url(self,
                                url_operation_name="overview",
                                view_class_type=XFDetailView,
                                form_class_type=XFModelForm,
                                ):
        return self._generate_form_instance_url(url_operation_name, view_class_type, form_class_type)


    def _generate_form_instance_url(self, operation_name, view_class_type, form_class_type):

        if form_class_type is None:
            try:
                form_class_type = mmodelform_factory(self.model_type, fields=self.model_type._meta.form_field_list)
            except:
                form_class_type = mmodelform_factory(self.model_type)

            form_class_type.Meta.title = self.url_model_name.capitalize()

        return url(r'^%s/%s/(?P<pk>[-\w]+)/%s' % (self.url_app_name, self.url_model_name, operation_name),
                   view_class_type.as_view(model=self.model_type,
                                           form_class=form_class_type,
                                           success_url="%s/%s/" % (self.url_app_name, self.url_model_name),
                                           app_name=self.url_app_name,
                                           model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name,
                                      self.url_model_name,
                                      operation_name))


    def get_list_url(self, url_operation_name="list",
                     view_class_type=XFListView,
                     list_class_type=XFModelList):

        # TODO:    list_class = list_class_type(model_type)
        return url(r'^%s/%s/' % (self.url_app_name, self.url_model_name),
                   view_class_type.as_view(model=self.model_type, generic=True,
                                           queryset=self.model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=self.url_app_name,
                                           model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name))


    def get_csv_url(self, url_operation_name="csv-export",
                    view_class_type=XFCSVContentView,
                    list_class_type=XFModelList):

        return url(r'^%s/%s/csv-export' % (self.url_app_name, self.url_model_name),
                   view_class_type.as_view(model=self.model_type, generic=True,
                                           queryset=self.model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=self.url_app_name,
                                           model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name))

    def get_list_preset_filter_url(self, url_operation_name="list_filter",
                                   view_class_type=XFListView,
                                   list_class_type=XFModelList):
        return url(r'^%s/%s/(?P<preset_filter>[-\w]+)' % (self.url_app_name, self.url_model_name),
                   view_class_type.as_view(model=self.model_type, generic=True,
                                           queryset=self.model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=self.url_app_name,
                                           model_url_part=self.url_model_name),
                   name="%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name))


    def get_list_related_url(self,
                             url_operation_name="list",
                             url_related_name="by-default",
                             foreign_key_name=None,
                             view_class_type=XFRelatedListView,
                             list_class_type=XFModelList):
        """
        Gets a URL that can be used to display related items. You must specify the foreign key name.
        """
        return url(r'^%s/%s/%s/(?P<related_fk>[-\w]+)' % (self.url_app_name, self.url_model_name, url_related_name),
                   view_class_type.as_view(model=self.model_type, generic=True,
                                           queryset=self.model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=self.url_app_name,
                                           model_url_part=self.url_model_name, foreign_key_name=foreign_key_name),
                   name="%s_%s_%s_%s" % (self.url_app_name, self.url_model_name, url_operation_name, url_related_name))

