from django.core.management.base import BaseCommand
import requests
import json
import os

class Command(BaseCommand):
    help = "Download cart data from DummyJSON and save to cart.json"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "cart.json")

        response = requests.get("https://dummyjson.com/carts")
        data = response.json()["carts"]

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ File saved successfully at {file_path}"))
