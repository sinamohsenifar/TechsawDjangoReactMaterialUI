from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.validators import UnicodeUsernameValidator
import os
import shutil
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
 
def profileUploader(instance, path):
    name , ext = os.path.splitext(path)
    ex_profile_image_folder = f'{settings.BASE_DIR}\static\media\profiles\{instance.id}'
    if os.path.exists(ex_profile_image_folder):
        shutil.rmtree(ex_profile_image_folder)
        
    name = 'profile_image'
    filePath = f'profiles\{instance.id}\{name}{ext}'
    return filePath
    
    
username_validator = UnicodeUsernameValidator()

class CustomUserManager(BaseUserManager):
    
    def create_user(self,username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username , email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email , password, **extra_fields)



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(default='defaultProfile.jpg' ,upload_to = profileUploader, blank = False , null=False)
    username = models.CharField( _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        blank=False, null=False,
        error_messages={
            'unique': 'False',
        },
    )
    email = models.EmailField(_('email address'),
                            unique=True,
                            max_length=150, 
                            blank=False, 
                            null=False,
                            error_messages={
                                'unique': 'False',
                            },)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    is_verify = models.BooleanField(_('verify'),default=False,)
    
    # verify_token = models.TextField(default='')
    
    objects = CustomUserManager()
    
    class Meta:
        ordering = ['-date_joined', 'last_login']
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username