from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserProfileManager(BaseUserManager):
    """ helps django work with our custom mocels """

    def create_user(self, email, name, password=None):
        """ create new user profile objects """

        if not email:
             # jika tidak menyediakan email
             raise ValueError("User must Provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ create and save a new superuser """

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """respents a 'user profile' inside our system """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' # standar username django adalah username, disini kita rubah ke email
    REQUIRED_FIELD = ['name']

    # create helper function
    def get_full_name(self):
        """ use to get a users full name """

        return self.name

    def get_short_name(self):
        """ use to get a users short name """

        return self.name

    def __str__(self):
        """ Django uses this to convert the object to string """

        return self.email
