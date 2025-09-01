# HAR Image Extractor

A Python tool and Flask web app to extract, preview, and download images directly from HAR files. Supports bulk and individual downloads, with a clean gallery UI. Designed for easy HAR file uploads and efficient image extraction without external requests.

## Features
- Extract images from HAR files (base64 only)
- Command-line and web (Flask) interfaces
- Preview images in a gallery
- Download images individually or as a ZIP
- No external image requests

## Command Line Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI script:
   ```bash
   python extract_images.py <path_to_har_file> [--output <output_folder>]
   ```
   - `<path_to_har_file>`: Path to your HAR file
   - `--output <output_folder>`: (Optional) Output folder for images

## Flask Web App Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Flask app:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://127.0.0.1:5000`
4. Upload a HAR file, preview images, and download as needed

## File Structure
- `extract_images.py`: CLI tool
- `app.py`: Flask web app
- `templates/`: HTML templates
- `uploads/`: Uploaded HAR files
- `images/`: Extracted images (if used)
- `requirements.txt`: Python dependencies
- `.gitignore`: Common ignores

## License
MIT
