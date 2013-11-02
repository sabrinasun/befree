from django import forms
from core.models import Material, GiverMaterial, Author, Publisher

class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['typ'].label = "Type"
    
    class Meta:
        model = Material
        exclude = ('create_date')

        
class GiverMaterialForm(forms.ModelForm):
    
    class Meta:
        model = GiverMaterial
        exclude = ('create_date')
        widgets = {
        'giver': forms.HiddenInput(attrs={'readonly':'True'})
        }
        
        
class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author

class PublisherForm(forms.ModelForm):
    
    class Meta:
        model = Publisher
