from django.urls import path,include

from .views import (
    CustomUserRegisterView,
    BlackListTokenView,
    TokenObtainPairView,
    TokenRefreshView, 
    CustomUserProfileApiView,
    AllUsersProfileApiView,
    TokenVerifyView,
    VerifyUsernameView,
    VerifyEmailView,
    UpdateUserProfileView,
    ChangeUserPasswordView,
    ChangeUsernameView,
    ChangeEmailView,
    DeleteAccountView,
    DeActiveAccount,
    UserVerification,
    )

app_name = 'rest-users'

urlpatterns = [
    
    path('all/', AllUsersProfileApiView.as_view(), name='users-all'),
    path('profile/', CustomUserProfileApiView.as_view(), name ='user-profile'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='user-update'),
    path('profile/changepassword/', ChangeUserPasswordView.as_view(), name='user-changepassword'),
    path('profile/changeusername/', ChangeUsernameView.as_view(), name='user-changeusername'),
    path('profile/changeemail/', ChangeEmailView.as_view(), name='user-changeemail'),
    path('profile/deleteaccount/',DeleteAccountView.as_view(),name='user-delete'),
    path('profile/deactiveaccount/',DeActiveAccount.as_view(),name='user-delete'),
    path('profile/activation/',UserVerification.as_view(),name='user-activation'),
    
    path('token/registration/',CustomUserRegisterView.as_view(), name='user-registeration' ),
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/logout/',BlackListTokenView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('verifyemail/', VerifyEmailView.as_view(), name='email-verify'),
    path('verifyusername/', VerifyUsernameView.as_view(), name='username-verify'),
    
] 