from django import forms
from django.forms import inlineformset_factory

from .models import Comment, Post, PostImage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'cover_image', 'content', 'status']
        labels = {'cover_image': 'Cover image'}
        help_texts = {
            'cover_image': 'The main photo, shown on the article card and at the top of the article.',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 14}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


PostImageFormSet = inlineformset_factory(
    Post,
    PostImage,
    fields=['image', 'caption'],
    extra=4,            # number of empty photo slots shown
    can_delete=True,    # lets authors remove a saved photo
    widgets={
        'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caption (optional)'}),
    },
)


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