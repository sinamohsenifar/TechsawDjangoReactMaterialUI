import re
from unicodedata import category
from django.urls import reverse
from django.db import models
from django.conf import settings
# Create your models here.
import os
import uuid
import shutil
from .modelsCategory import Category, SubCategory
from .modelsTag import ArticleTag
from django.core.exceptions import ValidationError
import unicodedata
from django.utils.text import slugify

def VideoUploader(instance , path):
    name , ext = os.path.splitext(path)
    # ex_product_video_folder = f'{settings.BASE_DIR}\static\videos\webblog\{instance.id}'
    
    # if os.path.exists(ex_product_video_folder):
    #     shutil.rmtree(ex_product_video_folder)
    vid_name = slugify(instance.title)  
    # name = 'article_video'
    filePath = f'weblog\{instance.id}\{vid_name}{ext}'
    return filePath


def ImageUploader(instance, path):
    name , ext = os.path.splitext(path)
    # ex_product_image_folder = f'{settings.BASE_DIR}\static\images\webblog\{instance.id}'
    
    # if os.path.exists(ex_product_image_folder):
    #     shutil.rmtree(ex_product_image_folder)
    image_name = slugify(instance.title) 
    # name = 'article_image'
    filePath = f'weblog\{instance.id}\{image_name}{ext}'
    return filePath


    
class Article(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    tags = models.ManyToManyField(ArticleTag,related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='articleAuthor')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='category_articles', null=True)
    
    slug = models.SlugField(unique=True, editable=False, allow_unicode=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    
    source_name = models.CharField(max_length=255 , null = True , blank=True)
    source_link = models.URLField(max_length=255 , null=True , blank=True)
    
    image = models.ImageField(upload_to = ImageUploader,null=False, blank=False )
    video = models.FileField(upload_to=VideoUploader, null=True, blank=True )
    
    main_description = models.TextField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    num_comments = models.IntegerField(null=True, blank=True, default=0, editable=False)
    num_likes = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at']
    
    
    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     return reverse("rest-products:get_product", kwargs={"pk": self.pk})
    def get_absolute_url(self):
        sub_cat = self.category
        parent = Category.objects.get(name = sub_cat.parent)
        # return reverse('articles:details', kwargs={"parent": parent.categorySlug, 'category': sub_cat.subCategorySlug, 'slug': self.slug})
        return f"http://127.0.0.1:8000/api/articles/" + f"{parent.slug}/{sub_cat.slug}/{self.slug}/"
    
    def clean(self):
        if not len(self.title) > 15:
            raise ValidationError(
                {'title': "Title should have at least 15 letters"})


def ExtraVideoUploader(instance , path):
    name , ext = os.path.splitext(path)
    # ex_product_video_folder = f'{settings.BASE_DIR}\static\videos\webblog\{instance.article.id}'
    # if os.path.exists(ex_product_video_folder):
    #     shutil.rmtree(ex_product_video_folder)
    vid_name = slugify(instance.title) 

    # name = 'article_video'
    filePath = f'weblog\{instance.article.id}\{vid_name}{ext}'
    return filePath


def ExtraImageUploader(instance, path):
    name , ext = os.path.splitext(path)
    # ex_product_image_folder = f'{settings.BASE_DIR}\static\images\webblog\{instance.article.id}'
    
    # if os.path.exists(ex_product_image_folder):
    #     shutil.rmtree(ex_product_image_folder)
    image_name = slugify(instance.title) 

    # name = 'article_video'
    filePath = f'weblog\{instance.article.id}\{image_name}{ext}'
    return filePath


   
class ExtraDescription(models.Model):
    title =  models.CharField(max_length=255, blank=False, null=True)
    article = models.ForeignKey(Article , on_delete=models.CASCADE , related_name='extra_descriptions')
    image = models.ImageField(upload_to=ExtraImageUploader,null=True, blank=True )
    video = models.FileField(upload_to=ExtraVideoUploader, null=True, blank=True )
    
    main_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class ArticleLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='users_likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articles_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
class ArticleFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='users_favorites')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articles_favorites')
    created_at = models.DateTimeField(auto_now_add=True)


