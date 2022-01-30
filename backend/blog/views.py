from cgitb import lookup
from django.db.models import Q
# restFramework Classes
from django.http import JsonResponse
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView,ListCreateAPIView,
                                     UpdateAPIView
                                     )
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, 
                                   HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED,
                                   HTTP_204_NO_CONTENT,)
from rest_framework.filters import SearchFilter
#rest framework permissions
from rest_framework.permissions import (IsAdminUser,AllowAny, IsAuthenticated, 
                                        IsAuthenticatedOrReadOnly,
                                        BasePermission, SAFE_METHODS,
                                        )

from rest_users.models import CustomUser

#local models
from .modelsArticle import Article, ArticleLike, ArticleFavorite
from .modelsCategory import Category , SubCategory
from .modelsTag import ArticleTag
from .modelsComment import Comment

#LOCAL serializers
from .serializers import (ArticleSerializer, CategorySerializer, SubCategorySerializer,ArticleDetailSerializer,
                          TagSerializer,AllCategoryWithChildsSerializer , CommentSerializer)

from .forms import ArticleForm

from .pagination import ArticleLimitOffsetPagination,ArticlePageNumberPagination




#make a permission for readonly or owner
class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        else:
            return obj.author == request.user

#here we list category tree view     DONE
class ListCategoryTreeView(APIView):
    # here we response all category tree objects
    def post(self, request , format=False):
        parent = Category.objects.all()
        serializer = AllCategoryWithChildsSerializer(parent , many=True)
        # sub_parents = Category.objects.all().prefetch_related('sub_category')
        # sub_parents = SubCategory.objects.all().select_related('parent')
        # print(sub_parents)
        return Response(serializer.data)   

# list articles with parent category   DONE
class CategoryListView(APIView):
    permission_classes = [IsAdminUser]
    def get_category(self, category):
        try:
            return Category.objects.get(slug=category)
        except Category.DoesNotExist:
            return Http404

    # here we list all of articles in category from parent
    def get(self, request,category= None, format=None):
        if category:
            category = self.get_category(category)
            serializer = CategorySerializer(category , many=False)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories , many=True)
        
        return Response(serializer.data)
    
    def post(self, request , format=None):
        data = request.data
        # data._mutable = True
        # data['user'] = request.user.id
        # data._mutable = False
        if data['name'] is not None:
            serializer = CategorySerializer(data=data , many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=HTTP_201_CREATED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)

    def put(self, request , category, format=None):
        category = self.get_category(category)
            # here we send data to serializer to validate them
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request , category, format=None):
        category = self.get_category(category)
        category.delete()
        return Response({'message': 'Okay'}, status=HTTP_204_NO_CONTENT)

# list articles with sub category    DONE
class SubCategoryListView(APIView):
    permission_classes = [IsAdminUser]
    def get_sub_category(self, subcategory):
        try:
            return SubCategory.objects.get(slug=subcategory)
        except SubCategory.DoesNotExist:
            return Http404

    # here we list all of articles in category from parent
    def get(self, request,subcategory= None, format=None):
        if subcategory:
            subcategory = self.get_sub_category(subcategory)
            serializer = SubCategorySerializer(subcategory , many=False)
        else:
            subcategory = SubCategory.objects.all()
            serializer = SubCategorySerializer(subcategory , many=True)
        
        return Response(serializer.data)
    
    def post(self, request , format=None):
        data = request.data
        # data._mutable = True
        # data['user'] = request.user.id
        # data._mutable = False
        if data['name'] is not None and data['parent'] is not None:
            serializer = SubCategorySerializer(data=data , many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=HTTP_201_CREATED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)

    def put(self, request , subcategory, format=None):
        subcategory = self.get_sub_category(subcategory)
            # here we send data to serializer to validate them
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request , subcategory, format=None):
        subcategory = self.get_sub_category(subcategory)
        subcategory.delete()
        return Response({'message': 'Okay'}, status=HTTP_204_NO_CONTENT)


# GENERIC View For Listing Searching and pagination
#http://127.0.0.1:8000/api/articles/all/?q=django&offset=1    search pagination
# http://127.0.0.1:8000/api/articles/all/?limit=1&offset=1    for pagination
class AllArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    # filter_banckends = [SearchFilter]
    # search_fields = ['title', 'main_description', 'extra_descriptions.title', 'extra_descriptions.main_description', 'tags','source_name']
    serializer_class = ArticleSerializer
    pagination_class = ArticlePageNumberPagination
    
    def get_queryset(self , *args , **kwargs):
        queryset_list = Article.objects.all()
        # query = self.request.GET.get('q')
        query =  self.kwargs.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(main_description__icontains=query)|
                Q(extra_descriptions__title__icontains=query)|
                Q(extra_descriptions__main_description__icontains=query)|
                Q(tags__name__icontains=query)|
                Q(source_name=query)
            ).distinct()
        return queryset_list
   
 
class CategoryArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    # filter_banckends = [SearchFilter]
    # search_fields = ['title', 'main_description', 'extra_descriptions.title', 'extra_descriptions.main_description', 'tags','source_name']
    serializer_class = ArticleSerializer
    pagination_class = ArticlePageNumberPagination
    # lookup_field = 'slug'
    
    def get_queryset(self , *args , **kwargs):
        queryset_list = Article.objects.all()
        # query = self.request.GET.get('q')
        parent_slug =  self.kwargs.get('category')
        try:
            parent = Category.objects.get(slug = parent_slug)
        except Category.DoesNotExist:
            return queryset_list
        
        childs = parent.sub_category.all().exclude(category_articles = None)
        
        if childs:
            queryset_list = queryset_list.filter(category_id__in = childs)
        return queryset_list


class SubCategoryArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    # filter_banckends = [SearchFilter]
    # search_fields = ['title', 'main_description', 'extra_descriptions.title', 'extra_descriptions.main_description', 'tags','source_name']
    serializer_class = ArticleSerializer
    pagination_class = ArticlePageNumberPagination
    
    def get_queryset(self , *args , **kwargs):
        queryset_list = Article.objects.all()
        # query = self.request.GET.get('q')
        sub_category_slug =  self.kwargs.get('subcategory')
        try:
            sub_category = SubCategory.objects.get(slug = sub_category_slug)
        except Category.DoesNotExist:
            return queryset_list
        queryset_list = queryset_list.filter(category_id = sub_category.id)
        return queryset_list
    

class ArticleCreateView(APIView):
    permission_classes = [IsAdminUser]
    # this function just retrieve articles
    
    #this function creates article
    def post(self, request, format=None):
    
        # here we send data to serializer to validate them
        # file_uploaded = request.FILES['image']
        data = request.data
        data._mutable = True
        data['user'] = request.user.id
        data._mutable = False
      
        serializer = ArticleSerializer(data = data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=HTTP_201_CREATED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)


class ArticleDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleDetailSerializer
    # queryset = Article.objects.all()
    # lookup_field = 'slug'
    multiple_lookup_fields = ['slug']
    
    def get_queryset(self):
        query = Article.objects.all()
        return query
    
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        obj.views += 1
        obj.save()
        self.check_object_permissions(self.request, obj)
        return obj

class ArticleUpdateView(APIView):
    # find Article by slug
    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Http404
    # update the article
    def put(self , request,category,subcategory, slug, format=None):
        article = self.get_object(slug)
        
        # here we send data to serializer to validate them
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)


class ArticleDeleteView(DestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        # user = request.user
        article = Article.objects.get(id = request.data['article_id'])
        object , created  = ArticleLike.objects.get_or_create(user=request.user,article=article)
        if not created:
            object.delete()
            return Response({'article_like': 'deleted'} , status=HTTP_200_OK)
        return Response({'article_like': 'Added'} , status=HTTP_200_OK)
            

class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        # user = request.user
        article = Article.objects.get(id = request.data['article_id'])
        object , created  = ArticleFavorite.objects.get_or_create(user=request.user,article=article)
        if not created:
            
            object.delete()
            return Response({'article_favorite': 'deleted'} , status=HTTP_200_OK)
        
        return Response({'article_favorite': 'Added'} , status=HTTP_200_OK)


# create edit and delete comments
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Http404
    
    def post(self, request, format=None):
        # here we send data to serializer to validate them
        data = request.data
        data._mutable = True
        data['user'] = request.user.id
        data._mutable = False
        
        serializer = CommentSerializer(data = request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=HTTP_201_CREATED)
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)
    
    # update the comment
    def put(self , request, format=None):
        comment_id = request.data['id']
        comment = self.get_object(comment_id)
        # getting owner id
        comment_owner_id = comment.user_id
        if comment_owner_id == request.user.id :
            
            # here we send data to serializer to validate them
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=HTTP_202_ACCEPTED)
            return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Owner Error'} , status=HTTP_400_BAD_REQUEST)
    
    # show the article detail
    def delete(self, request, format=None):
        comment_id = request.data['id']
        comment = self.get_object(comment_id)
        # getting owner id
        comment_owner_id = comment.user_id
        if comment_owner_id == request.user.id :
            comment.delete()
            return Response({'message': 'Okay'}, status=HTTP_204_NO_CONTENT)
        return Response({'error': 'Owner Error'} , status=HTTP_400_BAD_REQUEST)

