from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, ProductView, Order, Chat

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'status', 'createdAt')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'seller__username')
    list_editable = ('status',)

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductView)
admin.site.register(Order)
admin.site.register(Chat)
