from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from xf.uc_dashboards.models.perspective import Perspective
from xf.uc_dashboards.models.tag import Tag


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_init, sender=User)
def create_user_profile_on_post_init(sender, instance, **kwargs):
    # If, for some reason, the user doesn't have a profile, create one on the fly
    if not hasattr(instance, 'profile'):
        instance.profile = UserProfile()


class UserProfileManager(models.Manager):
    def get_by_natural_key(self, user):
        return self.get(user=user)


class UserProfile(models.Model):
    '''
    Extends the standard user profile
    '''
    objects = UserProfileManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    tags = models.ManyToManyField(
        Tag,
        related_name='user_profiles',
        blank=True
    )
    preset_filters = models.TextField(
        blank=True,
        help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives'
    )
    default_perspective = models.ForeignKey(
        Perspective,
        null=True,
        blank=True,
        help_text='The default perspective for this user. May be null if the user only has one perspective from their groups. If the perspective is not part of a group, the default perspective will be added.')
    comment = models.TextField(
        blank=True,
        help_text='Any comment.'
    )

    def save(self, *args, **kwargs):
        # See https://stackoverflow.com/questions/6117373/django-userprofile-m2m-field-in-admin-error/6117457#6117457

        print("user profile saved")
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass

        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('user',),)

    def natural_key(self):
        return (self.user,)
