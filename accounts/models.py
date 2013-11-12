from django.db import models
from django.utils import timezone
from django_countries import CountryField

from userena.utils import get_user_model
from userena.models import UserenaBaseProfile

TYPE_CHOICES = (
    ('TEM/ORG', 'Temple/Organization'),
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

    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50)
    country = CountryField(max_length=50)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True)
    is_nonprofit = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    paypal_email = models.EmailField(max_length=100, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)

    create_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    payment_description = models.TextField(blank=True)
    max_per_order = models.PositiveIntegerField(default=0)
    international_free_shipping = models.BooleanField(default=False)
    domestic_free_shipping = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

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
        
        
            
