from django.db import models


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='menuitem_images')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField(to='category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    items = models.ManyToManyField(to='MenuItem', related_name='order', blank=True)
    first_name = models.CharField(max_length=30, default='')
    second_name = models.CharField(max_length=30, default='')
    email = models.EmailField(max_length=30, default='')
    county = models.CharField(max_length=30, default='')
    sub_county = models.CharField(max_length=30, default='')
    area = models.CharField(max_length=30, default='')
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'order: {self.created_on.strftime("%b %d %I %M %p")}'
