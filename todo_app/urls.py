"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # Todo
    path('', views.home, name='home'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('completed/', views.completed_todos, name="completed_todos"),
    path('create/', views.create_todo, name="create_todo"),
    path('todo/<int:todo_id>', views.view_todo, name="view_todo"),
    path('todo/<int:todo_id>/completed',
         views.completed_todo, name="completed_todo"),
    path('todo/<int:todo_id>/delete',
         views.delete_todo, name="delete_todo"),
]
