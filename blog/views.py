from django.shortcuts import render
from django.views import generic
from .models import Post


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')  # contents of post table
    template_name = 'index.html' # html file that view will render
    paginate_by = 6  # limit number of post to 6, if there are more django will add page navagation

# Create your views here.
