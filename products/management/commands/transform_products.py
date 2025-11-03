from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = "Filter raw product data and save only selected fields"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        input_path = os.path.join(base_dir, "products.json")
        output_path = os.path.join(base_dir, "products_transformed.json")

        with open(input_path, "r") as f:
            products = json.load(f)

        filtered_products = []
        for item in products:
            filtered = {
                "sku": item.get("sku"),
                "name": item.get("title"),
                "description": item.get("description"),
                "price": item.get("price"),
                "stock": item.get("stock"),
                "category": item.get("category"),
                "brand": item.get("brand")
            }
            filtered_products.append(filtered)

        with open(output_path, "w") as f:
            json.dump(filtered_products, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Filtered data saved to {output_path}"))
        
     