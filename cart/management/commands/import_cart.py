from django.core.management.base import BaseCommand
import json
import os
from products.models import Product, Category  # Adjust if Category is in another app

class Command(BaseCommand):
    help = "Clear existing products and import filtered products from JSON"

    def handle(self, *args, **kwargs):
        # Locate the JSON file relative to this script
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "products_filtered.json")

        # Load the filtered product data
        try:
            with open(file_path, "r") as f:
                carts = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
            return

        # Clear existing products
        Cart.objects.all().delete()
        self.stdout.write(self.style.WARNING("⚠️ All existing products have been deleted."))

        # Import each product
        created_count = 0
        for item in carts:
            try:

                Cart.objects.create(
                    user = models.ForeignKey(User, on_delete=models.CASCADE)
                    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
                    #product_image = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
                    quantity = models.PositiveIntegerField(default=1)
                    added_at = models.DateTimeField(auto_now_add=True)
                    
                    
                    
                    
                    sku=item.get("sku"),
                    description=item.get("description"),
                    price=item.get("price"),
                    stock=item.get("stock"),
                    category=category_obj,
                    brand=brand_value
                )
                created_count += 1
            except Exception as e:
                self.stderr.write(self.style.WARNING(f"⚠️ Skipped product due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {created_count} products successfully."))
