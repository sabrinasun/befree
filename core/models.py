from django.db import models
from django.utils import timezone
from userena.utils import get_user_model
#from accounts.models import Profile
 
class Author(models.Model): 
    name = models.CharField(max_length=100, unique=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    website  = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    donate_url = models.URLField(max_length=255, null=True, blank=True)
    donate_note =  models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=255, null=True, blank=True)    
    description = models.TextField(blank=True)
    publish_free_book = models.BooleanField(default=False)
    donate_url = models.URLField(max_length=255, null=True, blank=True)
    donate_note =  models.TextField(blank=True)
    #contact = models.ForeignKey(get_user_model(), null=True, blank=True)

    def __unicode__(self):
        return self.name
    

class Tag(models.Model):
    name =  models.CharField(max_length=256)

TYPE_CHOICES = (
    ('Book', 'Book'),
    ('CD', 'CD'),
    ('DVD', 'DVD'),
)

#http://www.science.co.il/Language/Locale-codes.asp
LAN_CHOICES = (
    ('en', 'English'),
    ('zh', 'Chinese'), 
    ('o','Other')
)

CONDITION_CHOICES = (
    ('NEW', 'New' ),
    ('LN', 'Like New'),
    ('GOOD','Good'),
    ('OK', 'OK')
)

STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
)

ORDER_STATUS_CHOICES = (
    ('NEW', 'New'),
    ('PENDING', 'Pending'), 
    ('CANCEL', 'Cancel'),
    ('PAID','Paid'),
    ('SHIPPED','Shipped'),
)

def cover_pic_name(instance, filename):
    return "pic/book_"+str(instance.pk)+"_cover_"+filename

def pdf_name(instance, filename):
    return "pdf/book_"+str(instance.pk)+"_pdf_"+filename

class Material(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    isbn_10 = models.CharField(max_length=100, blank=True, null=True)
    isbn_13 = models.CharField(max_length=100, blank=True, null=True)
    publisher_book_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    pages = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    #weight_is_estimated = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    language = models.CharField(max_length=10, choices=LAN_CHOICES)
    pic = models.ImageField(upload_to=cover_pic_name, null=True, blank=True,  verbose_name="Upload Cover Picture")
    pdf = models.FileField(upload_to=pdf_name, null=True, blank=True, verbose_name='Upload PDF File')
    website = models.URLField(max_length=255,null=True, blank=True)  
    pdf_url  = models.URLField(max_length=255,null=True, blank=True)  
    paperback = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null = True)   
    size =  models.CharField(max_length=100, blank=True, null = True)
    create_date = models.DateTimeField(default=timezone.now)       
    
    def __unicode__(self):
        return u"{0}".format(self.title)

    def get_author_names(self):
        return ', '.join(a.name for a in self.author.all())
    
    @models.permalink
    def get_absolute_url(self):
        return ('account_material_edit', (), dict(material_id=self.id))


class GiverMaterial(models.Model):
    giver = models.ForeignKey(get_user_model())
    material = models.ForeignKey(Material)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="Good")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    create_date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('giver', 'material',)    

    def get_quantity_nums(self):
        return range(1, self.quantity + 1)
    
    def __unicode__(self):
        return "%s - %s " % (self.giver.get_profile().get_display_name() , self.material )


class Order(models.Model):
    reader = models.ForeignKey(get_user_model(), related_name = 'reader')
    giver = models.ForeignKey(get_user_model(), related_name = 'giver')
        
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price =   models.DecimalField(max_digits=8, decimal_places=2, default=0)   
    payment_detail = models.TextField(blank=True)    
    
    status =  models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default="NEW")     
    order_date = models.DateTimeField(default=timezone.now)
    ship_date = models.DateTimeField(null=True, blank=True)
    pay_date = models.DateTimeField(null=True, blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    
    def get_total_cost(self):
        return self.total_price + self.shipping_cost
    
    def get_paypal_cost(self):       
        return float ( self.shipping_cost ) * 1.029 + 0.3
    
    def __unicode__(self):
        return str(self.id)

class OrderDetail(models.Model):
    order     = models.ForeignKey(Order)
    inventory = models.ForeignKey(GiverMaterial)
    quantity = models.PositiveIntegerField(default=1)
    

