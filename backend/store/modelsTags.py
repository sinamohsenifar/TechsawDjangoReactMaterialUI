from django.db import models

class BookTag(models.Model):
    name        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
