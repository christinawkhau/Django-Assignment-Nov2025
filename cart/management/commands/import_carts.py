from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from cart.models import CartItem
from products.models import Product
import json
import os

class Command(BaseCommand):
    help = "Import cart items with user, product name, and quantity"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "carts_transformed.json")
        output_path = os.path.join(base_dir, "carts_imported.json")

        # 🧼 Clean existing cart items before import
        CartItem.objects.all().delete()

        try:
            with open(file_path, "r") as f:
                entries = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
            return

        created = []
        skipped_users = 0
        skipped_products = 0
        skipped_quantity = 0

        for item in entries:
            try:
                user = User.objects.get(id=item["user"])
            except User.DoesNotExist:
                skipped_users += 1
                continue

            try:
                product = Product.objects.get(name=item["product"])
            except Product.DoesNotExist:
                skipped_products += 1
                continue

            quantity = item.get("quantity", 1)
            if not isinstance(quantity, int) or quantity < 1:
                skipped_quantity += 1
                continue

            CartItem.objects.create(user=user, product=product, quantity=quantity)
            created.append({
                "user": user.id,
                "product": product.name,
                "quantity": quantity
            })

        with open(output_path, "w") as f:
            json.dump(created, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(created)} cart items successfully."))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped_users} users, {skipped_products} products, {skipped_quantity} invalid quantities."))




# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand
# from cart.models import CartItem
# from products.models import Product
# import json
# import os

# class Command(BaseCommand):
#     help = "Import cart items with user, product name, and quantity"

#     def handle(self, *args, **kwargs):
#         base_dir = os.path.dirname(__file__)
#         file_path = os.path.join(base_dir, "carts_transformed.json")
#         output_path = os.path.join(base_dir, "carts_imported.json")

#         try:
#             with open(file_path, "r") as f:
#                 entries = json.load(f)
#         except FileNotFoundError:
#             self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
#             return
#         except json.JSONDecodeError:
#             self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
#             return

#         created = []
#         skipped_users = 0
#         skipped_products = 0
#         skipped_quantity = 0

#         for item in entries:
#             try:
#                 user = User.objects.get(id=item["user"])
#             except User.DoesNotExist:
#                 skipped_users += 1
#                 continue

#             try:
#                 product = Product.objects.get(name=item["product"])
#             except Product.DoesNotExist:
#                 skipped_products += 1
#                 continue

#             quantity = item.get("quantity", 1)
#             if not isinstance(quantity, int) or quantity < 1:
#                 skipped_quantity += 1
#                 continue

#             CartItem.objects.create(user=user, product=product, quantity=quantity)
#             created.append({
#                 "user": user.id,
#                 "product": product.name,
#                 "quantity": quantity
#             })

#         with open(output_path, "w") as f:
#             json.dump(created, f, indent=2)

#         self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(created)} cart items successfully."))
#         self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped_users} users, {skipped_products} products, {skipped_quantity} invalid quantities."))





# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand
# from cart.models import CartItem
# from products.models import Product
# import json
# import os

# class Command(BaseCommand):
#     help = "Import cart items with user, product name, and quantity"

#     def handle(self, *args, **kwargs):
#         base_dir = os.path.dirname(__file__)
#         file_path = os.path.join(base_dir, "carts_transformed.json")

#         try:
#             with open(file_path, "r") as f:
#                 entries = json.load(f)
#         except FileNotFoundError:
#             self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
#             return
#         except json.JSONDecodeError:
#             self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
#             return

#         created_count = 0
#         skipped_users = 0
#         skipped_products = 0

#         for item in entries:
#             try:
#                 user = User.objects.get(id=item["user"])
#             except User.DoesNotExist:
#                 self.stderr.write(self.style.WARNING(f"⚠️ Skipped: User ID {item['user']} not found."))
#                 skipped_users += 1
#                 continue

#             try:
#                 product = Product.objects.get(name=item["product"])
#             except Product.DoesNotExist:
#                 self.stderr.write(self.style.WARNING(f"⚠️ Skipped: Product '{item['product']}' not found."))
#                 skipped_products += 1
#                 continue

#             quantity = item.get("quantity", 1)
#             if not isinstance(quantity, int) or quantity < 1:
#                 self.stderr.write(self.style.WARNING(f"⚠️ Skipped: Invalid quantity for user {item['user']} and product '{item['product']}'"))
#                 continue

#             CartItem.objects.create(user=user, product=product, quantity=quantity)
#             created_count += 1

#         self.stdout.write(self.style.SUCCESS(f"✅ Imported {created_count} cart items successfully."))
#         self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped_users} users, {skipped_products} products."))
