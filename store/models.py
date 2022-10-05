from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.template.defaultfilters import slugify

def upload_location_primary_image(instance, filename):
    """Used for naming uploaded primary product image automatically"""
    filebase, extension = filename.rsplit('.', maxsplit=1)
    return 'product-images/%s/primary-%s.%s' % (instance.slug, instance.slug, extension)

def upload_location_secondary_images(instance, filename):
    """Used for naming uploaded secondary product images automatically"""
    filebase, extension = filename.rsplit('.', maxsplit=1)
    return  'product-images/%s/secondary-%s.%s' % (
        instance.product.slug, instance.product.slug, extension)

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True, default=None, primary_key=True)
    
    def get_absolute_url(self):
        return reverse('categoria', kwargs={'slug': self.slug})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Product(models.Model): 
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=None, primary_key=True)
    price = MoneyField(
        max_digits=14, default_currency='ARS', default=0
    )
    discount_price = MoneyField(
        max_digits=14, default_currency='ARS', blank=True, null=True
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, 
        on_delete=models.SET_NULL, null=True, blank=True, default=None)
    color_or_version = models.CharField(max_length=200, blank=True, verbose_name='Color')
    TAGS = [
        ('s', 'Sale'),
        ('n', 'New'),
        ('l', 'Edición limitada'),
    ]
    tags = models.CharField(choices=TAGS, max_length=1, blank=True, null=True)
    MAX_IMAGES = 5
    primary_image = models.ImageField(blank=True,upload_to=upload_location_primary_image)

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detalle', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'slug' : self.slug,
        })

    def get_add_to_cart_from_product_list_url(self):
        return reverse('add_to_cart_from_product_list', kwargs={
            'slug' : self.slug,
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'slug' : self.slug,
        })

    class Meta:
        ordering = ['name' , 'price', 'discount_price']

class ProductImages(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = upload_location_secondary_images)

    def __str__(self) -> str:
        return self.product.name

    class Meta:
        verbose_name_plural = 'product images'
    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=64, null=True, blank=True)
    telephone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True,blank=True)
    started_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    final_price = MoneyField(
        max_digits=14, default_currency='ARS', default=0
    )

    def __str__(self):
        return f'{self.customer}\'s order'

class OrderProduct(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    selected_color = models.CharField(blank=True,max_length=50)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_decrease_url(self):
        return reverse('decrease', kwargs={
            'slug' : self.item.slug,
        })

    def get_increase_url(self):
        return reverse('increase', kwargs={
            'slug' : self.item.slug,
        })