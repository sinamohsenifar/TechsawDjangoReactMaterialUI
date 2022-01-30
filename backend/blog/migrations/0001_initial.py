# Generated by Django 4.0.1 on 2022-01-26 20:42

import blog.modelsArticle
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('source_name', models.CharField(blank=True, max_length=255, null=True)),
                ('source_link', models.URLField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(upload_to=blog.modelsArticle.ImageUploader)),
                ('video', models.FileField(blank=True, null=True, upload_to=blog.modelsArticle.VideoUploader)),
                ('main_description', models.TextField(null=True)),
                ('num_comments', models.IntegerField(blank=True, default=0, editable=False, null=True)),
                ('num_likes', models.PositiveIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ArticleFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, max_length=250, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, unique=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='blog.category')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=blog.modelsArticle.ExtraImageUploader)),
                ('video', models.FileField(blank=True, null=True, upload_to=blog.modelsArticle.ExtraVideoUploader)),
                ('main_description', models.TextField(blank=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_descriptions', to='blog.article')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Title', max_length=200)),
                ('description', models.TextField(default='write your description')),
                ('rating', models.DecimalField(decimal_places=1, default=7, max_digits=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.article')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
