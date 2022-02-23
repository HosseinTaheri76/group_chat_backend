from django.urls import path
from chat import views

urlpatterns = [
    path('memberships/', views.UserMembershipsListApiView.as_view(), name='user_groups'),
    path('create/', views.ChatCreateApiView.as_view(), name='create_chat'),
    path('enter/<str:group_code>/', views.EnterChatApiView.as_view(), name='enter_chat'),
    path('join/<str:group_code>/', views.JoinChatApiView.as_view(), name='join_chat'),
    path('leave/<str:group_code>/', views.LeaveChatApiView.as_view(), name='leave_chat'),

]
