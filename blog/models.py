from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

# Weather post is draft or published/live
STATUS = ((0, 'Draft'), (1, 'Published'))


# take ERD and convert in django model
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # if user is deleted, their posts are too
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-created_on']  # order post by create_on, from above, '-' means use descending order

    # use on project, return string representation of obj
    def __str__(self):
        return self.title

# helper method to return total number of likes on post
    def number_of_likes(self):
        return self.likes.count()   


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    approved = models.BooleanField(default=False)   

    class Meta:
        ordering = ['created_on']  # ascending order, so oldest comments are listed first

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
