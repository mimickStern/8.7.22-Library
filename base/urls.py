from django.contrib import admin
from django.urls import path,include
from . import views
from .views import MyTokenObtainPairView
# Authentication
#from rest_framework_simplejwt.views import TokenObtainPairView




urlpatterns = [
    #CRUD
    #path('', views.index),
    path('books', views.books),
    path('books/<id>', views.books),
    
    #Authentucation
    #Login/SignIn
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #Register/SignUp
    path('register/', views.addUser),
]