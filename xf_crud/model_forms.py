from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Model
from django.forms import DateInput
from django.forms.models import ModelForm, ModelChoiceField
#import floppyforms as forms
#from floppyforms.widgets import PasswordInput
from xf.xf_crud.model_lists import XFCrudAssetLoaderMixIn
from xf.xf_crud.widgets import StaticTextWidget, StaticSelectWidget, MissingTextInput, XFDatePickerInput


class XFAjaxForm(ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal mxlform'
        self.helper.label_class = 'col-lg-5'
        self.helper.field_class = 'col-lg-5'
        #self.helper.form_action = "accounthandler.changepwd.view"
        #print kwargs['initial']['form_action']

        try:
            if kwargs['initial']['form_action']:
                self.helper.form_action = kwargs['initial']['form_action']
        except:
            pass

        try:
            if kwargs['initial']['ajax']:
                self.helper.form_action = reverse("accounthandler.changepwd.view") + "?ajax"
                self.helper.form_tag = False
                print(self.helper.form_action)
        except:
            pass

        try:
            if kwargs['initial']['no-submit']:
                print(kwargs['initial']['no-submit'])
        except:
            self.helper.add_input(Submit('submit', 'Submit'))
            self.helper.add_input(Button('cancel', 'Cancel'))
            pass

        super(XFAjaxForm, self).__init__(*args, **kwargs)

class XFModelForm(ModelForm, XFCrudAssetLoaderMixIn):

    def __init__(self, *args, **kwargs):

        self.request = self.user = None
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
            if self.request is not None:
                self.user = self.request.user
            else:
                self.user = None


        super(XFModelForm, self).__init__(*args, **kwargs)

        self.js_assets = []
        self.css_assets = []
        self.make_xf_dateinputs()

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3 col-sm-3 col-xs-3'
        self.helper.field_class = 'col-lg-9 col-sm-9 col-xs-9'
        self.helper.form_action = ''  # redirect in the view
        self.helper.form_tag = False
        self.helper.help_text_inline = True  # means that I want <span> elements
        if self.request is not None:
            self.url_name = self.request.resolver_match.url_name # Can be used to derive the URL name, which can help you determine the action
            
            self.is_new = self.url_name.endswith('_new')
            self.is_add_to = self.url_name.endswith('_add_to')
            self.is_edit = self.url_name.endswith('_edit')
            self.is_details = self.url_name.endswith('_details')
            self.is_overview = self.url_name.endswith('_overview')



    def disable_initial_fields(self):
        for field in self.initial:
            if field in self.fields:
                self.fields[field].disabled = True

    def make_readonly(self):

        self.helper.form_class += ' form-static'
        self.helper.label_class = 'col-lg-5 col-sm-5 col-xs-5'
        self.helper.field_class = 'col-lg-7 col-sm-7 col-xs-7'

        for field in self.fields:
            if isinstance(self.fields[field], ModelChoiceField):
                self.fields[field].widget = StaticSelectWidget(choices=self.fields[field].choices)
            else:
                self.fields[field].widget = StaticTextWidget()

        pass

    def make_xf_dateinputs(self):
        for field in self.fields:
            if isinstance(self.fields[field].widget, DateInput):
                self.fields[field].widget = XFDatePickerInput()



    def create_locater(self, target_field, api_call_url, api_call, api_return_field, existing_value, *args, **kwargs):

        self.fields[target_field].widget.attrs['class'] = "mxl"
        self.fields[target_field].widget.attrs['mxl_api_call'] = reverse(api_call_url, kwargs= { 'command': api_call })
        self.fields[target_field].widget.attrs['mxl_param'] = api_return_field

        # Set an existing value if available
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            kwargs['initial'][target_field] = existing_value
            super(XFModelForm, self).__init__(*args, **kwargs)
            self.fields[target_field].disabled = True

    def clean(self):

        cleaned_data = super().clean()

        for field in self.fields:
            if type(self.fields[field].widget) is MissingTextInput:
                self._validate_required_field(cleaned_data, field)

        return cleaned_data


    def _validate_required_field(self, cleaned_data, field_name, message="This field is required"):
        """
        This method is specifically being used to support the "missing" textboxes
        :param cleaned_data:
        :param field_name:
        :param message:
        """
        if field_name in cleaned_data and cleaned_data[field_name] is None:
            blank_checkbox_name = field_name + "_blank"
            if not blank_checkbox_name in self.request.POST:
                self._errors[field_name] = self.error_class([message])
                self.fields[field_name].widget.blank_checked_initially = False
                del cleaned_data[field_name]
            elif blank_checkbox_name in self.request.POST:
                self.fields[field_name].widget.blank_checked_initially = True



    def is_new_entity(self):
        """
        Returns a value that determines if this is a new entity or not, in other words Create or Update/Details
        :return: True if a new entity, false otherwise
        """

        if self.instance.pk is None:
            return True

        return False


    def prepare_form_for_save(self, instance):
        """
        This method can be used to make changes to your model before saving. Use self.instance to make the changes,
        on the instance.
        :return:
        """
        pass


