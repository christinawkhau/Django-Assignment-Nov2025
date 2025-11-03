from django.core.management.base import BaseCommand
from cart.models import CartItem
import json
import os

class Command(BaseCommand):
    help = "Export all cart items from the database to a JSON file"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "carts_exported.json")

        cart_items = CartItem.objects.select_related("user", "product").all()
        data = []
        skipped = 0

        for item in cart_items:
            if not item.user or not item.product:
                skipped += 1
                continue

            data.append({
                "user": item.user.id,
                "product": item.product.name,
                "quantity": item.quantity
            })

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {len(data)} cart items to {output_path}"))
        if skipped:
            self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped} cart items due to missing user or product."))




# from django.core.management.base import BaseCommand
# from cart.models import CartItem
# import json
# import os

# class Command(BaseCommand):
#     help = "Export all cart items from the database to a JSON file"

#     def handle(self, *args, **kwargs):
#         base_dir = os.path.dirname(__file__)
#         output_path = os.path.join(base_dir, "carts_exported.json")

#         cart_items = CartItem.objects.select_related("user", "product").all()
#         data = []
#         skipped = 0

#         for item in cart_items:
#             if not item.user or not item.product:
#                 self.stderr.write(self.style.WARNING("⚠️ Skipped cart item with missing user or product."))
#                 skipped += 1
#                 continue

#             entry = {
#                 "user": item.user.id,
#                 "product": item.product.name,
#                 "quantity": item.quantity,
#             }
#             data.append(entry)

#         with open(output_path, "w") as f:
#             json.dump(data, f, indent=4)

#         self.stdout.write(self.style.SUCCESS(f"✅ Exported {len(data)} cart items to {output_path}"))
#         if skipped:
#             self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped} cart items due to missing user or product."))
