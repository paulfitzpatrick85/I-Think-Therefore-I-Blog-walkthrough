from .models import Comment
from django import forms


# tell comment form what model to use and which field to display
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)  # , makes python read as tuple and not string