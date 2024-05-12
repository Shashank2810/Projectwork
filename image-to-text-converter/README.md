**Image Comparison Web Application**

This is a simple Flask web application that allows users to upload two images and compare them to detect tampering using Structural Similarity Index (SSIM).

**Application Overview**

The application consists of two main parts:

1. **Frontend (HTML and CSS)**:
   
The frontend allows users to upload two image files (an original image and a potentially tampered image).

When the user clicks the "Compare" button, the images are processed on the server to compute the SSIM score and determine if the second image is tampered.

2. **Backend (Flask and OpenCV)**:
   
The backend is built using Flask, a lightweight Python web framework.

Image processing and comparison are performed using OpenCV and scikit-image libraries.


**Prerequisites**

Python (3.x recommended) installed on your system.

Pip (Python package manager) installed.

**Installation**

Clone or download this repository to your local machine.

Navigate to the project directory using the command line

cd flask-image-comparison

pip install -r requirements.txt

**Running the Application**

python app.py

Open a web browser and navigate to http://localhost:5000 to access the application.Port number can be modified

**Usage**

1. Upload an original image file and a potentially tampered image file using the file input fields on the web page.

2. Click the "Compare" button to submit the uploaded images to the server for processing.

3. The server will compute the Structural Similarity Index (SSIM) between the images and determine if the second image is tampered based on a predefined threshold.

4. The result (either "Tampered" or "Not Tampered") will be displayed on the web page.

5. Click the "Refresh" button to upload new images and perform another comparison.


**Code Breakdown**

**Image Upload**:

* When a user uploads two images (an original and a potentially tampered one) through the Flask web interface, these images are saved temporarily on the server.


**Image Comparison Function (compare_images)**:

* This function takes two file paths corresponding to the uploaded images: original_path and tampered_path.

* It reads both images using PIL (Pillow) and converts them into numpy arrays (original_array and tampered_array).

* The images are then converted to grayscale using cv2.cvtColor.

* The Structural Similarity Index (SSIM) is calculated between the grayscale versions of the two images using skimage.metrics.structural_similarity.
* SSIM is a metric that measures the similarity between two images. It takes values in the range of [-1, 1], where 1 indicates identical images and values close to 0 or negative values indicate significant differences.


**Threshold for Tampering**:

* After computing the SSIM score, the function compares this score against a predefined threshold (in this case, threshold = 0.9).

* If the SSIM score is less than the threshold (score < threshold), it implies that the tampered image is significantly different from the original image.

* If the SSIM score is greater than or equal to the threshold, it suggests that the tampered image is similar enough to the original image.


**Tampering Decision**:

* Based on the comparison result (score versus threshold), the compare_images function returns "Tampered" if the image is considered significantly different (below the threshold) or "Not Tampered" if it is similar enough (above or equal to the threshold).

**Web Interface Interaction**:

* Flask handles the user's request to upload images, invokes the compare_images function with the uploaded image paths, and captures the result (whether "Tampered" or "Not Tampered").

* The result is then rendered back to the user through the web interface (result.html), indicating whether the uploaded tampered image shows signs of tampering compared to the original.





**Project Structure**

The project directory contains the following files and directories:

app.py: Main Flask application file that handles routing and image processing logic.

templates/: Directory containing HTML templates for frontend presentation (index.html and result.html).

uploads/: Temporary directory to store uploaded image files during processing.

requirements.txt: List of Python packages required to run the application

**Dependencies**

Flask: Web framework for building the backend server.

Pillow: Library for image processing and manipulation.

scikit-image: Library for image processing algorithms (used for SSIM calculation).

OpenCV: Library for computer vision tasks (used for image processing).
