from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Model
from django.forms.models import ModelForm
#import floppyforms as forms
#from floppyforms.widgets import PasswordInput

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

class XFModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(XFModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3 col-sm-3 col-xs-3'
        self.helper.field_class = 'col-lg-9 col-sm-9 col-xs-9'
        self.helper.form_action = ''  # redirect in the view
        self.helper.form_tag = False
        self.helper.help_text_inline = True  # means that I want <span> elements


    def create_locater(self, target_field, api_call_url, api_call, api_return_field, existing_value, *args, **kwargs):

        self.fields[target_field].widget.attrs['class'] = "mxl"
        self.fields[target_field].widget.attrs['mxl_api_call'] = reverse(api_call_url, kwargs= { 'command': api_call })
        self.fields[target_field].widget.attrs['mxl_param'] = api_return_field

        # Set an existing value if available
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            kwargs['initial'][target_field] = existing_value
            super(XFModelForm, self).__init__(*args, **kwargs)
            self.fields[target_field].widget.attrs['readonly'] = True


