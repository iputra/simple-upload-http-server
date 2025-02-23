# Simple File Upload Server

A lightweight file upload server built with Python and HTML5. This application allows users to upload files through a web interface with drag-and-drop support and automatic handling of duplicate filenames.

## Features

- Drag and drop file upload
- Multiple file selection support
- Progress bars for upload tracking
- Automatic handling of duplicate filenames
- Configurable host and port
- Simple web interface
- Cross-origin resource sharing (CORS) support
- No external dependencies required

## Requirements

- Python 3.x

## Installation

1. Clone or download these files:
   - `server.py`
   - `index.html`

2. Create your project directory:
```bash
mkdir file-upload-server
cd file-upload-server
```

3. Place both files in your project directory
```
file-upload-server/
├── server.py
├── index.html
└── uploads/    (will be created automatically)
```

## Usage

### Starting the Server

1. Basic usage (default: 0.0.0.0:8000):
```bash
python3 server.py
```

2. Custom port:
```bash
python3 server.py --port 9000
```

3. Custom host:
```bash
python3 server.py --host 127.0.0.1
```

4. Both custom host and port:
```bash
python3 server.py --host 192.168.1.100 --port 8080
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| --host   | Host address to listen on | 0.0.0.0 |
| --port   | Port to listen on | 8000 |

To see all available options:
```bash
python3 server.py --help
```

### Accessing the Web Interface

1. Open your web browser
2. Navigate to `http://<host>:<port>`
   - If running locally with default settings: `http://localhost:8000`

### Uploading Files

1. Drag and drop files into the upload area, or click "Select Files" to choose files
2. Click the "Upload Files" button
3. Monitor upload progress through the progress bars
4. Files will be saved in the `uploads` directory

## File Naming

- Files are saved in the `uploads` directory
- If a file with the same name exists:
  - A timestamp suffix is added (format: `YYYYMMDD_HHMMSS`)
  - Example: `document.pdf` becomes `document_20250223_143022.pdf`
- Original filenames are preserved when no conflict exists

## Server Features

- Automatic creation of uploads directory
- Handling of simultaneous multiple file uploads
- Progress tracking for each file
- JSON responses with upload status
- Proper error handling and status messages
- Clean shutdown with Ctrl+C

## Web Interface Features

- Modern, responsive design
- Drag and drop support
- Multiple file selection
- Upload progress bars
- File size display
- Remove button for selected files
- Status messages for success/failure
- Visual feedback for renamed files

## Security Notes

This is a basic implementation intended for local or controlled network use. For production use, consider implementing:

- File size limits
- File type restrictions
- Authentication
- HTTPS support
- Rate limiting
- Additional input validation

## Directory Structure During Operation

```
file-upload-server/
├── server.py           # Server implementation
├── index.html         # Web interface
└── uploads/          # Created automatically
    ├── file1.pdf
    ├── file2_20250223_143022.jpg
    └── ...
```

## Troubleshooting

1. "Address already in use" error:
   - The port is already being used by another process
   - Try a different port: `python3 server.py --port 9000`

2. Can't access server from another computer:
   - Ensure the host is set to '0.0.0.0': `python3 server.py --host 0.0.0.0`
   - Check firewall settings
   - Verify network connectivity

3. Upload directory not created:
   - Ensure write permissions in the server directory
   - Try creating the 'uploads' directory manually
