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

# helper function
    def number_of_likes(self):
        return self.likes.count()      # return total number of likes on post




class Comment(models.Model):
    