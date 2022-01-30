from unicodedata import name
from django.urls import path
from .views import (ArticleDetailView, AllArticleListView,CategoryArticleListView,
                    SubCategoryArticleListView, ArticleCreateView,
                    ArticleUpdateView,ArticleDeleteView,
                    CategoryListView, SubCategoryListView, 
                    ListCategoryTreeView, CommentView, LikeView, FavoriteView)

app_name= 'articles'

urlpatterns = [
    # get all articles and create one article
    path('', AllArticleListView.as_view(), name= 'articles-all'),    # List and search all articles
    
    path('create/',ArticleCreateView.as_view() , name='create' ), # create an article
    
    path('like/', LikeView.as_view(), name='article-like'), # like and unlike an article
    
    path('favorite/', FavoriteView.as_view(), name='article-favorite'), # make article user favorite
    
    path('categories/', ListCategoryTreeView.as_view(), name='category-list' ), # list all categories and sub categories
   
    path('comments/', CommentView.as_view(), name='article-comments'), # create update and delete a comment
    
    path('category/', CategoryListView.as_view(), name='category-list'), # list all categories for Admin
    
    path('category/<slug:category>/', CategoryListView.as_view(), name='category-edit'), # update create and delete a category for admin
     
    path('subcategory/', SubCategoryListView.as_view(), name='sub-category-list'),   # list all SUB categories for Admin
     
    path('subcategory/<slug:subcategory>/', SubCategoryListView.as_view(), name='sub-category-edit'), # update create and delete a sub category for admin
    
    path('<slug:category>/', CategoryArticleListView.as_view(), name= 'articles-category-all'),    # List and search all articles
    path('<slug:category>/<slug:subcategory>/', SubCategoryArticleListView.as_view(), name= 'articles-sub-category-all'),    # List and search all articles
    
    # get atricle category and UPDATE and DELETE
    path('<slug:category>/<slug:subcategory>/<str:slug>/', ArticleDetailView.as_view(), name= 'details'),
    path('<slug:category>/<slug:subcategory>/<str:slug>/edit/', ArticleUpdateView.as_view(), name= 'details'),
    path('<slug:category>/<slug:subcategory>/<str:slug>/delete/', ArticleDeleteView.as_view(), name= 'details'),
    
]
