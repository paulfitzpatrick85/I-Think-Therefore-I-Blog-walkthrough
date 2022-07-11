from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home') # since using class based views, need to add 'as views' 
]