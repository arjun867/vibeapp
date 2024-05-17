from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('suggest_user/', views.suggest_user, name='suggest_user'),
    path('recent_chats/', views.recent_chats, name='recent_chats'),
]
