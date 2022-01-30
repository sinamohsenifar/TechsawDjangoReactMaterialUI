from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from .modelsTag import ArticleTag

from django.utils.text import slugify


@receiver(pre_save, sender=ArticleTag)
def sluggify_title(sender, instance, **kwargs):
    instance.slug = slugify(instance.name, allow_unicode=True)