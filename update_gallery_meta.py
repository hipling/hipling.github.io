import os
import json

EVENTS_DIR = "assets/events"
META_FILE = "gallery_meta.json"
SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.webp')

# Load existing meta if available
if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}

# Track updates
updated = False

# Traverse the event directory
for entry in sorted(os.listdir(EVENTS_DIR)):
    full_path = os.path.join(EVENTS_DIR, entry)

    # Case 1: Directory — multi-image event
    if os.path.isdir(full_path):
        images = [
            os.path.join(EVENTS_DIR, entry, f)
            for f in sorted(os.listdir(full_path))
            if f.lower().endswith(SUPPORTED_EXTS)
        ]
        if not images:
            continue

        if entry not in meta:
            meta[entry] = {
                "title": entry.replace("-", " ").title(),
                "date": "",
                "desc": "",
                "images": images
            }
            updated = True
        else:
            # Always update image list to reflect changes
            meta[entry]["images"] = images

    # Case 2: File — single-image event
    elif entry.lower().endswith(SUPPORTED_EXTS):
        key = entry
        image_path = os.path.join(EVENTS_DIR, entry)

        if key not in meta:
            meta[key] = {
                "title": os.path.splitext(entry)[0].replace("-", " ").title(),
                "date": "",
                "desc": "",
                "images": [image_path]
            }
            updated = True
        else:
            # Ensure image is present in the list
            meta[key]["images"] = [image_path]

# Save back to JSON if anything changed
if updated:
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("✅ Metadata updated and saved to gallery_meta.json")
else:
    print("✅ No new entries. Metadata already up-to-date.")
