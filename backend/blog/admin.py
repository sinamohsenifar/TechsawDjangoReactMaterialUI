from django.contrib import admin
from .modelsArticle import Article,ExtraDescription , ArticleLike, ArticleFavorite
from .modelsTag import ArticleTag
from .modelsCategory import Category, SubCategory
from .modelsComment import Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('article', 'title', 'description', 'rating', 'created_at', 'updated_at', 'verified')
    readonly_fields = ('created_at', 'updated_at','article', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title','user','id', 'created_at', 'rating', 'verified')
    # inlines = [CommentInline]
    _readonly_fields = ('slug', 'verified')
    
class ExtraDescriptionInline(admin.StackedInline):
    model= ExtraDescription
    readonly_fields = ('id',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'author', 'source_name', 'id', 'category','num_likes','num_comments', 'created_at')
    list_filter = ('author','category', 'created_at')
    # prepopulated_fields = {"slug": ("title",)}
    inlines = [ExtraDescriptionInline,CommentInline]

@admin.register(ArticleTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug','created_at')

class SubCategoryInline(admin.TabularInline):
    model= SubCategory
    fields = ( 'name' , 'slug')
    readonly_fields = ('slug',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'slug',)
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'slug', 'parent')
    list_filter = ( 'parent',)
    
    
    
@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ('user','article', 'id', 'created_at')
    list_filter = ( 'created_at',)
    
@admin.register(ArticleFavorite)
class ArticleFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user','article', 'id', 'created_at')
    list_filter = ( 'created_at',)