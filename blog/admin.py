from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}  # populate slug(form?) from title
    list_filter = ('status', 'created_on')  # will create filter window/box with status and created today, last 7 days etc
    list_display = ('title', 'slug', 'status', 'created_on')  # titles/info on each post
    search_fields = ('title', 'content')  # add search bar in admin page

    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']     # approve comment box in admin, actions can take list of functions

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)    # approve is boolean which is false by default, this updates quearyset to true