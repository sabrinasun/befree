from django import forms
from core.models import Material, Author, Publisher

class MaterialForm(forms.ModelForm):
    
    class Meta:
        model = Material
        exclude = ('create_date')

class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author

class PublisherForm(forms.ModelForm):
    
    class Meta:
        model = Publisher
