from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'cover_image', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 14}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': ''}
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Write a comment...',
            }),
        }