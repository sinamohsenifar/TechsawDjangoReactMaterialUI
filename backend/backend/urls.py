from unicodedata import name
from django.contrib import admin
from django.urls.conf import include, path
from django.conf import settings
from django.conf.urls.static import static
    # for Simple_JWT 



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/users/', include('rest_users.urls', namespace='rest-users'))
    # for users Model and token
    path('api/users/', include('rest_users.urls', namespace = 'rest-users')),
    path('api/articles/', include('blog.urls', namespace='articles')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)