from django.db import models
from django.contrib.auth.models import User


# class UserExtension(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.IntegerField()
#     company = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     website = models.CharField(max_length=255)
#     gender = models.CharField(max_length=50, choices=(("male", "male"), ('female', 'female'), ('other', 'other')))
#
#     class Meta:
#         default_related_name = 'user_extension'
#
#     def __str__(self):
#         return self.user.username
