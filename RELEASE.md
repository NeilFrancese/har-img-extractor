# Release 1.1.2

## Features & Fixes
- Gallery filter for images/videos in the web UI
- CLI and web app now reconstruct chunked images/videos from HAR base64 data (no live URL fetch)
- Improved reliability for offline/archived HAR extraction
- Video preview and download support in both CLI and web app

# Features

- Extract images directly from HAR files (base64 only).
- Command-line tool (`har-img-cli-<os>`) for batch extraction.
- Flask web app (`har-img-app-<os>`) for uploading, previewing, and downloading images via a browser.
- Download images individually or as a ZIP archive.
- Cross-platform executables for Windows, macOS, and Linux.
- No external image requests—works entirely offline.

# How to Run Via Binaries

Download the appropriate OS version and follow instructions below for Command-Line Interface (CLI) or via a local Web-App.

## Windows
```powershell
# For CLI tool
har-img-cli-windows.exe <path_to_har_file> [--output <output_folder>]

# For Flask web app
har-img-app-windows.exe
# Then open http://127.0.0.1:5000 in your browser
```

## macOS
```bash
# For CLI tool
./har-img-cli-macos <path_to_har_file> [--output <output_folder>]

# For Flask web app
./har-img-app-macos
# Then open http://127.0.0.1:5000 in your browser
```

## Linux
```bash
# For CLI tool
./har-img-cli-linux <path_to_har_file> [--output <output_folder>]

# For Flask web app
./har-img-app-linux
# Then open http://127.0.0.1:5000 in your browser
```
