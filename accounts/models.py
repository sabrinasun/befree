from django.db import models
from django.utils import timezone
from django_countries import CountryField

from userena.utils import get_user_model
from userena.models import UserenaBaseProfile
from core.models import Publisher
from django.core.exceptions import ValidationError

TYPE_CHOICES = (
    #('TEM/ORG', 'Temple/Organization'),
    ('TEA', 'Buddhist Teacher'),
    ('BUD', 'Regular Buddhist'),
    ('Other', 'Other'),
)

STATUS_CHOICES = (
    ('REG', 'Registerd'),
    ('ACT', 'Active'),
    ('DEA', 'Dead'),
)


class Profile(UserenaBaseProfile):
    user = models.ForeignKey(get_user_model(), unique=True)
    screen_name = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=50)
    country = CountryField(max_length=50)    

    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True)
    #is_nonprofit = models.BooleanField(default=False)
    paypal_email = models.EmailField(max_length=100, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)

    create_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    payment_description = models.TextField(blank=True)
    pickup_description = models.TextField(blank=True)
    max_per_order = models.PositiveIntegerField(default=0)
    
    local_pickup = models.BooleanField(default=False)
    domestic_pay_shipping  = models.BooleanField(default=False)
    domestic_free_shipping = models.BooleanField(default=False)
    international_free_shipping = models.BooleanField(default=False)
    
    payinfo_for_donation = models.BooleanField(default=False)
    
    donation = models.TextField(blank=True)
        
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    #is_reader = models.BooleanField(default=False)
    #is_giver  = models.BooleanField(default=False)
    #is_public = models.BooleanField(default=False)

    def get_shipping_address(self):
        ret = self.user.first_name + " " + self.user.last_name + ", "
        ret += self.address1 +", "
        if self.address2: 
            ret += self.address2+", "
        ret += self.city  + ", " + self.state  + " " + self.zipcode + ", "
        ret += self.get_country_display()
        return ret
    
    def get_location(self):
        lst = []
        """
        for attr in ('address1', 'address2', 'city', 'state', 'country'):
            if hasattr(self, attr) and getattr(self, attr):
                lst.append(getattr(self, attr))
        """
        location = self.state + ", " + self.get_country_display()
        return location
    
    def get_display_name(self):
        ret = self.screen_name
        if not ret: 
            ret = self.user.first_name
        if not ret: 
            ret = self.user.username
        return ret
    
    def validate_reader(self,first_name, last_name, address1, city, zipcode):
        if not first_name: 
          raise ValidationError("First Name is required.")
        if not last_name: 
          raise ValidationError("Last Name is required. ")
        if not address1: 
          raise ValidationError("Address1 is required. ")
        if not city:
          raise ValidationError("City is required. ")
        if not zipcode:
          raise ValidationError("Zipcode is required. ")
            
    def validate_giver(self, local_pickup, domestic_pay_shipping,domestic_free_shipping,international_free_shipping,pickup_description, paypal_email, payment_description):
        if not local_pickup and not domestic_pay_shipping \
            and not domestic_pay_shipping and not international_free_shipping: 
            raise ValidationError("Please choose at least one distribution method. ")
        if domestic_pay_shipping and domestic_free_shipping:
            raise ValidationError("Please choose either  Free Domestic Shipping or Receive Payment for Domestic Shipping, not both.")
        if local_pickup and not pickup_description: 
            raise ValidationError("Since you allow user to pickup locally, please provide pickup instruction. ")
        if domestic_pay_shipping and not ( paypal_email or payment_description):
            raise ValidationError("Sorry receivers need to pay your for shipping. Either Paypal Email or Other Payment Methods is required for giver profile. ")

    
    def has_reader_profile(self):
        #has shipping information all filled in
        try:
           self.validate_reader( self.user.first_name,  self.user.last_name, self.address1, self.city, self.zipcode)
        except:
           return False
       
        return True
            
    def has_giver_profile(self):
        try: 
            self.validate_giver(self.local_pickup, self.domestic_pay_shipping, self.domestic_free_shipping, \
                          self.international_free_shipping, self.pickup_description, self.paypal_email, self.payment_description)
        except:
            return False
        
        return True