
from django.db import models
from django.conf import settings
# Create your models here.
import os
import uuid
import shutil
from .modelsTags import BookTag
from .mdoelsCategory import SubCategory

def ImageUploader(instance, path):
    name , ext = os.path.splitext(path)
    ex_product_image_folder = f'{settings.BASE_DIR}\static\images\books\{instance.id}'
    
    if os.path.exists(ex_product_image_folder):
        shutil.rmtree(ex_product_image_folder)
        
    name = 'product_image'
    filePath = f'books\{instance.id}\{name}{ext}'
    return filePath

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    tags = models.ManyToManyField(BookTag,related_name='books')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='bookAuthor')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    
    image = models.ImageField(upload_to = ImageUploader,null=False, blank=False )
    title = models.CharField(max_length=200, null=True, blank=True)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     return reverse("rest-products:get_product", kwargs={"pk": self.pk})
    def get_absolute_url(self):
        return f"http://127.0.0.1:8000/api/products/{self.slug}/"
    
    # def get_absolute_url(self):
    #     return "http://127.0.0.1:8000/api/products/%i/" % self.pk

    
    #  <a href="https://www.w3schools.com">Visit W3Schools.com!</a> 


