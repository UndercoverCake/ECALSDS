from django.contrib import admin
from website.models import Profile, Category, Product, Variety, Company, Order, Transaction, Receipt, OrderItem, Cart, CartItem,TrackingLog, Region, Province, Municipality, Barangay
from .models import User

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variety)
admin.site.register(Company)
admin.site.register(Order)
admin.site.register(Receipt)
admin.site.register(Transaction)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(TrackingLog)
admin.site.register(Region)
admin.site.register(Municipality)
admin.site.register(Province)
admin.site.register(Barangay)
