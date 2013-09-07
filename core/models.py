from django.db import models
from django.utils import timezone
from userena.utils import get_user_model
from accounts.models import Profile

class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

TYPE_CHOICES = (
    ('Book', 'Book'),
    ('CD', 'CD'),
    ('DVD', 'DVD'),
)

LAN_CHOICES = (
    ('English', 'English'),
    ('Chinese', 'Chinese'),
    ('French', 'French'),
    ('Hindi', 'Hindi'),
    ('Indonesian', 'Indonesian'),
    ('Italy', 'Italy'),
    ('Spanish', 'Spanish'),
    ('Thai', 'Thai'),
    ('Tibetan', 'Tibetan'),
    ('Vietnamese', 'Vietnamese'),
)

CONDITION_CHOICES = (
    ('NE', 'NE'),
    ('LN', 'LN'),
    ('GO for New', 'GO for New'),
    ('Like New', 'Like New'),
    ('Good', 'Good'),
)

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

class Material(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, null=True, blank=True)
    giver = models.ForeignKey(get_user_model())
    isbn = models.CharField(max_length=100, blank=True)
    publisher_book_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Book')
    pages = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    create_date = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=10, choices=LAN_CHOICES, blank=True)
    pic = models.ImageField(upload_to='pic', null=True, blank=True, verbose_name="Upload Cover Picture")
    pdf = models.FileField(upload_to='pdf', null=True, blank=True, verbose_name='Upload PDF File')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='Good')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __unicode__(self):
        return self.title

    def get_author_names(self):
        return ', '.join(a.name for a in self.author.all())
    
    def get_quantity_nums(self):
        return range(1, self.quantity + 1)
    
    @models.permalink
    def get_absolute_url(self):
        return ('account_material_edit', (), dict(material_id=self.id))

class GiverMaterial(models.Model):
    giver = models.ForeignKey(get_user_model())
    material = models.ForeignKey(Material)
    count = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    create_date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

class Order(models.Model):
    reader = models.ForeignKey(get_user_model())
    material = models.ForeignKey(Material)
    quantity = models.PositiveIntegerField(default=1)
    
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    order_date = models.DateTimeField(default=timezone.now)
    ship_date = models.DateTimeField(null=True, blank=True)
    pay_date = models.DateTimeField(null=True, blank=True)
    payment_detail = models.TextField(blank=True)

    def get_total_price(self):
        return self.material.price * self.quantity
