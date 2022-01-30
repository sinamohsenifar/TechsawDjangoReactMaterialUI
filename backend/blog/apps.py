from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        import blog.signalsArticle ,blog.signalsArticleLike, blog.signalsCategory , blog.signalsComment , blog.signalsTag
