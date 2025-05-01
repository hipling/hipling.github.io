import json
import datetime

META_FILE = "gallery_meta.json"
OUTPUT_HTML = "gallery.html"

def parse_date(date_str):
    """Try to parse the date string; fallback to very old date."""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except:
            continue
    return datetime.datetime(1900, 1, 1)  # fallback for missing/invalid

# Load metadata
with open(META_FILE, "r", encoding="utf-8") as f:
    meta = json.load(f)

# Prepare sorted entries with type flag (0 = folder, 1 = file)
entries = []
for key, entry in meta.items():
    if not entry.get("images") or entry.get("generate", True) is False:
        continue

    date_str = entry.get("date", "")
    parsed_date = parse_date(date_str)
    is_file = '.' in key  # file = single image

    entries.append((is_file, parsed_date, key, entry))

# Sort: folder (is_file=False) before file (is_file=True), then by date descending
entries.sort(key=lambda x: (x[0], -x[1].timestamp()))

# Generate HTML
html_output = ""
for is_file, _, key, entry in entries:
    images = entry["images"]
    title = entry.get("title", key)
    date = entry.get("date", "")
    desc = entry.get("desc", "")
    preview = images[0]

    if not is_file:  # folder: multi-image popup
        popup_images = ", ".join(f"'{img}'" for img in images)
        html_output += f"""
<div class="gallery-card" onclick="openPopup([{popup_images}], '{title}')">
  <img src="{preview}" alt="{title}" class="gallery-image">
  <div class="gallery-overlay">
    <div class="gallery-text">
      <h3 class="gallery-title">{title}</h3>
      <p class="gallery-date">{date}</p>
      <p class="gallery-desc">{desc}</p>
      <p class="text-xs italic mt-1 opacity-80">Click to view more →</p> 
    </div>
  </div>
</div>
"""
    else:  # file: standalone image
        html_output += f"""
<div class="gallery-card">
  <img src="{preview}" alt="{title}" class="gallery-image">
  <div class="gallery-overlay">
    <div class="gallery-text">
      <h3 class="gallery-title">{title}</h3>
      <p class="gallery-date">{date}</p>
      <p class="gallery-desc">{desc}</p>
    </div>
  </div>
</div>
"""

# Save to file
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ gallery.html generated: folders first, then single images — all sorted by date.")
