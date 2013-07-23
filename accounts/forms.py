from django import forms
from userena.forms import SignupForm as UserenaSignupForm

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

class SignupForm(UserenaSignupForm):
    screen_name = forms.CharField(required=False)
    paypal_email = forms.EmailField(required=False)
    other_means = forms.CharField(widget=forms.Textarea, required=False)
    free_domestic_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    free_international_shipping = forms.ChoiceField(widget=forms.CheckboxInput, required=False, choices=BOOL_CHOICES)
    max_number_per_order = forms.ChoiceField(choices=NUM_CHOICES)

    def clean_free_domestic_shipping(self):
        return True if self.cleaned_data['free_domestic_shipping']=='True' else False

    def clean_free_international_shipping(self):
        return True if self.cleaned_data['free_international_shipping']=='True' else False

    def save(self):
        user = super(SignupForm, self).save()
        profile = user.get_profile()
        profile.screen_name = self.cleaned_data['screen_name']
        profile.paypal_email = self.cleaned_data['paypal_email']
        profile.description = self.cleaned_data['other_means']
        profile.domestic_free_shipping = self.cleaned_data['free_domestic_shipping']
        profile.international_free_shipping = self.cleaned_data['free_international_shipping']
        profile.max_per_order = self.cleaned_data['max_number_per_order']
        profile.status = 'REG'
        profile.save()
        return user
