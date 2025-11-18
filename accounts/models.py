from django.db import models
from django.contrib.auth.models import User


def user_profile_image_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    picture = models.ImageField(
        upload_to=user_profile_image_path,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Profile for {self.user.username}"
