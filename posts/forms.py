from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "maxlength": 280, "placeholder": "O que esta acontecendo?"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 2, "maxlength": 280, "placeholder": "Escreva um comentario..."}),
        }
