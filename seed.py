import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store_api.models import User, Category, Product

# Clear existing products to avoid duplicates
Product.objects.all().delete()

# Ensure we have our test user (Busi)
user, _ = User.objects.get_or_create(username="bus1s1w3", email="makhubedubusi@gmail.com")
user.first_name = "Busi"
user.last_name = "Makhubedu"
user.whatsapp = "+27643619533"
user.set_password("bus1s1w3")
user.is_staff = True
user.is_superuser = True
user.save()

# Create products with real images from your frontend folder
products_data = [
    {
        "title": "Romantic Crystal-Beaded Bridal Gown",
        "price": 8500.00,
        "category": "white-wedding",
        "imageUrl": "images/categories/wedding_dresses.png",
        "description": "Fit-and-flare gown with illusion neckline and shear back. Worn once, professionally dry cleaned."
    },
]

for p_data in products_data:
    # Ensure category exists
    cat, _ = Category.objects.get_or_create(name=p_data['category'])
    
    # Create product
    Product.objects.create(
        title=p_data['title'],
        price=p_data['price'],
        category=cat.name,
        seller=user,
        imageUrl=p_data['imageUrl'],
        description=p_data['description']
    )

print(f"Successfully seeded {len(products_data)} realistic products into the database!")
