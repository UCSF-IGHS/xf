from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class TypeAheadWidget(widgets.TextInput):

    template_name = 'widgets/autocomplete.html'

    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs)


class StaticTextWidget(widgets.TextInput):

    template_name = 'widgets/static_text.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)


class StaticSelectWidget(widgets.Select):
    template_name = 'widgets/static_select.html'
    option_template_name = 'widgets/static_select_option.html'

    pass


class MissingTextInput(widgets.TextInput):

    template_name = "widgets/missing_text_input.html"
    blank_checked_initially = False
    blank_text = "Missing"

    def __init__(self, attrs=None, is_new_entity=False, blank_text="Missing", is_date_picker=False):

        self.blank_checked_initially = not is_new_entity
        self.blank_text = blank_text
        self.is_date_picker = is_date_picker
        if is_date_picker:
            attrs = {'class': 'date-field datepicker'}
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context["widget"]["blank_checked_initially"] = self.blank_checked_initially
        context["widget"]["blank_text"] = self.blank_text
        context["widget"]["is_date_picker"] = self.is_date_picker
        return self._render(self.template_name, context, renderer)


class XFDatePickerInput(widgets.DateInput):
    template_name = "widgets/date_input.html"

    def __init__(self, attrs=None, format='%Y-%m-%d'):
        attrs = {'class': 'date-field datepicker'}
        super().__init__(attrs, format)
