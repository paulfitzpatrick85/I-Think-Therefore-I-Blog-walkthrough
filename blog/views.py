from django.shortcuts import render, get_list_or_404
from django.views import generic, View
from .models import Post


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')  # contents of post table
    template_name = 'index.html'     # html file that view will render
    paginate_by = 6           # limit number of post to 6, if there are more django will add page navagation


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):    
        queryset = Post.objects.filter(status=1)   # status = 1 filters only active posts
        post = get_object_or_404(queryset, slug=slug)  # getting post by slug as slug is unique for each post
        comments = post.comments.filter(approved=True).order_by("-created_on") # filter by only approved  and oldest firt comments
        liked = False     # defaulted to false
        if post.likes.filter(id=self.request.user.id).exists():   # only registered/signed in user can like post
            liked = True

        return render(
            request,            
            "post_detail.html",       # render to this page
            {
                "post": post,          #render dictionary
                "comments": comments,
                "liked": liked
            },
        )
