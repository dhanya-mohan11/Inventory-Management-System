from django.db import models
from email.policy import default
from django.contrib.auth.models import User
from uuid import uuid4
import random
import string

# Create your models here.

# Users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username
       

# Vendors
class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Vendors'

    def __str__(self):
	    return self.name

    
# Units
class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, default="", verbose_name='Name')
    short_name = models.CharField(max_length=10, unique=True, default="", verbose_name='ShortName')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Units'

    def __str__(self):
	    return self.name
    

# Products
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, verbose_name='Name')
    description = models.TextField(blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
	    return self.name


# Unique key generation for billno
def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    if Purchase.objects.filter(billno=key).exists():
        key = key_generator()
    if Sale.objects.filter(billno=key).exists():
        key = key_generator()
    return key

# Purchases
class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    billno = models.CharField(max_length=6, default=key_generator, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False, default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Purchases'
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super(Purchase, self).save(*args, **kwargs)

        # Update inventory effect related to purchase
        inventory = Stock.objects.filter(
            product=self.product
            ).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_quantity + self.quantity
        else:
            totalBal = self.quantity

        # Insert in inventory 
        Stock.objects.create(
            product = self.product,
            vendor = self.vendor,
            purchase = self,
            sale = None,
            purchase_quantity = self.quantity,
            sale_quantity = None,
            total_balance_quantity = totalBal
        )
    
    def __str__(self):
	    return "INV" + str(self.billno)

#contains the details in the purchases bill
class PurchaseBill(models.Model):
    id = models.AutoField(primary_key=True)
    billno = models.ForeignKey(Purchase, on_delete = models.CASCADE, related_name='purchasebillno')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    purchase_date = models.ForeignKey(Purchase, on_delete = models.CASCADE)

    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
	    return "Bill no: " + str(self.billno)


# Sales
class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    billno = models.CharField(max_length=6, default=key_generator, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=10, unique=True)
    customer_address = models.TextField(blank=True)

    
    class Meta:
        verbose_name_plural = 'Sales'    
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super(Sale, self).save(*args, **kwargs)

        # Update inventory effect related to sale
        inventory = Stock.objects.filter(
            product=self.product
            ).order_by('-id').first()
        
        totalBal = 0
        if inventory:
            totalBal = inventory.total_balance_quantity - self.quantity

        # Insert in inventory 
        Stock.objects.create(
            product = self.product,
            purchase = None,
            sale = self,
            purchase_quantity = None,
            sale_quantity = self.quantity,
            total_balance_quantity = totalBal
        )
        
    def __str__(self):
	    return "INV" + str(self.billno)
    

#contains the details in the purchases bill
class SaleBill(models.Model):
    id = models.AutoField(primary_key=True)
    billno = models.ForeignKey(Sale, on_delete = models.CASCADE, related_name='salebillno')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer_name = models.ForeignKey(Sale, on_delete = models.CASCADE, related_name='customername')
    customer_phone = models.ForeignKey(Sale, on_delete = models.CASCADE, related_name='customerphone')
    sale_date = models.ForeignKey(Sale, on_delete = models.CASCADE)

    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


# Inventory
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=0, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    customer_name = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, related_name='customer')
    purchase_quantity = models.FloatField(default=0, null=True)
    sale_quantity = models.FloatField(default=0, null=True)
    #total_balance_quantity is expressed as: total_balance_quantity = purchase_quantity - sale_quantity
    total_balance_quantity = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Inventory'
    
    def product_unit(self):
        return self.product.unit.name

    def purchase_date(self):
        if self.purchase:
            return self.purchase.purchase_date

    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
        
    def __str__(self):
	    return str(self.product)