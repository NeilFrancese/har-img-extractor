
# HAR Image & Video Extractor

A Python tool and Flask web app to extract, preview, and download images and videos (full, non-chunked only) directly from HAR files. Supports bulk and individual downloads, with a clean gallery UI. Designed for easy HAR file uploads and efficient media extraction without external requests.


## Features
- Extract images and videos from HAR files (base64 only)
- Command-line and web (Flask) interfaces
- Preview images and videos in a gallery
- Download images/videos individually or as a ZIP
- No external media requests



## Binary Releases

Pre-built executables for Windows, macOS, and Linux are available in the [Releases](https://github.com/NeilFrancese/har-img-extractor/releases) section.

- **CLI:** Download the appropriate `har-img-cli-<os>` binary for your platform and run:
   ```
   har-img-cli-<os> <path_to_har_file> [--output <output_folder>]
   ```
   Replace `<os>` with `windows.exe`, `macos`, or `linux` as needed.
   - The CLI extracts both images and videos (e.g., mp4) from HAR files using base64 data.

- **Web App:** Download the appropriate `har-img-app-<os>` binary and run:
   ```
   har-img-app-<os>
   ```
   Then open your browser to `http://127.0.0.1:5000`.
   - The web app previews and downloads both images and videos from HAR files.

You can also run from source as described below.


## Command Line Usage (from source)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI script:
   ```bash
   python extract_images.py <path_to_har_file> [--output <output_folder>]
   ```
   - `<path_to_har_file>`: Path to your HAR file
   - `--output <output_folder>`: (Optional) Output folder for extracted media
   - The CLI will extract both images and videos (base64-encoded) from the HAR file.


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
4. Upload a HAR file, preview images and videos, and download as needed

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
