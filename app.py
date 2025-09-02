import zipfile
import io
import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_FOLDER'] = 'images'
app.config['ALLOWED_EXTENSIONS'] = {'har'}

# Configure logging
import sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['IMAGE_FOLDER']):
    os.makedirs(app.config['IMAGE_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_image_entries(har_data):
    media_entries = []
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        response = entry.get('response', {})
        mime_type = response.get('content', {}).get('mimeType', '')
        base64_data = response.get('content', {}).get('text') if response.get('content', {}).get('encoding') == 'base64' else None
        # Get content-length from headers if available
        content_length = None
        for h in response.get('headers', []):
            if h.get('name', '').lower() == 'content-length':
                try:
                    content_length = int(h.get('value'))
                except Exception:
                    content_length = None
                break
        if mime_type.startswith('image/') or mime_type.startswith('video/'):
            media_entries.append({
                'url': url,
                'mime_type': mime_type,
                'base64_data': base64_data,
                'content_length': content_length
            })
    return media_entries


import base64
from flask import session
import uuid
app.secret_key = 'har-image-extractor-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        if 'harfile' not in request.files:
            return 'No file part', 400
        file = request.files['harfile']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Generate a unique ID for this HAR upload
            har_id = str(uuid.uuid4())
            har_save_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{har_id}.har')
            os.rename(filepath, har_save_path)
            session['har_id'] = har_id
            with open(har_save_path, 'r', encoding='utf-8') as f:
                har_data = json.load(f)
            media_entries = extract_image_entries(har_data)
            from urllib.parse import urlparse
            media = []
            base64_media = [entry for entry in media_entries if entry.get('base64_data')]
            for i, entry in enumerate(base64_media):
                parsed_url = urlparse(entry['url'])
                filename = os.path.basename(parsed_url.path)
                # Prepare base64 data URL for preview
                data_url = None
                if entry.get('base64_data'):
                    data_url = f"data:{entry['mime_type']};base64,{entry['base64_data']}"
                # Use content_length from entry, fallback to None
                content_length = entry.get('content_length')
                media.append({
                    'url': entry['url'],
                    'mime_type': entry['mime_type'],
                    'id': i,
                    'filename': filename,
                    'data_url': data_url,
                    'content_length': content_length
                })
            # Do NOT store media_entries or large data in session
            return render_template('gallery.html', images=media)
    return render_template('index.html')


def get_har_data():
    har_id = session.get('har_id')
    if not har_id:
        return None
    har_save_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{har_id}.har')
    if not os.path.exists(har_save_path):
        return None
    with open(har_save_path, 'r', encoding='utf-8') as f:
        return json.load(f)



@app.route('/download_image')
def download_image():
    har_data = get_har_data()
    image_entries = extract_image_entries(har_data) if har_data else []
    requested_filename = request.args.get('filename')
    if not requested_filename:
        return "No filename provided.", 404
    from urllib.parse import urlparse
    import os
    entry = None
    requested_filename_norm = requested_filename.strip().lower()
    for e in image_entries:
        parsed_url = urlparse(e['url'])
        filename = os.path.basename(parsed_url.path)
        filename_norm = filename.strip().lower()
        if filename_norm == requested_filename_norm:
            entry = e
            break
    if entry and entry.get('base64_data'):
        try:
            image_data = base64.b64decode(entry['base64_data'])
            mime_type = entry['mime_type']
            return app.response_class(
                image_data,
                mimetype=mime_type,
                headers={
                    'Content-Disposition': f'attachment; filename={filename}'
                }
            )
        except Exception as e:
            return f"Failed to decode image from HAR: {e}", 500
    print(f"Requested filename: {requested_filename}")
    return "No base64-encoded image found for this filename.", 404

@app.route('/download_all', methods=['POST'])
def download_all():
    har_data = get_har_data()
    image_entries = extract_image_entries(har_data) if har_data else []
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for i, entry in enumerate(image_entries):
            if entry.get('base64_data'):
                try:
                    image_data = base64.b64decode(entry['base64_data'])
                    mime_type = entry['mime_type']
                    ext = mime_type.split('/')[-1].split(';')[0]
                    filename = f"image_{i+1}.{ext}"
                    zipf.writestr(filename, image_data)
                except Exception:
                    continue
    zip_buffer.seek(0)
    return app.response_class(
        zip_buffer.getvalue(),
        mimetype='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=images.zip'
        }
    )

if __name__ == '__main__':
    logging.debug('Starting Flask app...')
    app.run(debug=True)