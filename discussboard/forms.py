from django import forms
from .models import Post, Comment, LikedComment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class LikedCommentForm(forms.ModelForm):
    class Meta:
        model = LikedComment
        fields = ('value',)