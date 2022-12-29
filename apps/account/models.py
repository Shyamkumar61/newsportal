from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from .managers import AccountManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class Account(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, default='profiles/')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_image_url(self):
        return 'https://news-day-2022.s3.amazonaws.com/media/%s' % self.image
