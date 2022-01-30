from functools import partial
from json import JSONEncoder
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q

from .models import CustomUser
from django.forms import ValidationError

from .serializers import (UserModelSerializer,
                          MyTokenObtainPairSerializer,
                          UserModelSerializerWithToken,
                          UpdateProfileSerializer,
                          ChangePasswordSerializer,
                          ChangeUsernameSerializer,
                          ChangeEmailSerializer,
                          CustomUserRegistrationClass
                          )
#rest_framework

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny,
                                        BasePermission,
                                        IsAuthenticated,
                                        IsAdminUser
                                        )
from rest_framework.response import Response
from rest_framework import status

#Simple_JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import  (TokenRefreshSerializer, 
                                                   TokenVerifySerializer,)
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import (
                                    uri_to_iri,
                                    iri_to_uri,
                                   force_str,
                                   force_bytes,
                                   )
#         _mutable = data._mutable
#         # set to mutable
#         data._mutable = True
#         # сhange the values you want
#         if data['password']:
#             data['password'] = make_password(data['password'])
#         # set mutable flag back
#         data._mutable = _mutable



#activation email function
def send_activation_email(username, id , refresh , email, request):
    current_site= get_current_site(request)
    email_subject = 'Activate Your account'
    
    email_body = render_to_string('emails/ActivationEmailBody.html',{
        'user': username,
        'domain': current_site,
        'id':id,
        'token':refresh})
    
    send_mail(email_subject , email_body , 
              'cena@gmail.com', 
              [email],
              fail_silently=False)


# permission for register view
class UserRegisterPermissio(BasePermission):
    message = "false"
    
    def has_permission(self, request, view):
        
        if request.user.id == None:
               return True
        return False

class NotAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
               return False
        return True

class IsOwnerOrAdminPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        elif request.user.groups == 'Admin':
            return True

class IsActivePermission(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.user.is_active:
               return True
        return False

class IsVerifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.user.is_verify:
               return True
        return False

class NotVerifyPermission(BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_verify:
               return False
        return True







#view for update user first_name m last_name , image 
class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        data = request.data
        # here we get first_name, last_name, password and image
        serializer = UpdateProfileSerializer(user, data= data, partial= True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        data = request.data
        old_password = data['old_password']
        user_password = user.password
        
        check = check_password(old_password,user_password)
        if check:
            serializer = ChangePasswordSerializer(user, data= data, partial= True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response({'error':'wrong password'})

class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        data = request.data
        serializer = ChangeUsernameSerializer(user, data= data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'wrong password'}, status=status.HTTP_400_BAD_REQUEST)

class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        data = request.data
        serializer = ChangeEmailSerializer(user, data= data, partial= True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.is_verify = False
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [IsOwnerOrAdminPermission]
    
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({'user':'DELETED'}, status=status.HTTP_200_OK)
        
class DeActiveAccount(APIView):
    permission_classes = [IsOwnerOrAdminPermission]
    
    def post(self,request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'user':'DeActivated'}, status=status.HTTP_200_OK)





# view for Registering user
class CustomUserRegisterView(APIView):
    permission_classes = [UserRegisterPermissio]
    def post(self, request):
        data = request.data
        # for k , v in data:
        #     data[k] = v    
        
        
        serializer = UserModelSerializerWithToken( data = data , many=False)
        # user_serializer = RegisterUserModelSerializer(data=request.data)
        # if user_serializer.is_valid():
        #     new_user = user_serializer.save()
        #     if new_user:
        #         return Response(status=status.HTTP_201_CREATED)
        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            refresh =serializer.validated_data.get('refresh')
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# check and validate email
class VerifyEmailView(APIView):
    
    def get(self, request):
        email = request.GET.get('email')
        # user = CustomUser.objects.filter(Q(username = username) | Q(email = email)).first()
        user = CustomUser.objects.filter(email = email)
        if user : 
            return Response({'message' : False })
        else:
            return Response({'message' : True })

# check and validate username  
class VerifyUsernameView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        # user = CustomUser.objects.filter(Q(username = username) | Q(email = email)).first()
        user = CustomUser.objects.filter(username = username)
        if user : 
            return Response({'message' : False })
        else:
            return Response({'message' : True })


class UserVerification(APIView):
    def post(self,request):
        
        try:
            if request.user.is_authenticated:
                user = request.user
            else:
                user = CustomUser.objects.get(id=request.POST.get('id'))
        except Exception as e:
            user = None
            
        serializer = TokenVerifySerializer(data = {'token' : request.POST.get('token')})
        verified = False
        try:
            serializer.is_valid(raise_exception=True)
            verified = True
            
        except TokenError as e:
            verified = False
            raise InvalidToken(e.args[0])


        if user and verified:
            user.is_active = True
            user.is_verify = True
            user.save()
            return Response({'user email verified'} , status=status.HTTP_202_ACCEPTED)
        return Response({'user email not verified'} , status=status.HTTP_400_BAD_REQUEST)
    
# view for User Profile Informations            
class CustomUserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = UserModelSerializerWithToken(user, many=False)
        return Response(serializer.data)        

# view for showing all users
class AllUsersProfileApiView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        users = CustomUser.objects.all()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data)    

# blacklist a refresh token but access can work
class BlackListTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'logout': 'Okay'},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'bad'},status=status.HTTP_400_BAD_REQUEST)


# Login        
class TokenObtainPairView(generics.GenericAPIView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """ 
    permission_classes = [NotAuthenticatedPermission]
    authentication_classes = ()

    serializer_class = MyTokenObtainPairSerializer

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        # gets serializer_class from abov and send it data
        serializer = self.get_serializer(data=request.data)     
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        # here we sent a validation link to user email
        if serializer.validated_data.get('is_verify'): 
            print(serializer.validated_data.get('is_verify'))  
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            send_activation_email(serializer.validated_data.get('username'),
                                  serializer.validated_data.get('id') , 
                                  serializer.validated_data.get('refresh') ,
                                  serializer.validated_data.get('email'), 
                                  request
                                  )
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        

# get access by refresh 
class TokenRefreshView(TokenViewBase):
    
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer   

# check oken refresh or access with the name of token
class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = TokenVerifySerializer       
 
 


 
 
        
      















