import uuid
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, editable=False)
    reference = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    min_quantity = models.IntegerField()
    low_quantity = models.IntegerField()
    current_quantity = models.IntegerField(default=0)
    inventory_tracking = models.BooleanField(default=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = (
        ('K', 'KILOGRAM'),
        ('L', 'LITRE'),
        ('SET', 'SET'),
    )
    product_type = models.CharField(max_length=3, choices=type_choices)

    # Override the save method to generate a unique SKU SKu is a mix of the first 3 letters of the product name and 3 numbers derived from the reference and 4 numbers derived from 
    def save(self, *args, **kwargs):
        self.sku = self.name[:4].upper() + str(self.reference)[:4] + str(self.product_type)[:1] + str(self.product_type)[:1]
        super().save(*args, **kwargs)
        print(self.sku)
    
    def __str__(self):
        return self.name    


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    products = models.ManyToManyField(Product, through='OrderProduct')
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_fulfilled = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_choices = (
        ('P', 'PENDING'),
        ('F', 'FULFILLED'),
        ('C', 'CANCELLED'),
    )
    status = models.CharField(max_length=1, choices=status_choices, default='P')
    supplier = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    # Override the save method to generate to calculate the total price of the order
    def save(self, *args, **kwargs):
        self.total_price = self.products.aggregate(models.Sum('unit_price'))['unit_price__sum']
        super().save(*args, **kwargs)

    # Override the save method to generate a unique order number
    def save(self, *args, **kwargs):
        self.order_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price_product = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class DeliveryOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_order_number = models.CharField(max_length=50, unique=True)
    date_delivered = models.DateTimeField(null=True, blank=True)

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    driving_license = models.CharField(max_length=50)

class Reparation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ReparationProduct')
    date_repaired = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    odometer = models.IntegerField()
    driver_name = models.CharField(max_length=100)

class ReparationProduct(models.Model):
    reparation = models.ForeignKey(Reparation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price_product = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price_product = self.product.unit_price * self.quantity
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.reparation.save()

    class Meta:
        unique_together = ('reparation', 'product')



