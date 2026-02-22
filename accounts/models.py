from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Func
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class CustomAccountManager(BaseUserManager):
    # ...
    def create_superuser(self, email, username, first_name, last_name, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)             
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('agree_terms', True)


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, last_name,  password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        # ...

        # Create the user object
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)

        # Assign the user to the "newcomers" group
        try:
            clients = Group.objects.get(name='Clients')
        except Group.DoesNotExist:
            # Handle the case when the "newcomers" group does not exist
            clients = Group.objects.create(name='Clients')

        user.save()
        # Add the user to the "newcomers" group
        user.groups.add(clients)

        return user



class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)   
    is_admin = models.BooleanField(default=False)    
    is_banned = models.BooleanField(default=False)    
    agree_terms = models.BooleanField() 
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_account_permissions'  # Custom related_name
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='user_account_groups'  # Custom related_name
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
