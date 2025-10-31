from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = "Filter raw product data and save only selected fields"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        input_path = os.path.join(base_dir, "cart.json")
        output_path = os.path.join(base_dir, "cart_filtered.json")

        with open(input_path, "r") as f:
            carts = json.load(f)

        filtered_cart = []
        for item in carts:
            filtered = {
                "user": item.get("user"),
                "product": item.get("product"),
                "quantity": item.get("quantity"),
                "added_at": item.get("added_at"),
            }
            filtered_cart.append(filtered)

        with open(output_path, "w") as f:
            json.dump(filtered_cart, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Filtered data saved to {output_path}"))
