from django.shortcuts import render, get_object_or_404, reverse  # rev - look up url by url name in urls .py
from django.views import generic, View 
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')  # contents of post table
    template_name = 'index.html'     # html file that view will render
    paginate_by = 6           # limit number of post to 6, if there are more django will add page navagation


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):    
        queryset = Post.objects.filter(status=1)   # status = 1 filters only active posts
        post = get_object_or_404(queryset, slug=slug)  # getting post by slug as slug is unique for each post
        comments = post.comments.filter(approved=True).order_by("-created_on")  # filter by only approved  and oldest firt comments
        liked = False     # defaulted to false
        if post.likes.filter(id=self.request.user.id).exists():   # only registered/signed in user can like post
            liked = True

        return render(
            request,            
            "post_detail.html",       # render to this page
            {
                "post": post,          # render dictionary
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):    
        queryset = Post.objects.filter(status=1)   # status = 1 filters only active posts
        post = get_object_or_404(queryset, slug=slug)  # getting post by slug as slug is unique for each post
        comments = post.comments.filter(approved=True).order_by("-created_on") # filter by only approved  and oldest firt comments
        liked = False     #  defaulted to false
        if post.likes.filter(id=self.request.user.id).exists():   # only registered/signed in user can like post
            liked = True

        # get data posted from form and put in variable
        comment_form = CommentForm(data=request.POST)
        # if form in filled in correctly, auto fill these fields from logged in user info
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)    # not commited to database yet (not until a post is assigned to it)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()  # return empty comment form instance
 
        return render(
            request,            
            "post_detail.html",       # render to this page
            {
                "post": post,          # render dictionary
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked,
                
            },
        )

    
    class PostLike(View):
        def post(self, request, slug):
            post = get_object_or_404(queryset, slug=slug)  # getting post by slug as slug is unique for each post
            # toggle 'like' status by checking if already liked or not
            if post.likes.filter(id=request.user.id).exists():  # if user id exists than post has been liked
                post.likes.remove(request.user)                 # so it can be removed
            else:
                post.likes.add(request.user)                    # add the like

            # reload post_detail template to see results, import HttpResponseRedirect  and reverse at top of page
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))  # page reloads on like/unlike

