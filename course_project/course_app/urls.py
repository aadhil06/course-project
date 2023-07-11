from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('course/list/', views.course_list, name='course_list'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/update/<int:course_id>/', views.update_course, name='update_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_view/', views.my_view, name='myview'),
    
]
