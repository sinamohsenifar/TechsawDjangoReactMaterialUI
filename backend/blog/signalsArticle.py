from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

from .modelsArticle import Article
from .modelsCategory import Category , SubCategory
from .modelsTag import ArticleTag
import os
import shutil
from django.conf import settings
from django.utils.text import slugify
from django.utils.encoding import iri_to_uri
User = settings.AUTH_USER_MODEL


@receiver(post_delete, sender=Article)
def delete_folderAndFiles(sender, instance, **kwargs):
    ex_product_image_folder = f"{settings.BASE_DIR}\static\media\weblog\{instance.id}"
    if os.path.exists(ex_product_image_folder):
        shutil.rmtree(ex_product_image_folder)
        

@receiver(pre_save, sender=Article)
def sluggify_title(sender, instance, **kwargs):
    
    ex_product_image_folder = f"{settings.BASE_DIR}\static\media\weblog\{instance.id}"
    if os.path.exists(ex_product_image_folder):
        shutil.rmtree(ex_product_image_folder)

    instance.slug = slugify(instance.title, allow_unicode=True)

    
