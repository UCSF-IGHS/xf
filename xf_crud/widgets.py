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


class MandatoryTextInput(widgets.TextInput):

    template_name = "widgets/mandatory_text_input.html"
    blank_should_be_checked = False
    blank_text = "Missing"

    def __init__(self, attrs=None, blank_should_be_checked=False, blank_text="Missing"):

        self.blank_should_be_checked = blank_should_be_checked;
        self.blank_text = blank_text
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context["widget"]["blank_should_be_checked"] = self.blank_should_be_checked
        context["widget"]["blank_text"] = self.blank_text
        return self._render(self.template_name, context, renderer)

