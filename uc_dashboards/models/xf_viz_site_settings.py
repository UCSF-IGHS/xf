from django.db import models

from xf.uc_dashboards.models.perspective import Perspective
from xf.xf_system.models import XFSiteSettings


class XFVizSiteSettings(models.Model):
    '''
    Extends XF Settings
    '''
    settings = models.OneToOneField(XFSiteSettings, on_delete=models.CASCADE, related_name="settings")
    anonymous_perspective = models.ForeignKey(Perspective, on_delete=models.PROTECT, related_name="anonymous_perspective")

    def save(self, *args, **kwargs):
    #See https://stackoverflow.com/questions/6117373/django-userprofile-m2m-field-in-admin-error/6117457#6117457

        print("viz settings saved")
        if not self.pk:
            try:
                p = XFVizSiteSettings.objects.get(settings=self.settings)
                self.pk = p.pk
            except XFVizSiteSettings.DoesNotExist:
                pass

        super(XFVizSiteSettings, self).save(*args, **kwargs)