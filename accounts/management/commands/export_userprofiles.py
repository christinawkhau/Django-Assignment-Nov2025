from django.core.management.base import BaseCommand
import json
import os
from accounts.models import Userprofile

class Command(BaseCommand):
    help = "Export all user profiles from the database to a JSON file"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "userprofiles_exported.json")

        profiles = Userprofile.objects.select_related("user").all()
        data = []

        for profile in profiles:
            # Normalize address
            addr = profile.address
            if isinstance(addr, dict):
                full_address = f"{addr.get('address', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('postalCode', '')} ({addr.get('stateCode', '')})"
            else:
                full_address = str(addr)

            item = {
                "user": profile.user.id,
                "phone_number": profile.phone_number,
                "address": full_address,
                "company": profile.company,
                "department": profile.department,
                "role": profile.role,
            }
            data.append(item)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {len(data)} user profiles to {output_path}"))
