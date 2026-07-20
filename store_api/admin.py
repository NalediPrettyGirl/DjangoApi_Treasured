from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, ProductView, Order, Chat

admin.site.register(User, UserAdmin)
admin.site.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'status', 'price', 'createdAt')
    list_filter = ('status', 'createdAt')
    list_editable = ('status',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductView)
admin.site.register(Order)
admin.site.register(Chat)
