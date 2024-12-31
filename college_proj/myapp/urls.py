from django.urls import path
from .import views

urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('reg',views.reg,name='reg'),
    path('user_create',views.user_create,name='user_create'),
    path('login_func',views.login_func,name='login_func'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('user_home',views.user_home,name='user_home'),
    path('log_out',views.log_out,name='log_out'),
    path('course',views.course,name='course'),
    path('add_course',views.add_course,name='add_course'),
    path('add_stud',views.add_stud,name='add_stud'),
    path('add_student',views.add_student,name='add_student'),
    path('stud_details',views.stud_details,name='stud_details'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('edit_details/<int:id>',views.edit_details,name='edit_details'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('teacher_details',views.teacher_details,name='teacher_details'),
    path('delete_tchr/<int:id>',views.delete_tchr,name='delete_tchr'),
    path('card',views.card,name='card'),
    
    path('edit_teacher',views.edit_teacher,name='edit_teacher'),
    path('edit_tr/<int:id>',views.edit_tr,name='edit_tr'),
]