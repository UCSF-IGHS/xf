import ast

from xf.xf_system.views import XFNavigationViewMixin


class XFTranslationHelper:


    def translations(self, field_name):
        """
        Gets a dictionary with translations based on a field name. The method searches for the
        field_name and also field_name_strings and merges these into a dictonary. The field_name
        will be merged into the dictionary using the default language code.
        So:
        title = 'hello'
        title_strings = 'pt':'ola', 'nl':'hallo',
        The dictionary will be:
        [pt] = 'ola'
        [nl] = 'hallo'
        [en] = 'hello'

        The en code comes from the site default language setting.

        :param field_name:
        The field name for which to get the translations
        :return:
        A dictionary with all the translations
        """

        if XFNavigationViewMixin.site_settings is not None:

            if hasattr(self, "%s_%s" % (field_name, "strings")):
                translation_strings = getattr(self, "%s_%s" % (field_name, "strings"))
                trls = ast.literal_eval("{%s}" % translation_strings)
            else:
                trls = []

            if hasattr(self, field_name):
                trls[XFNavigationViewMixin.site_settings.site_default_language] = getattr(self, field_name)

        else:
            return []

        return trls


    def translate(self, field_name, language_code=None):
        """
        Gets the translation for a specific field_name, with an optional language code
        :param field_name:
        :param language_code:
        :return:
        """

        trls = self.translations(field_name)

        if language_code is None:
            language_code = "en"

        if language_code in trls:
            return trls[language_code]
        else:
            return "[[%s]] missing" % language_code

