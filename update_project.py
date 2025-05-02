import json
import os

PROJECTS_FILE = "projects.json"
OUTPUT_FILE = "projects.html"
SUPPORTED_EXTS = (".jpg", ".jpeg", ".png", ".webp")

def get_images_from_folder(folder_path):
    if not os.path.isdir(folder_path):
        return []
    return [
        os.path.join(folder_path, f).replace("\\", "/")
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(SUPPORTED_EXTS)
    ]

with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
    projects = json.load(f)

html_output = ""

for project in projects:
    title = project["title"]
    role = project["role"]
    duration = project["duration"]
    bullets = project["bullets"]
    folder = project["image_folder"]
    link = project.get("link", "").strip()

    images = get_images_from_folder(folder)
    if not images:
        print(f"⚠️ Warning: No images found in {folder}")
        continue

    bullet_html = "\n".join(f"<li>{b}</li>" for b in bullets)
    image_list = ", ".join(f"'{img}'" for img in images)

    link_html = f"""<a href="{link}" target="_blank" title="External link" class="ml-2 text-blue-500 hover:underline text-sm inline-flex items-center">
        🔗
    </a>""" if link else ""

    html_output += f"""
<div class="project-card bg-rose-50 p-6 rounded-xl cursor-pointer" onclick="openPopup([{image_list}], '{title}')">
  <div class="flex flex-col md:flex-row md:justify-between md:items-start">
    <div>
      <h3 class="font-bold text-lg flex items-center">{title}{link_html}</h3>
      <p class="text-sm text-gray-600 italic">{role}</p>
      <ul class="list-disc ml-5 mt-2 text-sm text-gray-700">
        {bullet_html}
      </ul>
      <p class="text-xs italic mt-2 text-rose-600">Click to view more →</p>
    </div>
    <div class="text-gray-600 font-semibold mt-2 md:mt-0">
      {duration}
    </div>
  </div>
</div>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ {OUTPUT_FILE} generated with {len(projects)} interactive project cards.")
