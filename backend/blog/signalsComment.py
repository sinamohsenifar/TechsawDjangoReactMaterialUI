from asyncio.windows_events import NULL
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from .modelsArticle import Article
from .modelsComment import Comment
import os
import shutil
from django.conf import settings
from django.utils.text import slugify
from django.utils.encoding import iri_to_uri
User = settings.AUTH_USER_MODEL



@receiver(post_delete, sender=Comment)
def minus_num_comment(sender, instance, **kwargs):
    article = instance.article
    article.num_comments -= 1
    article.save()
    
@receiver(pre_save, sender=Comment)
def plus_num_comment(sender, instance, **kwargs):
    article = instance.article
    article.num_comments += 1
    article.save()