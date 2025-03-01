from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/products/', blank=True)
    comment = models.TextField(blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField()
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'product'
        verbose_name_plural = "products"

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    Phone_number = PhoneNumberField(region="UZ", null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    description = models.TextField()
    vat_number = models.IntegerField()
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'customer'
        verbose_name_plural = "customers"

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    image = models.ImageField(upload_to='media/products/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    @property
    def get_absolute_url(self):
        return self.image.url


class Attribute(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AttributeValue(BaseModel):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductAttribute(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True,
                                blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)
