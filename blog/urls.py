from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),  # since using class based views, need to add 'as views' 
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),  
    # 1st slug ins path converter, 2nd is a keyword name, in this case,
    #  slug keyword matches 'slug' parameter in the get method of the post_detail class in blog/views.py,
    #  thats how they are linked
]