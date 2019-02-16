from django.db import models


class TagManager(models.Manager):
    def get_by_natural_key(self, text):
        return self.get(text=text)


class Tag(models.Model):
    objects = TagManager()
    text = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        unique_together = (('text',),)

    def natural_key(self):
        return (self.text,)

    def __str__(self):
        return self.text
