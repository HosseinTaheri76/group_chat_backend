from django.urls import path
from authentication import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.UserCreateApiView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('user/', views.UserInfoApiView.as_view(), name='user_info')
]