from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string


class GenderChoice(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class Region(models.Model):
    name = models.CharField(_("name"), max_length=512)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ("name",)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    email = models.EmailField(_("email address"), null=True, unique=True)
    full_name = models.CharField(_("full name"), max_length=512, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=512, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=512, blank=True, null=True)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name=_("region"), on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=6, choices=GenderChoice.choices, blank=True, null=True)
    REQUIRED_FIELDS = []
    
    def get_full_name(self) -> str:
        return str(self.full_name)



class EmailOtp(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(_("email address"))
    otp = models.CharField(_("OTP"), max_length=6)
    verified = models.BooleanField(_("is verified"), default=False)
    attempts = models.PositiveSmallIntegerField(_("attempts"), default=0)
    expires_at = models.DateTimeField(_("expires at"))
    used_at = models.DateTimeField(_("used at"), null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        if not self.otp:
            self.otp = get_random_string(length=6, allowed_chars="1234567890")
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("Email OTP")
        verbose_name_plural = _("Email OTPs")
        ordering = ("-created_at",)

    def is_verified(self):
        return self.verified and not self.used_at and self.expires_at > timezone.now()
    
    def make_used(self):
        self.used_at = timezone.now()
        self.save()

    @classmethod
    def get_verify_pendings(cls):
        return cls.objects.filter(
            verified=False, used_at=None, expires_at__gt=timezone.now(),
            attempts__lt=5
        )

    def send(self):
       send_mail(
            "Email Verification for Your Styly Account",
            render_to_string("email_code.html", {"code": self.otp}),
            None,
            recipient_list=[self.email],
        )
