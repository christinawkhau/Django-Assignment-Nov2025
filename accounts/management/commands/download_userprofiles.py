from django.core.management.base import BaseCommand
import requests
import json
import os

class Command(BaseCommand):
    help = "Download user data from DummyJSON and save to userprofiles.json"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "userprofiles.json")

        response = requests.get("https://dummyjson.com/users")
        data = response.json()["users"]

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ File saved successfully at {file_path}"))
