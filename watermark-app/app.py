import os
from flask import Flask, request, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'watermarked'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get uploaded files
    image_file = request.files['image']
    logo_file = request.files['logo']

    if image_file and logo_file:
        # Save uploaded files
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        logo_path = os.path.join(UPLOAD_FOLDER, logo_file.filename)
        image_file.save(image_path)
        logo_file.save(logo_path)

        # Process image to add watermark
        add_watermark(image_path, logo_path)

        # Generate path to watermarked image
        watermarked_filename = f'watermarked_{image_file.filename}'
        watermarked_path = os.path.join(OUTPUT_FOLDER, watermarked_filename)

        return send_from_directory(OUTPUT_FOLDER, watermarked_filename, as_attachment=True)

    return 'Error: Please upload both image and logo files.'

def add_watermark(image_path, logo_path):
    # Load image and logo
    image = Image.open(image_path).convert('RGBA')
    logo = Image.open(logo_path).convert('RGBA')

    # Resize logo (increase size by 50 times)
    logo_width, logo_height = logo.size
    new_logo_size = (logo_width * 50, logo_height * 10)
    resized_logo = logo.resize(new_logo_size)

    # Calculate watermark position (bottom right corner with margin)
    image_width, image_height = image.size
    margin = 10
    watermark_position = (image_width - new_logo_size[0] - margin, image_height - new_logo_size[1] - margin)

    # Add watermark to the image
    watermarked_image = image.copy()
    watermarked_image.paste(resized_logo, watermark_position, resized_logo)

    # Save watermarked image
    watermarked_image_path = os.path.join(OUTPUT_FOLDER, f'watermarked_{os.path.basename(image_path)}')
    watermarked_image.convert('RGB').save(watermarked_image_path)

if __name__ == '__main__':
    app.run(debug=True)
