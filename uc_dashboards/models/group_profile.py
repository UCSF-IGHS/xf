from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver

from xf.uc_dashboards.models.perspective import Perspective
from xf.uc_dashboards.models.tag import Tag
from django.db.models.signals import post_save, post_init


class GroupProfileManager(models.Manager):
    def get_by_natural_key(self, group):
        return self.get(group=group)


class GroupProfile(models.Model):
    '''
    A group profile extends the normal Django group with extra fields. A 1:1 relationship exists here, and a
    custom admin has been defined to make this show up in the admin interface.
    '''
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="profile")
    perspectives = models.ManyToManyField(
        Perspective,
        related_name='group_perspectives',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='group_profiles',
        blank=True
    )
    preset_filters = models.TextField(
        blank=True,
        help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives'
    )
    comment = models.TextField(
        blank=True,
        help_text='Any comment.'
    )

    def save(self, *args, **kwargs):
        # See https://stackoverflow.com/questions/6117373/django-userprofile-m2m-field-in-admin-error/6117457#6117457

        print("user profile saved")
        if not self.pk:
            try:
                p = GroupProfile.objects.get(group=self.group)
                self.pk = p.pk
            except GroupProfile.DoesNotExist:
                pass

        super(GroupProfile, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('group',),)

    def natural_key(self):
        return (self.group,)


@receiver(post_save, sender=Group)
def create_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)


@receiver(post_save, sender=Group)
def save_group_profile(sender, instance, **kwargs):
    instance.profile.save()
