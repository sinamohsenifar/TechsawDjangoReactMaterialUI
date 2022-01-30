from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

from .models import CustomUser
import os
import shutil
from django.conf import settings
from django.utils.text import slugify
User = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Article.objects.create(user=instance)
  
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#         instance.profile.save()

@receiver(post_delete, sender=CustomUser)
def delete_folderAndFiles(sender, instance, **kwargs):
    ex_product_image_folder = f"{settings.BASE_DIR}\static\media\profiles\{instance.id}"
    if os.path.exists(ex_product_image_folder):
        shutil.rmtree(ex_product_image_folder)
        