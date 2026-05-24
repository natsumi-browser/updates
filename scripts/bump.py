import time
import json
import sys
import os
import hashlib

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

# Get archive hash
exit_code = os.system(f"wget -O natsumi-browser/archive.zip https://github.com/greeeen-dev/natsumi-browser/archive/refs/tags/v{version}.zip")
if exit_code != 0:
    print("Failed to download archive.")
    sys.exit(1)

with open("natsumi-browser/archive.zip", "rb") as file:
    sha256 = hashlib.sha256()
    sha256.update(file.read())

# Template data
template_data = {
    "version": version,
    "tag": f"v{version}",
    "hash": sha256.hexdigest(),
    "releasedAt": round(time.time())
}

# Write new data
with open(f"{branch}.json", 'w+') as file:
    json.dump(template_data, file, indent=2)

print("Version bumped!")
print(json.dumps(template_data, indent=2))
