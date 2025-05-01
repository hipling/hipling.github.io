# build_site.py

TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"
GALLERY_FILE = "gallery.html"
PROJECTS_FILE = "projects.html"

PLACEHOLDERS = {
    "<!-- GALLERY_PLACEHOLDER -->": GALLERY_FILE,
    "<!-- PROJECTS_PLACEHOLDER -->": PROJECTS_FILE
}

# Load template
try:
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        html = f.read()
except FileNotFoundError:
    print(f"❌ Cannot find {TEMPLATE_FILE}")
    exit(1)

# Replace each placeholder
for placeholder, filename in PLACEHOLDERS.items():
    try:
        with open(filename, "r", encoding="utf-8") as f:
            replacement = f.read()
    except FileNotFoundError:
        print(f"⚠️ Warning: {filename} not found. Skipping replacement for {placeholder}.")
        continue

    if placeholder not in html:
        print(f"⚠️ Warning: Placeholder {placeholder} not found in template.")
    else:
        html = html.replace(placeholder, replacement)

# Write final merged HTML
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Site built successfully to {OUTPUT_FILE}")
