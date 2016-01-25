from django import forms

from network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('last_update', 'user')

    def save(self, commit=False):
        post = super(forms.ModelForm, self).save(commit)
        parts = post.link.split('://')
        post.link_http_mode, post.link = parts[0], parts[1] if len(parts) > 1 and parts[0].startswith('http') else None
        return post
