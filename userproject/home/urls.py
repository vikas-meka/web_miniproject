from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [ 
    path('',views.index, name="index"),
    path('login',views.loginUser, name="login"),
    path('marking',views.marking, name="marking"),
    path('calculate',views.calculate, name="calculate"),
    path('add_delete_student',views.add_delete_student, name="ADD/DELETE"),
    path('add_delete_course',views.add_delete_course, name="ADD/DELETE"),
    path('administrator',views.admin, name="admin"),
    path('logout/',views.logoutUser, name="logout"),
   # path('tea_login',views.tea_login, name="Teacherlogin"),
]
