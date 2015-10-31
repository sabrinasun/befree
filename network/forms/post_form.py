from django import forms

from network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('last_update', 'user')