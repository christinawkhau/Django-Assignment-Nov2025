import subprocess
import sys
import json
import os

def run_command(command):
    """Run a Django management command."""
    full_command = f"python manage.py {command}"
    print(f"\n🔄 Running: {full_command}\n")
    result = subprocess.run(full_command, shell=True)
    if result.returncode == 0:
        print("✅ Command executed successfully.\n")
    else:
        print("❌ Command failed. Check your command or logs.\n")

def show_data_volume(app, action):
    """Display the number of records in the output JSON file."""
    filename_map = {
        "download": f"{app}_download.json",
        "transform": f"{app}_transformed.json",
        "import": f"{app}_imported.json",
        "export": f"{app}_exported.json"
    }

    filename = filename_map.get(action)
    if not filename or not os.path.exists(filename):
        print(f"📁 No data file found for {action}. Skipping volume check.\n")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            count = len(data) if isinstance(data, list) else len(data.get("results", []))
            print(f"📊 {action.capitalize()} completed: {count} records processed.\n")
    except Exception as e:
        print(f"⚠️ Could not read {filename}: {e}\n")

def choose_data_type():
    print("\n📦 What type of data would you like to process?")
    print("1. UserProfiles")
    print("2. Products")
    print("3. Carts")
    data_choice = input("Enter choice (1-3): ").strip()

    data_map = {
        "1": "userprofiles",
        "2": "products",
        "3": "carts"
    }

    if data_choice not in data_map:
        print("❌ Invalid choice. Exiting.")
        sys.exit(1)

    return data_map[data_choice]

def process_pipeline(app):
    for action in ["download", "transform", "import", "export"]:
        command_name = f"{action}_{app}"
        run_command(command_name)
        show_data_volume(app, action)

def main():
    print("🧠 Welcome to the Django DB Tool")
    print("────────────────────────────────")
    app = choose_data_type()
    process_pipeline(app)
    print("\n✅ All steps completed.")

if __name__ == "__main__":
    main()
