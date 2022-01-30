from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination


class ArticleLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 24
    default_limit = 12
    
    
class ArticlePageNumberPagination(PageNumberPagination):
    page_size = 1