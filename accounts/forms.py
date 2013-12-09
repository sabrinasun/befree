import time
from django import forms
from django.db import IntegrityError
from django.utils.text import slugify
from userena.forms import SignupFormOnlyEmail as UserenaSignupForm
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

STATE_CHOICES = (
    ("", "----------"),
    ("AL", "Alabama"),
    ("AK","Alaska"),
    ("AS","American Samoa"),
    ("AZ","Arizona"),
    ("AR","Arkansas"),
    ("AA","Armed Forces Americas"),
    ("AE","Armed Forces Europe"),
    ("AP","Armed Forces Pacific"),
    ("CA","California"),
    ("CO","Colorado"),
    ("CT","Connecticut"),
    ("DE","Delaware"),
    ("DC","District of Columbia"),
    ("FM","Federated States of Micronesia"),
    ("FL","Florida"),
    ("GA","Georgia"),
    ("GU","Guam"),
    ("HI","Hawaii"),
    ("ID","Idaho"),
    ("IL","Illinois"),
    ("IN","Indiana"),
    ("IA","Iowa"),
    ("KS","Kansas"),
    ("KY","Kentucky"),
    ("LA","Louisiana"),
    ("ME","Maine"),
    ("MH","Marshall Islands"),
    ("MD","Maryland"),
    ("MA","MA"),
    ("MI","Michigan"),
    ("MN","Minnesota"),
    ("MS","Mississippi"),
    ("MO","Missouri"),
    ("MT","Montana"),
    ("NE","Nebraska"),
    ("NV","Nevada"),
    ("NH","New Hampshire"),
    ("NJ","New Jersey"),
    ("NM","New Mexico"),
    ("NY","New York"),
    ("NC","North Carolina"),
    ("ND","North Dakota"),
    ("MP","Northern Mariana Islands"),
    ("OH","Ohio"),
    ("OK","Oklahoma"),
    ("OR","Oregon"),
    ("PW","Palau"),
    ("PA","Pennsylvania"),
    ("PR","Puerto Rico"),
    ("RI","Rhode Island"),
    ("SC","South Carolina"),
    ("SD","South Dakota"),
    ("TN","Tennessee"),
    ("TX","Texas"),
    ("UM","U.S. Minor Outlying Islands"),
    ("UT","Utah"),
    ("VT","Vermont"),
    ("VI","Virgin Islands"),
    ("VA","Virginia"),
    ("WA","Washington"),
    ("WV","West Virginia"),
    ("WI","Wisconsin"),
    ("WY","Wyoming"),
                 
)

attrs_dict = {'class': 'required'}
class UserenaSignupFormBase(UserenaSignupForm):
    def __init__(self, *args, **kwargs):
        super(UserenaSignupFormBase, self).__init__(*args, **kwargs)
        self.fields['country'].initial = "US"    
    
    """ Add a Terms of Service button to the ``SignupForm``. """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), \
                             label='I have read and agree to the Terms of Service', \
                             error_messages={'required': 'You must agree to the terms to register.'})
    state =  forms.ChoiceField(choices = STATE_CHOICES)      
        
    country = forms.ChoiceField(choices = countries.COUNTRIES, initial="US", required = True)  
    
    def save(self):
        user = super(UserenaSignupFormBase, self).save()
        profile = user.get_profile()
        profile.state = self.cleaned_data['state']
        profile.country = self.cleaned_data['country']    
        profile.save()
        
        return user

class SignupReaderForm(UserenaSignupFormBase):
    first_name = forms.CharField()
    last_name = forms.CharField()
    address1 = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=255, required = False)
    city = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(SignupReaderForm, self).__init__(*args, **kwargs)
        
    def save(self):
        user = super(SignupReaderForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = user.get_profile()
        profile.address1 = self.cleaned_data['address1']
        profile.address2 = self.cleaned_data['address2']
        profile.city = self.cleaned_data['city']
        profile.is_reader = True
        profile.save()
        return user

class SignupForm(UserenaSignupFormBase):
    first_name = forms.CharField(required=False) #first name/last name not required
    last_name = forms.CharField(required=False)    
    screen_name = forms.CharField()  
    paypal_email = forms.EmailField(required=False)
    other_means = forms.CharField(widget=forms.Textarea, required=False)
    free_domestic_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    free_international_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    max_number_per_order = forms.ChoiceField(choices=NUM_CHOICES, initial='5')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
    def clean_free_domestic_shipping(self):
        return True if self.cleaned_data['free_domestic_shipping']=='True' else False

    def clean_free_international_shipping(self):
        return True if self.cleaned_data['free_international_shipping']=='True' else False

    def clean(self):
        data = self.cleaned_data
        paypal_email = data.get('paypal_email', '')
        other_means = data.get('other_means', '')
        if not paypal_email and not other_means:
            raise forms.ValidationError("Please enter either paypal_email or other means to pay, so buyers can pay you. If all your items are always free, then declare so in other payment methods field.")
        return data

    def save(self):
        user = super(SignupForm, self).save()
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
        profile.is_giver = True  
        
        profile.save()
        return user

class EditProfileForm(UserenaEditProfileForm):
    max_per_order = forms.ChoiceField(choices = NUM_CHOICES, initial='5')
    state = forms.ChoiceField(choices = STATE_CHOICES)    

    def clean(self):
        data = self.cleaned_data
        is_reader = data.get('is_reader', '')
        is_giver = data.get('is_giver', '')
        if not is_reader and not is_giver:
            raise forms.ValidationError('Please select either "I am a giver" or "I am a reader".')
        
        reader_fields = {'first_name':"First Name",
                         'last_name':"Last Name",
                         'address1':"Address 1",
                         'city':"City",
                         'zipcode':"Zip Code"}
        if is_reader:
            for key in reader_fields.keys(): 
                value = data.get(key, '')
                if not value:
                    raise forms.ValidationError('Field '+reader_fields[key]+" is required for reader profile. ")
        
        if is_giver:
            if not data.get("screen_name"):
                raise forms.ValidationError("Field Public Name is required for giver profile. ")
            if not data.get("paypal_email") and not data.get("email_description"):
                raise forms.ValidationError("Either Paypal Email or Other Payment Methods is required for giver profile. ")
       
        return data    
    
    class Meta:
        model = Profile
        exclude = ('user', 'status', 'privacy','create_date')
