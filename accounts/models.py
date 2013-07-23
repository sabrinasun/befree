from django.db import models
from django.utils import timezone
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
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
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
