from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import cgi
from datetime import datetime
import json
import argparse

class FileUploadHandler(BaseHTTPRequestHandler):
    def generate_unique_filename(self, original_filename):
        # Split filename into name and extension
        name, ext = os.path.splitext(original_filename)

        # First try with original filename
        filepath = os.path.join('uploads', original_filename)

        # If file exists, add datetime suffix
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{name}_{timestamp}{ext}"
            filepath = os.path.join('uploads', new_filename)
            return new_filename, filepath

        return original_filename, filepath

    def do_GET(self):
        if self.path == '/':
            # Serve the index.html file
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            # Serve 404 for other paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/upload':
            # Create uploads directory if it doesn't exist
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )

            # Process uploaded files
            if 'file' in form:
                response_data = {
                    "status": "success",
                    "files": []
                }

                file_items = form['file']
                # Handle multiple files
                if isinstance(file_items, list):
                    files = file_items
                else:
                    files = [file_items]

                for file_item in files:
                    if file_item.filename:
                        # Get safe filename with datetime suffix if needed
                        original_filename = os.path.basename(file_item.filename)
                        new_filename, filepath = self.generate_unique_filename(original_filename)

                        # Save the file
                        with open(filepath, 'wb') as f:
                            f.write(file_item.file.read())

                        # Add file info to response
                        response_data["files"].append({
                            "originalName": original_filename,
                            "savedAs": new_filename,
                            "renamed": original_filename != new_filename
                        })

                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
            else:
                # Send error response if no file was uploaded
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "No file uploaded"
                }).encode())

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(host='0.0.0.0', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, FileUploadHandler)
    print(f'Server running on http://{host}:{port}')
    print(f'Uploaded files will be stored in the "uploads" directory')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.server_close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='File Upload Server')
    parser.add_argument('--host', default='0.0.0.0',
                      help='Host address to listen on (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000,
                      help='Port to listen on (default: 8000)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    run_server(host=args.host, port=args.port)
