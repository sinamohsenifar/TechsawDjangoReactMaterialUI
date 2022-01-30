from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

from .modelsCategory import Category , SubCategory

from django.utils.text import slugify

@receiver(pre_save, sender=Category)
def sluggify_title(sender, instance, **kwargs):
    instance.slug = slugify(instance.name, allow_unicode=True)

@receiver(pre_save, sender=SubCategory)
def sluggify_title(sender, instance, **kwargs):
    instance.slug = slugify(instance.name, allow_unicode=True)