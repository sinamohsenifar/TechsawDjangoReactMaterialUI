from __future__ import unicode_literals
from django.db import models
# from .serializers import SubCategorySerializer
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False, allow_unicode=True)
    # parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True )
    
    class Meta:
        verbose_name_plural = "categories"   

    def __str__(self):
        return self.name
    

    # def categories(self):
    #     subs = SubCategory.objects.filter(parent__categorySlug = self.categorySlug)
    #     # serializer = SubCategorySerializer(sub , many=True)
    #     return subs
          
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False, allow_unicode=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='sub_category')
    
    def __str__(self):
        return self.name
    
    def has_article(self):
        if self.category_articles is not [] :
            return True
        else : 
            return False
    