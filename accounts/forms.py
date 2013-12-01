import time
from django import forms
from django.db import IntegrityError
from django.utils.text import slugify
from userena.forms import SignupForm as UserenaSignupForm
from userena.forms import EditProfileForm as UserenaEditProfileForm
from accounts.models import Profile
from django_countries import countries 

NUM_CHOICES = (
    ('-1', 'Unlimitted'),
    ('1', '1'),
    ('3', '3'),
    ('5', '5'),
    ('10', '10'),
    ('20', '20'),
    ('30', '30'),
    ('40', '40'),
    ('50', '50'),
)

BOOL_CHOICES = (
    (True, True),
    (False, False),
)

class SignupReaderForm(UserenaSignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address1 = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=255, required = False)
    city = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    country = forms.ChoiceField(choices = countries.COUNTRIES, initial="US", )

    def __init__(self, *args, **kwargs):
        super(SignupReaderForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['country'].initial = "US"
    
    def clean(self):
        data = self.cleaned_data
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        data['username'] = slugify(first_name + last_name)

        return data
    
    def save(self):
        try:
            user = super(SignupReaderForm, self).save()
        except IntegrityError:
            self.cleaned_data['username'] += str(int(time.time()))
            user = super(SignupReaderForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = user.get_profile()
        profile.address1 = self.cleaned_data['address1']
        profile.address2 = self.cleaned_data['address2']
        profile.city = self.cleaned_data['city']
        profile.state = self.cleaned_data['state']
        profile.country = self.cleaned_data['country']
        profile.save()
        return user

class SignupForm(UserenaSignupForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    screen_name = forms.CharField(required=False)  
    paypal_email = forms.EmailField(required=False)
    other_means = forms.CharField(widget=forms.Textarea, required=False)
    free_domestic_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    free_international_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    max_number_per_order = forms.ChoiceField(choices=NUM_CHOICES, initial='5')
    state = forms.CharField(max_length=50, required = True)
    country = forms.ChoiceField(choices = countries.COUNTRIES, initial="US", required = True)    

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].widget = forms.HiddenInput()
        
               

    def clean_free_domestic_shipping(self):
        return True if self.cleaned_data['free_domestic_shipping']=='True' else False

    def clean_free_international_shipping(self):
        return True if self.cleaned_data['free_international_shipping']=='True' else False

    def clean(self):
        data = self.cleaned_data
        screen_name = data.get('screen_name', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        if screen_name:
            data['username'] = slugify(screen_name)
        elif first_name + last_name:
            data['username'] = slugify(first_name + last_name)
        else:
            raise forms.ValidationError('Please input Public Name.')
        return data

    def save(self):
        try:
            user = super(SignupForm, self).save()
        except IntegrityError:
            self.cleaned_data['username'] += str(int(time.time()))
            user = super(SignupForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        profile = user.get_profile()
        profile.screen_name = self.cleaned_data['screen_name']
        profile.paypal_email = self.cleaned_data['paypal_email']
        profile.description = self.cleaned_data['other_means']
        profile.domestic_free_shipping = self.cleaned_data['free_domestic_shipping']
        profile.international_free_shipping = self.cleaned_data['free_international_shipping']
        profile.max_per_order = self.cleaned_data['max_number_per_order']
        profile.status = 'REG'
        profile.state = self.cleaned_data['state']
        profile.country = self.cleaned_data['country']        
        
        profile.save()
        return user

class EditProfileForm(UserenaEditProfileForm):
    max_per_order = forms.ChoiceField(choices=NUM_CHOICES, initial='5')
    
    class Meta:
        model = Profile
        exclude = ('user', 'status', 'privacy','create_date')
