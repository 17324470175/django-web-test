"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from blog.views import post_list, post_detail
from config.views import links
from .custom_site import custom_site

urlpatterns = [
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='admin'),
    path('', post_list, name='index'),
    # 通过定义(?P<category_id>\d+)把url这个位置的字符作为category_id的参数传递给post_list
    path('category/<int:category_id>/', post_list, name='category-list'),
    path('tag/<int:tag_id>/', post_list, name='tag-list'),
    path('post/<int:post_id>.html', post_detail, name='post-detail'),
    path('links/', links, name='links'),

]
