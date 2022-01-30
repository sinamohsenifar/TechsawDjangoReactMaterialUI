from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"   

    def __str__(self):
        return self.name
    
    
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='parent_category')
    
    def __str__(self):
        return self.name
    
    # def __str__(self):                           
    #     full_path = [self.name]            
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.name)
    #         k = k.parent

    #     return ' -> '.join(full_path[::-1])