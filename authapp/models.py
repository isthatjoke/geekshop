from datetime import timedelta
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='age', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'F')
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='about me', max_length=512, blank=True)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_CHOICES, blank=True)
    localization = models.CharField(verbose_name='localization', max_length=30, blank=True)
    social_page = models.TextField(verbose_name='social page', max_length=512, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()


