from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = "Filter raw cart data and save only selected fields"

    def handle(self, *args, **kwargs):
        # Locate input and output files
        base_dir = os.path.dirname(__file__)
        input_path = os.path.join(base_dir, "carts.json")
        output_path = os.path.join(base_dir, "carts_transformed.json")

        # Load raw cart data
        try:
            with open(input_path, "r") as f:
                carts = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {input_path}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
            return

        # Filter and flatten cart data
        filtered_carts = []
        for cart in carts:
            user_id = cart.get("id")
            for product in cart.get("products", []):
                filtered = {
                    "user": user_id,
                    "product": product.get("title", ""),
                    "quantity": product.get("quantity", 0)
                }
                filtered_carts.append(filtered)

        # Save filtered data
        with open(output_path, "w") as f:
            json.dump(filtered_carts, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Saved {len(filtered_carts)} filtered cart items to {output_path}"))













