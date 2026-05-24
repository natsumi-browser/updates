import time
import json
import sys

# Read version data
try:
    with open('natsumi-browser/natsumi/version.json', 'r') as file:
        version_data = json.load(file)
except:
    print("Could not read Natsumi version file.")
    print("Maybe you didn't correctly git clone the repository?")
    raise

version = version_data['version']
branch = version_data['branch']

# Template data
template_data = {
    "version": version,
    "tag": f"v{version}",
    "releasedAt": round(time.time())
}

# Run version check
# If versions are identical, this check should fail
try:
    with open(f"{branch}.json", 'r') as file:
        existing_data = json.load(file)
except:
    print("No existing data found for this branch. Skipping version check.")
else:
    print(f"Current version: {existing_data.get('version', 'none')}")
    print(f"Incoming version: {version}")

    if existing_data.get("version") == version:
        print("Versions are identical, cannot publish.")
        sys.exit(1)

# Write new data
with open(f"{branch}.json", 'w+') as file:
    json.dump(template_data, file, indent=2)

print("Version bumped!")
print(json.dumps(template_data, indent=2))
