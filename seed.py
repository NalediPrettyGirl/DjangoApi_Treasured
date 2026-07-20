import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store_api.models import User, Category, Product

# Clear existing products to avoid duplicates
Product.objects.all().delete()

# Ensure we have our test user
user, _ = User.objects.get_or_create(username="testuser", email="test@example.com")
if _:
    user.set_password("password123")
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
    {
        "title": "Stunning Traditional Makoti Dress",
        "price": 3200.00,
        "category": "traditional-wedding",
        "imageUrl": "images/categories/traditional_dresses.png",
        "description": "Beautiful cultural garment perfect for lobola celebrations and traditional ceremonies. Includes headwrap."
    },
    {
        "title": "Classic Black Tuxedo Set",
        "price": 1500.00,
        "category": "tuxedos",
        "imageUrl": "images/categories/mens_formal.png",
        "description": "Premium quality black tuxedo. Includes jacket and trousers. Perfect for weddings and formal events."
    },
    {
        "title": "Men's Tailored Traditional Attire",
        "price": 2100.00,
        "category": "traditional-attire",
        "imageUrl": "images/categories/mens_traditional.png",
        "description": "Custom-tailored men's traditional suit with intricate embroidery. Excellent condition."
    },
    {
        "title": "Elegant Evening Matric Dance Dress",
        "price": 4500.00,
        "category": "evening",
        "imageUrl": "images/categories/matric_dance.png",
        "description": "Show-stopping evening dress perfect for a matric dance or gala. Features subtle sequins and a sweeping train."
    }
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
