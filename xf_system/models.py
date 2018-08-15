from django.db import models

from xf.xf_system.mixins import XFTranslationHelper


class XFSiteSettings(models.Model, XFTranslationHelper):
    settings_key = models.CharField(max_length=50, null=False, blank=False)
    site_title = models.CharField(max_length=50, null=True, blank=True)

    site_title_strings = models.TextField(
        blank=True,
        help_text="Translations. Use a format as follows: 'pt':'tradução', 'nl':'vertaling', -- each on a new line"
    )

    site_icon = models.CharField(max_length=50,
                                 null=True,
                                 blank=True,
                                 help_text="The site icon to be used",
                                 default="fa-globe")

    site_default_language = models.CharField(max_length=5,
                                             null=False,
                                             blank=False,
                                             help_text="The default language code for the site.",
                                             default="en")

    custom_theme = models.CharField(max_length=50,
                                    null=True,
                                    blank=True,
                                    help_text="Custom theme defined for the site.")

    footer_details = models.TextField(null=True,
                                      blank=True,
                                      help_text="Details that will be added to the site footer")

    def __str__(self):
        return self.settings_key
