from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.
from .modelsBook import Book

class Review(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.user)
    def rev_title(self):
        return self.title
    def rev_comment(self):
        return self.comment
    def rev_rateing(self):
        return self.rating