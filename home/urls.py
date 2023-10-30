from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [ 
    path('',views.index, name="index"),
    path('login',views.loginUser, name="login"),
    path('marking',views.marking, name="marking"),
    path('calculate',views.calculate, name="calculate"),
    path('Changepassword',views.changepwd, name="Changepassword"),
    path('administrator',views.admin, name="admin"),
    path('logout/',views.logoutUser, name="logout"),
   # path('tea_login',views.tea_login, name="Teacherlogin"),
]
