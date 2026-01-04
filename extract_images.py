import json
import os
import argparse

from urllib.parse import urlparse
import base64

def extract_media_entries(har_data):
    media_entries = []
    video_chunks = {}
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        response = entry.get('response', {})
        mime_type = response.get('content', {}).get('mimeType', '')
        base64_data = response.get('content', {}).get('text') if response.get('content', {}).get('encoding') == 'base64' else None
        if mime_type.startswith('image/'):
            if base64_data:
                media_entries.append({
                    'url': url,
                    'mime_type': mime_type,
                    'base64_data': base64_data
                })
        elif mime_type.startswith('video/'):
            # Use filename as key
            filename = os.path.basename(urlparse(url).path)
            # Get chunk order from content-range header if present
            content_range = None
            for h in response.get('headers', []):
                if h.get('name', '').lower() == 'content-range':
                    content_range = h.get('value')
                    break
            # Parse start byte for sorting
            start_byte = 0
            if content_range:
                try:
                    start_byte = int(content_range.split(' ')[1].split('-')[0])
                except Exception:
                    start_byte = 0
            if filename not in video_chunks:
                video_chunks[filename] = []
            video_chunks[filename].append({
                'url': url,
                'mime_type': mime_type,
                'base64_data': base64_data,
                'start_byte': start_byte
            })
    # Combine video chunks
    for filename, chunks in video_chunks.items():
        sorted_chunks = sorted(chunks, key=lambda x: x['start_byte'])
        combined_base64 = ''.join([c['base64_data'] for c in sorted_chunks if c['base64_data']])
        if combined_base64:
            first = sorted_chunks[0]
            media_entries.append({
                'url': first['url'],
                'mime_type': first['mime_type'],
                'base64_data': combined_base64
            })
    return media_entries

def save_media(media_entries, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, entry in enumerate(media_entries):
        mime_type = entry['mime_type']
        ext = mime_type.split('/')[-1].split(';')[0]
        filename = f"media_{i+1}.{ext}"
        filepath = os.path.join(output_dir, filename)
        try:
            if entry.get('base64_data'):
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(entry['base64_data']))
                print(f"Extracted: {filename}")
            else:
                print(f"No base64 data for {filename}, skipping.")
        except Exception as e:
            print(f"Failed to save {filename}: {e}")

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

    media_entries = extract_media_entries(har_data)
    print(f"Found {len(media_entries)} media entries with base64 data.")
    save_media(media_entries, output_dir)

if __name__ == '__main__':
    main()
