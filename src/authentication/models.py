from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, gender, date_of_birth):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            date_registered=timezone.now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, gender, date_of_birth):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'gender']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
