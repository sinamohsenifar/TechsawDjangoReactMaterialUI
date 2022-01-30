from django.db import models


class ArticleTag(models.Model):
    name= models.CharField(max_length=35)
    slug= models.SlugField(unique=True,max_length=250, editable=False, allow_unicode=True)
    created_at= models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.slug