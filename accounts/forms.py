import time
from django import forms
from django.db import IntegrityError
from django.utils.text import slugify
from userena.forms import SignupForm as UserenaSignupForm
from userena.forms import EditProfileForm as UserenaEditProfileForm
from accounts.models import Profile
from django_countries import countries
from core.models import Order, GiverMaterial

USERNAME_RE = r'^[\.\w]+$'

NUM_CHOICES = (
    ('0', 'Unlimitted'),  # nobody will choose 0 for this, so it means unlimitted.
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
    ("AK", "Alaska"),
    ("AS", "American Samoa"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("AA", "Armed Forces Americas"),
    ("AE", "Armed Forces Europe"),
    ("AP", "Armed Forces Pacific"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District of Columbia"),
    ("FM", "Federated States of Micronesia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("GU", "Guam"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MH", "Marshall Islands"),
    ("MD", "Maryland"),
    ("MA", "MA"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("MP", "Northern Mariana Islands"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PW", "Palau"),
    ("PA", "Pennsylvania"),
    ("PR", "Puerto Rico"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UM", "U.S. Minor Outlying Islands"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VI", "Virgin Islands"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),

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
    # username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Your real name or nick name.'}))

    us_state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    state = forms.CharField(max_length=50)

    country = forms.ChoiceField(choices=countries.COUNTRIES, initial="US", required=True)

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
    address2 = forms.CharField(max_length=255, required=False)
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
        # profile.is_reader = True
        profile.zipcode = self.cleaned_data['zipcode']
        profile.save()
        return user


"""
class SignupForm(UserenaSignupFormBase):
    first_name = forms.CharField(required=False) #first name/last name not required
    last_name = forms.CharField(required=False)    
    screen_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your real name or nick name.'}))  
    paypal_email = forms.EmailField(required=False)
    other_means = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ask users to mail you a check, provide instruction and mailing address here. '}), required=False)
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
        #profile.is_giver = True  
        
        profile.save()
        return user
"""

from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena.utils import get_profile_model, get_user_model


class EditProfileForm(UserenaEditProfileForm):
    max_per_order = forms.ChoiceField(choices=NUM_CHOICES, initial='5')
    us_state = forms.ChoiceField(choices=STATE_CHOICES)
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                error_messages={
                                    'invalid': 'Username must contain only letters, numbers, dots and underscores.'})


    # validate_receiver = forms.CharField()
    check_receiver = forms.BooleanField()
    check_giver = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.validate_receiver = args[0].get('validate_receiver', False)
            self.validate_giver = args[0].get('validate_giver', False)

        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        Also validates that the username is not listed in
        ``USERENA_FORBIDDEN_USERNAMES`` list.

        """
        username = self.cleaned_data['username']
        user = None
        try:
            user = get_user_model().objects.get(username__iexact=username)
        except get_user_model().DoesNotExist:
            pass

        else:
            if UserenaSignup.objects.filter(user__username__iexact=username).exclude(
                    activation_key=userena_settings.USERENA_ACTIVATED):
                raise forms.ValidationError(
                    'This username is already taken but not confirmed. Please check you email for verification steps.')
            if user.id != self.instance.user.id:
                raise forms.ValidationError('This username is already taken.')
        if username.lower() in userena_settings.USERENA_FORBIDDEN_USERNAMES:
            raise forms.ValidationError('This username is not allowed.')
        return username

    def clean(self):
        rawdata = self.data
        data = self.cleaned_data
        user = self.instance.user

        # check if have pending reader order
        is_reading = Order.objects.filter(reader=user, status__in=('NEW', 'PENDING', 'PAID',)).count()

        # check if have pending giver order or displayed giver inventory
        is_giving = Order.objects.filter(giver=user, status__in=('NEW', 'PENDING',)).count() > 0 or \
                    GiverMaterial.objects.filter(giver=user, status__in=('ACTIVE')).count() > 0

        if is_reading or self.validate_receiver or rawdata.get('check_receiver',
                                                               False):  # if have pending reader orders in the last month
            self.instance.validate_reader(data['first_name'], data['last_name'], data['address1'], data['city'],
                                          data['zipcode'])

        if is_giving or self.validate_giver or rawdata.get('check_giver',
                                                           False):  # if have pending giver orders or inventory
            self.instance.validate_giver(data['local_pickup'], \
                                         data['domestic_pay_shipping'], \
                                         data['domestic_free_shipping'], \
                                         data['international_free_shipping'], \
                                         data['pickup_description'], \
                                         data['paypal_email'], \
                                         data['payment_description']
                                         )

        return data

    def save(self):
        profile = super(UserenaEditProfileForm, self).save()
        profile.user.username = self.cleaned_data['username']
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.save()

    class Meta:
        model = Profile
        exclude = ('user', 'status', 'privacy', 'create_date')
