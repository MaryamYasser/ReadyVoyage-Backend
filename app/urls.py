from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from knox import views as knox_views


urlpatterns = [
	
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    

] 
