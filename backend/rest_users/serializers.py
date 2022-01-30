from attr import validate
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Exists
from .models import CustomUser
from django.contrib.auth.hashers import (make_password ,
                                         BasePasswordHasher,
                                         Argon2PasswordHasher,
                                         BCryptPasswordHasher,
                                         BCryptSHA256PasswordHasher,
                                         CryptPasswordHasher,
                                         MD5PasswordHasher,
                                         PBKDF2PasswordHasher,
                                         PBKDF2SHA1PasswordHasher,
                                         SHA1PasswordHasher,
                                         UnsaltedMD5PasswordHasher,
                                         UnsaltedSHA1PasswordHasher,
                                         check_password,
                                         )
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.serializers import  TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.settings import api_settings
from blog.serializers import ArticleLikeSerializer , ArticleFavoriteSerializer, CommentSerializer


 
class UpdateProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','image']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs

    class Meta:
        model = CustomUser
        fields = ['password']

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

class ChangeUsernameSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        username = attrs['username']
        # check username
        try:
            get_user = CustomUser.objects.get(username=username)
            raise serializers.ValidationError({'username': 'this username is taken'})        
        except:
            pass
        
        return attrs

    class Meta:
        model = CustomUser
        fields = ['username']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

class ChangeEmailSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        email = attrs['email']
        # check email
        try:
            get_user = CustomUser.objects.get(email=email)
            raise serializers.ValidationError({'email': 'this email is taken'})     
        except:
            pass
        
        return attrs

    class Meta:
        model = CustomUser
        fields = ['email']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class UserModelSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'full_name', 'image', 
                  'last_login', 'is_active', 'is_staff', 'is_superuser']
        
    def get_full_name(self,obj):
        return f'{obj.first_name} {obj.last_name}'


class UserModelSerializerWithToken(UserModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    user_likes = serializers.SerializerMethodField(read_only=True)
    user_favorite_articles = serializers.SerializerMethodField(read_only=True)
    user_comments = serializers.SerializerMethodField(read_only=True)
    
    def get_access(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    def get_refresh(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token)
    
    
    def get_user_likes(self, obj):
        likes = obj.users_likes
        serializer = ArticleLikeSerializer(likes , many=True)
        return serializer.data
    
    def get_user_favorite_articles(self, obj):
        favorites = obj.users_favorites
        serializer = ArticleFavoriteSerializer(favorites , many=True)
        return serializer.data
    
    def get_user_comments(self, obj):
        comments = obj.users_comments
        serializer = CommentSerializer(comments , many=True)
        return serializer.data
    


    def validate(self,data):    
        username = data['username']
        email = data['email']
        password = data['password']
        if data['email']:
            # check email
            try:
                get_user = CustomUser.objects.get(email=email)
                raise ValidationError("Email Has Taken Before")
            except:
                pass
            # check username
            try:
                get_user = CustomUser.objects.get(username=username)
                raise ValidationError("Username Has Taken Before")
            except:
                pass
            # hass password
            data['password'] = make_password(data['password'])

        return data

    class Meta:
        model = CustomUser
        fields = ['id','access', 'refresh','username', 
                  'email','first_name','last_name', 'full_name', 
                  'image','password','user_likes','user_favorite_articles','user_comments' ,'last_login', 'is_active', 
                  'is_staff', 'is_superuser','is_verify',]
        # extra_kwargs = {"password":{"write_only": True}}
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=CustomUser.objects.all(),
        #         fields=['username', 'email'])]
    
    
    def create(self, validated_data):
        user =CustomUser.objects.create(**validated_data)
        return user
    
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user
    
    
    
    
class CustomUserRegistrationClass(serializers.ModelSerializer):
    
    def validate(self,data):
        username = data['username']
        email = data['email']
        try:
            get_email = CustomUser.objects.get(email=email)
            raise ValidationError("Email Has Taken Before")
        except:
            pass
        try:
            get_username = CustomUser.objects.get(username=username)
            raise ValidationError("Username Has Taken Before")
        except:
            pass    
        data['password'] = make_password(data['password'])
        return data
    
    class Meta : 
        model = CustomUser
        fields = ['username', 'email', 'password']    
    
    
    def create(self, validated_data):
        user =CustomUser.objects.create(**validated_data) 
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # refresh = self.get_token(self.user)
        serializer = UserModelSerializerWithToken(self.user).data
        
        for k , v in serializer.items():
            data[k] = v
        
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)
        return data

class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = UntypedToken(attrs['token'])
        jti = token.get(api_settings.JTI_CLAIM)
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise ValidationError("Token is blacklisted")

        return {}
