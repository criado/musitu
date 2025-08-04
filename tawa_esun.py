from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

# Settings
output_pdf = "esun/output.pdf"
input_folder = "pini"
output_folder = "esun"
os.makedirs(output_folder, exist_ok=True)

page_width, page_height = A4
margin = 50
columns = 2
rows = 3
images_per_page = columns * rows
spacing_x = (page_width - 2 * margin) / columns
spacing_y = (page_height - 2 * margin) / rows
image_size = min(spacing_x, spacing_y)  # leave small padding

# Get list of image files
images = [f"{input_folder}/lipu-{i}.png" for i in range(133)]  # 0 to 132

# Create PDF
c = canvas.Canvas(output_pdf, pagesize=A4)

for i, path in enumerate(images):
    col = i % columns
    row = (i // columns) % rows
    page = i // images_per_page

    if i % images_per_page == 0 and i != 0:
        c.showPage()  # new page

    x = margin + col * spacing_x + (spacing_x - image_size) / 2
    y = page_height - margin - (row + 1) * spacing_y + (spacing_y - image_size) / 2

    c.drawImage(path, x, y, width=image_size, height=image_size)

c.save()
