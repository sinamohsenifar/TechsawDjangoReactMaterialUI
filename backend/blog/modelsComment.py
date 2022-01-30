from unicodedata import category
from django.urls import reverse
from django.db import models
from django.conf import settings
# Create your models here.
import os
import uuid
import shutil
from .modelsArticle import Article
from django.core.exceptions import ValidationError
import unicodedata


class Comment(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=False, related_name='users_comments', editable=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', null=True,blank=False)
    
    title = models.CharField(default='Title',max_length=200, null=False, blank=False)
    description = models.TextField(default = 'write your description',null=False, blank=False)
    rating = models.DecimalField(default=7,
        max_digits=2, decimal_places=1, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    verified = models.BooleanField(default = False)
    
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

    
    def is_verified(self):
        return self.verified
    
    def clean(self):
        if not len(self.title) > 3:
            raise ValidationError(
                {'title': "Title should have at least 3 letters"})
    
    # def get_absolute_url(self):
    #     return "http://127.0.0.1:8000/api/products/%i/" % self.pk

    
    #  <a href="https://www.w3schools.com">Visit W3Schools.com!</a> 


