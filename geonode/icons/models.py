import datetime
import hashlib
import os

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from taggit.managers import TaggableManager

IMGTYPES = ['svg', 'png']

class IconProfile(models.Model):
    LICENSE_CHOICES = [
        ("PD", _("Public Domain")),
        ("CC_2.0", _("Creative Commons 2.0")),
        ("MIT", _("MIT")),
    ]

    license_help_text = _('Public: Any registered user can view and join a public group.<br>'
                         'Public (invite-only):Any registered user can view the group.  '
                         'Only invited users can join.<br>'
                         'Private: Registered users cannot see any details about the group, including membership.  '
                         'Only invited users can join.')

    icon = models.AutoField(primary_key=True)
    #owner = models.OneToOneField(get_user_model)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    file = models.FileField(upload_to="icon", blank=True)
    description = models.TextField()
    icon_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('The URL of the icon if it is external.'),
        verbose_name=_('URL'))
    keywords = TaggableManager(
        _('keywords'),
        help_text=_("A space or comma-separated list of keywords"),
        blank=True)
    license = models.CharField(
        max_length=15,
        default="PD",
        choices=LICENSE_CHOICES,
        help_text=license_help_text)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        IconProfile.save()

#    def save(self, *args, **kwargs):
#        icon, created = Group.objects.get_or_create(name=self.slug)
#        self.icon = icon
#        super(GroupProfile, self).save(*args, **kwargs)

#    def delete(self, *args, **kwargs):
#        icon.objects.filter(name=self.slug).delete()
#        super(IconProfile, self).delete(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return reverse('icon_detail', kwargs={'slug': self.slug})

    @property
    def class_name(self):
        return self.__class__.__name__

    def get_owner(self):
        """
        Returns a queryset of the icon's owner.
        """
        return get_user_model().objects.filter(
            id__in=self.owner_queryset().filter(
                role='owner').values_list(
                "user",
                flat=True))

    @classmethod
    def groups_for_user(cls, user):
        """
        Returns the groups that user is a member of.  If the user is a superuser, all groups are returned.
        """
        if user.is_authenticated():
            if user.is_superuser:
                return cls.objects.all()
            return cls.objects.filter(groupmember__user=user)
        return []

    def __unicode__(self):
        return self.title

    def icon_pre_delete(instance, sender, **kwargs):
        """Make sure that the public icon is not deleted"""
        if instance.name == 'anonymous':
            raise Exception('Deletion of icons is\
             not permitted by anonymous users')
