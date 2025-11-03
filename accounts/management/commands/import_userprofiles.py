from django.contrib.auth.models import User
from accounts.models import Userprofile
from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = "Import all user profiles and link to existing Django users"

    def handle(self, *args, **kwargs):
        # Locate the JSON file relative to this script
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "userprofiles_transformed.json")

        # Load JSON data
        try:
            with open(file_path, "r") as f:
                profiles = json.load(f)  # ← no slicing here
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
            return

        # Import each profile
        created_count = 0
        for item in profiles:
            try:
                user = User.objects.get(id=item["user"])
                addr = item.get("address", {})
                full_address = f"{addr.get('address', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('postalCode', '')} ({addr.get('stateCode', '')})"

                Userprofile.objects.update_or_create(
                    user=user,
                    defaults={
                        "phone_number": item.get("phone_number", ""),
                        "address": full_address,
                        "company": item.get("company", ""),
                        "department": item.get("department", ""),
                        "role": item.get("role", "")
                    }
                )
                created_count += 1
            except User.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"⚠️ Skipped profile: User ID {item['user']} not found."))
            except Exception as e:
                self.stderr.write(self.style.WARNING(f"⚠️ Skipped profile due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {created_count} user profiles successfully."))

