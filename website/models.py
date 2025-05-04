from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.timezone import now, timedelta
from uuid import uuid4

class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="provinces", null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.region.name}"

class Municipality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="municipalities", null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.province.name if self.province else 'No Province'}"

class Barangay(models.Model):
    name = models.CharField(max_length=255, unique=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="barangays", null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.municipality.name}"

class Company(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
        ('logistics', 'Logistics'),
    ]
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Variety(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='varieties', blank=True, null=True)
    description = models.CharField(max_length=255)  # e.g., "12 pcs, 155g each"
    quantity = models.PositiveIntegerField(default=0)  # Number of items in stock
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.description}"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_id = models.CharField(max_length=255, null=True, blank=True)
    claimed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='claimed_orders')  # New field
    claimed_at = models.DateTimeField(null=True, blank=True)  # Track when it was claimed
    is_archived = models.BooleanField(default=False)
    has_been_transferred = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Picked Up", "Picked Up"),  # Item-level tracking handled separately
            ("Shipped", "Shipped"),
            ("In Transit", "In Transit"),
            ("Arrived", "Arrived"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        default='Pending'
    )

    def needs_reassignment(self):
        """ Check if an order needs reassignment after 1 hour """
        return self.claimed_by is None or (self.claimed_at and now() - self.claimed_at > timedelta(hours=1))

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username if self.buyer else 'Unknown Buyer'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_picked_up = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.quantity} x {self.variety.description} ({self.product.name})"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.variety.price

    def __str__(self):
        return f"{self.quantity} x {self.variety.description} ({self.variety.product.name})"
        
class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.buyer.username}"

class Receipt(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='receipt', blank=True, null=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"RCPT-{uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_number} for Transaction {self.transaction.id}"

class TrackingLog(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Picked Up", "Picked Up"),
        ("Shipped", "Shipped"),
        ("In Transit", "In Transit"),
        ("Arrived", "Arrived"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_logs')
    logistics_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracking_logs')  
    status_update = models.CharField(max_length=50, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Order)
def update_transaction_on_order_status_change(sender, instance, **kwargs):
    """ Update the transaction record when the order status changes """
    print(f"Signal Triggered: Order {instance.id} status changed to {instance.status}")

    if instance.status in ['Delivered', 'Cancelled']:
        transaction = Transaction.objects.filter(order=instance).first()

        if transaction:
            transaction.total_price = instance.total_price  
            transaction.save()
            print(f"Transaction {transaction.id} updated for Order {instance.id}.")
        else:
            print(f"No transaction found for Order {instance.id}.")

