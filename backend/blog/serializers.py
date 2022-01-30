#local models
from .modelsArticle import Article, ArticleLike ,ArticleFavorite, ExtraDescription
from .modelsCategory import Category , SubCategory
from .modelsTag import ArticleTag
from .modelsComment import Comment
#  rest framework
from rest_framework import serializers
from django.utils.text import slugify, capfirst

        # slugify('asds asdasd asd sd', allow_unicode=True)


        
# this serializer sends a list of all categories and related sub categories name and slug
class AllCategoryWithChildsSerializer(serializers.ModelSerializer):
    
    childs = serializers.SerializerMethodField()
    
    def get_childs(self, obj):
        # get childs from parent with lazy query
        # this sub_category is related_name of SubCategory Object
        childs = obj.sub_category.all().exclude(category_articles = None)
        serializer = SubCategorySerializer(childs , many=True)
        return serializer.data
    
    
    class Meta : 
        model = Category
        fields = ['id','name', 'slug','childs']
    
    
    #list the categories name and slug
class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['id','name', 'slug','sub_category']
    
    #list the Sub categories name and slug    
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta : 
        model = SubCategory
        fields = ['id','name', 'slug', 'parent']
    
    #list Tage name and slugs
class TagSerializer(serializers.ModelSerializer):
    class Meta : 
        model = ArticleTag
        fields = ['id','name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id','user','article', 'title', 'description', 'rating', 'created_at', 'updated_at' , 'verified']


class ExtraDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDescription
        fields = ['title', 'main_description','article','id', 'image', 'video',]
        
class ArticleSerializer(serializers.ModelSerializer):
    
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    # category = serializers.StringRelatedField(many=False, read_only=True)
    comments = serializers.SerializerMethodField()
    extra_descriptions = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        comments= obj.comments.filter(verified = True)
        serializer = CommentSerializer(comments , many=True)
        return serializer.data

    def get_extra_descriptions(self,obj):
        extra_descriptions = obj.extra_descriptions.all()
        serializer = ExtraDescriptionSerializer(extra_descriptions , many=True)
        return serializer.data       
    
    def get_author(self,obj):
        author = obj.author.username
        return capfirst(author)
    
    def validate(self, data):
        if not len(data['title']) > 15:
            raise serializers.ValidationError({"short_itle" : 'the title must be at least 15 char'})
        # data['slug'] = slugify(data['title'], allow_unicode=True)
        return data
    
    class Meta:
        model = Article
        fields = ['id','author', 'title', 'main_description','extra_descriptions',
                  'num_likes','comments', 'tags','category','slug', 'image' , 
                  'source_name', 'source_link','num_comments', 'created_at', 
                  'updated_at','get_absolute_url']
        
        _readable_fields = ['author','id', 'createdAt', 'updated_at', 'num_comments']



class ArticleDetailSerializer(serializers.ModelSerializer):
    
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    # category = serializers.StringRelatedField(many=False, read_only=True)
    comments = serializers.SerializerMethodField()
    extra_descriptions = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    recomendations  = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        comments= obj.comments.filter(verified = True)
        serializer = CommentSerializer(comments , many=True)
        return serializer.data

    def get_extra_descriptions(self,obj):
        extra_descriptions = obj.extra_descriptions.all()
        serializer = ExtraDescriptionSerializer(extra_descriptions , many=True)
        return serializer.data       
    
    def get_author(self,obj):
        author = obj.author.username
        return capfirst(author)
    
    
    def get_recomendations(self , obj):
        tags_id_list = obj.tags.all().exclude(articles = None).values('id')
        articles = Article.objects.filter(tags__in = tags_id_list).exclude(id = obj.id)
        print(articles)
        serializer = ArticleRecommendationSerializer(articles , many=True)
        return serializer.data
    
    class Meta:
        model = Article
        fields = ['id','author', 'title', 'main_description','extra_descriptions',
                  'num_likes','comments', 'tags', 'category', 'slug', 'image' , 
                  'source_name', 'source_link','num_comments', 'created_at', 
                  'updated_at','get_absolute_url','recomendations', 'views']
        
        _readable_fields = ['author','id', 'createdAt', 'updated_at', 'num_comments']



class ArticleRecommendationSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField()
    
    class Meta:
        model = Article
        fields = ['id', 'slug' , 'title' , 'main_description','num_comments', 'created_at', 
                  'get_absolute_url','category', 'tags','num_likes']


class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = ['article', 'created_at']

class ArticleFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleFavorite
        fields = ['article', 'created_at']