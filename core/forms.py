from django import forms
from core.models import Material, GiverMaterial, Author, Publisher
from core.widgets import SelectWithPopUp


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['typ'].label = "Type"
        self.fields['author'].help_text = ''
        self.fields['author'] = forms.ModelChoiceField(Author.objects.all(), widget=SelectWithPopUp)
        self.fields['publisher'] = forms.ModelChoiceField(Publisher.objects.all(), widget=SelectWithPopUp)
        
    
    class Meta:
        model = Material
        exclude = ('create_date')
        
    def clean(self):
        cleaned_data = super(MaterialForm, self).clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        materials = Material.objects.filter(title=title)
        authors_list = []
        if materials:
            for mater in materials:
                for auth in mater.author.values("pk"):
                    authors_list.append(auth["pk"])
            form_author_list = [a.pk for a in author]
            if authors_list == form_author_list:
                if self.instance.pk:
                    if list(self.instance.author.all()) == list(author):
                        return cleaned_data
                raise forms.ValidationError("The material with this title and author alredy exist.")
        return cleaned_data
        

        
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
