from pydoc import describe
from django import forms
from .modelsArticle import Article




class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image' , 'main_description', 'tags', 'category',]