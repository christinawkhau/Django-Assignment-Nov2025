from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = "Filter raw users data and save only selected fields"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        input_path = os.path.join(base_dir, "userprofiles.json")                                                    
        output_path = os.path.join(base_dir, "userprofiles_transformed.json")
        
        with open(input_path, "r") as f:
            users = json.load(f)

        filtered_users = []
        for item in users:
            filtered = {
                "user": item.get("id"),
                "phone_number": item.get("phone"),
                "address": item.get("address"),
                "company": item.get("company", {}).get("name", ""),
                "department" : item.get("company", {}).get("department", ""),
                "role": item.get("company", {}).get("title", ""),
            }
            filtered_users.append(filtered)

        with open(output_path, "w") as f:
            json.dump(filtered_users, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Filtered data saved to {output_path}"))
        
     