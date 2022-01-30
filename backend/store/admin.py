from django.contrib import admin
from .modelsBook import Book
from .modelsOrder import Order
from .modelsTags import BookTag
from .mdoelsCategory import Category, SubCategory
# Register your models here.


@admin.register(Book)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','id', 'category', 'slug', 'rating', 'countInStock')
    

@admin.register(Order)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'isPaid','createdAt', 'deliveredAt', 'totalPrice')


@admin.register(BookTag)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','created_at')

@admin.register(Category)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
@admin.register(SubCategory)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')