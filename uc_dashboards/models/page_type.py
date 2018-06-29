from django.db import models


class PageType(models.Model):
    name = models.CharField(max_length=150)
    url_section = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name