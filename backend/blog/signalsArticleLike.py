from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

from .modelsArticle import ArticleLike, Article
from django.utils.text import slugify

@receiver(pre_save, sender=ArticleLike)
def plus_num_like(sender, instance, **kwargs):
    article = instance.article
    # article = Article.objects.get(id = article_id)
    article.num_likes += 1
    article.save()
@receiver(post_delete, sender=ArticleLike)
def minus_num_like(sender, instance, **kwargs):
    article = instance.article
    article.num_likes -= 1
    article.save()