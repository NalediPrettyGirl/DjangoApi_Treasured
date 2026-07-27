from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_user, login_user, create_checkout, UserViewSet,
    CategoryViewSet, ProductViewSet, OrderViewSet, ChatViewSet,
    contact_message
)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('users/register', register_user, name='register'),
    path('users/login', login_user, name='login'),
    path('checkout/create', create_checkout, name='create_checkout'),
    path('contact', contact_message, name='contact'),
    # ViewSets
    path('', include(router.urls)),
]
