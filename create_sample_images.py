#!/usr/bin/env python3
"""Generate 10 simple placeholder images for testing."""
from PIL import Image, ImageDraw
import os

os.makedirs("sample_images", exist_ok=True)

images = [
    ("photo01.jpg", "Photo 1",  "#4A90D9"),
    ("photo02.jpg", "Photo 2",  "#7B68EE"),
    ("photo03.jpg", "Photo 3",  "#5BA85A"),
    ("photo04.jpg", "Photo 4",  "#E8A838"),
    ("photo05.jpg", "Photo 5",  "#D9534F"),
    ("photo06.jpg", "Photo 6",  "#5BC0DE"),
    ("photo07.jpg", "Photo 7",  "#9B59B6"),
    ("photo08.jpg", "Photo 8",  "#1ABC9C"),
    ("photo09.jpg", "Photo 9",  "#E67E22"),
    ("photo10.jpg", "Photo 10", "#2C3E50"),
]

for filename, label, color in images:
    img = Image.new("RGB", (1920, 1080), color=color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([660, 340, 1260, 740], fill="white")
    draw.text((960, 540), label, fill=color, anchor="mm")
    draw.text((960, 80), "FotoOwl AI Sample", fill="white", anchor="mm")
    img.save(os.path.join("sample_images", filename), "JPEG", quality=85)
    print(f"  ✓ {filename}")

print(f"\nCreated {len(images)} images in sample_images/")
