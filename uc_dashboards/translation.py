from modeltranslation.translator import register, translator, TranslationOptions

from xf.uc_dashboards.models import Widget, Page, NavigationSection, PageSection, PageStatus
from xf.uc_dashboards.models.perspective import Perspective


@register(Widget)
class WidgetTranslationOptions(TranslationOptions):
    fields = ('title', 'user_description', 'sub_text', 'text',)

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'main_title', 'text', 'data_sources', 'about')

@register(NavigationSection)
class NavigationSectionTranslationOptions(TranslationOptions):
    fields = ('caption',)


@register(PageSection)
class PageSectionTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(PageStatus)
class PageStatusTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Perspective)
class PerspectiveTranslationOptions(TranslationOptions):
    fields = ('name',)
