from django.contrib import admin
from .models import CustomUser
# Register your models here.




@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined')
    list_filter = ('date_joined', 'last_login')