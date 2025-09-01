import json
import os
import argparse
import requests
from urllib.parse import urlparse

def extract_image_entries(har_data):
    image_entries = []
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        response = entry.get('response', {})
        mime_type = response.get('content', {}).get('mimeType', '')
        if mime_type.startswith('image/'):
            image_entries.append({
                'url': url,
                'mime_type': mime_type
            })
    return image_entries

def download_images(image_entries, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, entry in enumerate(image_entries):
        url = entry['url']
        mime_type = entry['mime_type']
        ext = mime_type.split('/')[-1].split(';')[0]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            filename = f"image_{i+1}.{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Extract and download images from a HAR file.',
        usage='python extract_images.py <har_file> [-o OUTPUT]'
    )
    parser.add_argument('har_file', help='Path to the HAR file')
    parser.add_argument('-o', '--output', help='Output directory for images')
    args = parser.parse_args()

    # Show help if no arguments are provided
    if not hasattr(args, 'har_file') or args.har_file in ('-h', '--help'):
        parser.print_help()
        return

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        har_dir = os.path.dirname(os.path.abspath(args.har_file))
        output_dir = os.path.join(har_dir, 'images')

    with open(args.har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    image_entries = extract_image_entries(har_data)
    print(f"Found {len(image_entries)} image entries.")
    download_images(image_entries, output_dir)

if __name__ == '__main__':
    main()
