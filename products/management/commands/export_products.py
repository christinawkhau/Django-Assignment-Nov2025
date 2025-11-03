from django.core.management.base import BaseCommand
import json
import os
from decimal import Decimal
from products.models import Product

class Command(BaseCommand):
    help = "Export all products from the database to a JSON file"

    def handle(self, *args, **kwargs):
        # Define output path relative to this script
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "products_exported.json")

        # Fetch all products
        products = Product.objects.select_related("category").all()

        # Prepare data for export
        data = []
        for product in products:
            item = {
                "sku": product.sku,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),  # Convert Decimal to float
                "stock": product.stock,
                "category": product.category.name if product.category else None,
                "brand": product.brand
            }
            data.append(item)

        # Write to JSON file
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {len(data)} products to {output_path}"))
