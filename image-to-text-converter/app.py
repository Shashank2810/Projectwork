from flask import Flask, render_template, request, redirect, url_for
from skimage.metrics import structural_similarity
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)

def compare_images(original_path, tampered_path):
    # Load images
    original = Image.open(original_path)
    tampered = Image.open(tampered_path)

    # Convert images to numpy arrays
    original_array = np.array(original)
    tampered_array = np.array(tampered)

    # Convert images to grayscale
    original_gray = cv2.cvtColor(original_array, cv2.COLOR_RGB2GRAY)
    tampered_gray = cv2.cvtColor(tampered_array, cv2.COLOR_RGB2GRAY)

    # Compute Structural Similarity Index (SSIM) between the images
    (score, _) = structural_similarity(original_gray, tampered_gray, full=True)

    # Define a threshold for SSIM score to detect tampering
    threshold = 0.9  # You can adjust this threshold based on your needs

    # Determine if the image is tampered based on SSIM score
    if score < threshold:
        return "Tampered"
    else:
        return "Not Tampered"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file uploads
        original_file = request.files['original']
        tampered_file = request.files['tampered']

        # Save uploaded files
        uploads_dir = 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        original_path = os.path.join(uploads_dir, 'original.png')
        tampered_path = os.path.join(uploads_dir, 'tampered.png')

        original_file.save(original_path)
        tampered_file.save(tampered_path)

        # Compare images
        result = compare_images(original_path, tampered_path)

        # Delete uploaded files after comparison
        os.remove(original_path)
        os.remove(tampered_path)

        return render_template('result.html', result=result)

    return render_template('index.html')

@app.route('/refresh', methods=['GET'])
def refresh():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
