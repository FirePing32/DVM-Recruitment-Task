from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

class UserDetail(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=False)
    balance = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1)
        ]
     )

    def __str__(self):
        return self.user.username

class VendorDetail(models.Model):

    vendor = models.OneToOneField(User,on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=True)
    vendordesc = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.vendor.username