from django.db import models


class PageStatus(models.Model):
    code = models.CharField(
        max_length=50,
        help_text='Code of the status.')
    name = models.CharField(
        max_length=150,
        help_text='Name of the status.')

    def __str__(self):
        return self.name