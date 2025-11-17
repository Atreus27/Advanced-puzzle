import yaml
import sys
import os

def update_values_file(env, app_version):
    # Get absolute path of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Correct path to values files
    values_file_path = os.path.join(script_dir, "charts", "application", "values", f"{env}.yaml")

    if not os.path.exists(values_file_path):
        print(f"❌ Error: {values_file_path} not found.")
        sys.exit(1)

    try:
        # Read YAML file
        with open(values_file_path, 'r') as file:
            values = yaml.safe_load(file) or {}

        # Update key
        values["appVersion"] = app_version

        # Create backup before changing it
        backup_path = values_file_path + ".bak"
        with open(backup_path, "w") as backup_file:
            yaml.dump(values, backup_file)

        # Write updated YAML
        with open(values_file_path, 'w') as file:
            yaml.dump(values, file, sort_keys=False, default_flow_style=False)

        print(f"✅ Updated {env}.yaml with appVersion: {app_version}")
        print(f"🗂  Backup created: {backup_path}")

    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update-values.py <environment> <app_version>")
        sys.exit(1)

    environment = sys.argv[1].lower()
    version = sys.argv[2]

    if environment not in ["dev", "prod"]:
        print("❌ Error: Environment must be 'dev' or 'prod'.")
        sys.exit(1)

    update_values_file(environment, version)
