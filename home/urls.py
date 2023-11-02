from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [ 
    path('',views.index, name="index"),
    path('login',views.loginUser, name="login"),
    path('student',views.student, name="student"),
    path('admin_login',views.admin_login, name="login"),
    path('admin_logout',views.admin_logout, name="logout"),
    path('marking',views.marking, name="marking"),
    path('calculate',views.calculate, name="calculate"),
    path('add_student',views.add_student, name="ADD"),
    path('delete_student',views.delete_student, name="DELETE"),
    path('add_delete_student',views.add_delete_student, name="ADD/DELETE"),
    path('add_delete_course',views.add_delete_course, name="ADD/DELETE"),
    path('add_course',views.add_course, name="ADD"),
    path('delete_course',views.delete_course, name="DELETE"),    
    path('administrator',views.admin, name="admin"),
    path('change_pwd',views.change_pwd, name="change password"),
    path('logout/',views.logoutUser, name="logout"),
   # path('tea_login',views.tea_login, name="Teacherlogin"),
]
