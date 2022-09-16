from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# from store.models import Account


class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name, email, password=None, profile_pic=None):
        if not email:
            raise ValueError('user must have an email to register')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name

        user.save(using=self._db)

        # Account.objects.create(user=user, profile_pic=profile_pic)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmailAccount(AbstractUser, models.Model):
    username = models.NOT_PROVIDED
    email = models.EmailField('Email Address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    def __str__(self):
        return self.email

