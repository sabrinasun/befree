from django import forms

from core.models import Material, GiverMaterial, Author, Publisher


class ContactForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(widget=forms.Textarea)


class PayForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput)
    pay_method = forms.CharField(widget=forms.RadioSelect,
                                 error_messages={'required': "Please select one payment method that applies."})
    message = forms.CharField(widget=forms.Textarea, required=False)


class ShippingCostForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput)
    shipping_cost = forms.DecimalField(max_digits=8, decimal_places=2)


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        # self.fields['print_free_distribution_id'].choices = [(r.id,r.get_display_name()) for r in Profile.objects.filter(print_free_distribution=True)]
        # self.fields['typ'].label = "Type"
        #self.fields['author'].help_text = ''
        #self.fields['author'] = forms.ModelChoiceField(Author.objects.all())
        #self.fields['publisher'] = forms.ModelChoiceField(Publisher.objects.all(), widget=SelectWithPopUp)


    class Meta:
        model = Material
        exclude = ('create_date')

    def clean(self):
        cleaned_data = super(MaterialForm, self).clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        materials = Material.objects.filter(title=title)
        authors_list = []
        # materials = Material.objects.filter(title=title).exclude(id=self.instance.pk)

        if materials:
            for mater in materials:
                for auth in mater.author.values("pk"):
                    authors_list.append(auth["pk"])
            form_author_list = author
            if authors_list == form_author_list:
                if self.instance.pk:
                    if list(self.instance.author.all()) == list(author):
                        return cleaned_data
                raise forms.ValidationError("The material with this title and author alredy exist.")


                # if author == mater.author:
                #    raise forms.ValidationError("The material with this title and author alredy exist.")

        pages = cleaned_data.get('pages')
        weight = cleaned_data.get('weight')
        if weight == 0:
            raise forms.ValidationError("This book should weight more than 0 lb.")

        if pages == 0:
            raise forms.ValidationError("This book should have more than one page.")

        return cleaned_data


class GiverMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GiverMaterialForm, self).__init__(*args, **kwargs)
        self.fields['note'].label = "Why did you choose this book? Do you have any thought to share about this book:"

    class Meta:
        model = GiverMaterial
        exclude = ('create_date')
        widgets = {
            'giver': forms.HiddenInput(attrs={'readonly': 'True'}),
            'price': forms.HiddenInput(attrs={'readonly': 'True'})
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
