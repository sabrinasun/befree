from django import forms
from network.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('last_update', 'user')
    #def clean_language(self):
     #   return "en"
    
    def clean_title(self):
        return ""
    
    def clean_content(self):
        content = self.cleaned_data["content"]
        return content
    
    #not used
    def save(self, commit=False):
        form = super(forms.ModelForm, self)
        form.save(commit)

        #parts = post.link.split('://')
        #post.link_http_mode, post.link = parts[0], parts[1] if len(parts) > 1 and parts[0].startswith('http') else None
        return form
