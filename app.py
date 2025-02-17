import os
import sys
from flask import Flask, request, send_file, jsonify
import ebooklib
from ebooklib import epub
import tempfile
from weasyprint import HTML
import html
import base64

# Add these new imports
from sys import setrecursionlimit
from collections import deque

app = Flask(__name__)

# Increase Python's recursion limit
setrecursionlimit(10000)

def decode_html_entities(text):
    return html.unescape(text)

def process_content_safely(content):
    """Process content in chunks to avoid recursion issues"""
    try:
        chunk_size = 1024 * 1024  # 1MB chunks
        if len(content) > chunk_size:
            result = []
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i + chunk_size]
                result.append(decode_html_entities(chunk))
            return ''.join(result)
        return decode_html_entities(content)
    except Exception as e:
        print(f"Content processing error: {str(e)}", file=sys.stderr)
        return content

def epub_to_pdf(epub_file_path, pdf_file_path):
    try:
        print(f"Processing EPUB: {epub_file_path}", file=sys.stderr)
        
        # Read the EPUB file
        book = epub.read_epub(epub_file_path)
        html_parts = []
        images = {}

        # Process items iteratively instead of recursively
        items = deque(book.get_items())
        while items:
            item = items.popleft()
            
            try:
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content().decode('utf-8', errors='ignore')
                    processed_content = process_content_safely(content)
                    html_parts.append(processed_content)
                
                elif item.get_type() == ebooklib.ITEM_IMAGE:
                    try:
                        images[item.id] = base64.b64encode(item.content).decode('utf-8')
                    except Exception as img_error:
                        print(f"Image processing error for {item.id}: {str(img_error)}", file=sys.stderr)
                        continue
            
            except Exception as item_error:
                print(f"Error processing item: {str(item_error)}", file=sys.stderr)
                continue

        # Combine HTML content
        html_content = '\n'.join(html_parts)

        # Process images in chunks
        for image_id, image_data in images.items():
            try:
                html_content = html_content.replace(
                    f'src="{image_id}"',
                    f'src="data:image/png;base64,{image_data}"'
                )
            except Exception as img_replace_error:
                print(f"Image replacement error for {image_id}: {str(img_replace_error)}", file=sys.stderr)
                continue

        # Add meta tags and styling
        html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ margin: 3em; }}
                    img {{ max-width: 100%; height: auto; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
        """

        # Save HTML content in chunks
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html_file:
            chunk_size = 1024 * 1024  # 1MB chunks
            for i in range(0, len(html_content), chunk_size):
                temp_html_file.write(html_content[i:i + chunk_size])
            temp_html_path = temp_html_file.name

        try:
            # Convert to PDF with error handling
            HTML(temp_html_path).write_pdf(pdf_file_path)
        except Exception as pdf_error:
            print(f"PDF conversion error: {str(pdf_error)}", file=sys.stderr)
            raise
        finally:
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

    except Exception as e:
        print(f"General conversion error: {str(e)}", file=sys.stderr)
        raise

@app.route('/convert', methods=['POST'])
def convert_epub_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.epub'):
        return jsonify({"error": "File format not supported. Please upload a .epub file"}), 400

    try:
        # Create temporary files with error handling
        epub_file_path = None
        pdf_file_path = None

        with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as temp_epub_file:
            epub_file_path = temp_epub_file.name
            file.save(epub_file_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
            pdf_file_path = temp_pdf_file.name

        # Convert EPUB to PDF
        epub_to_pdf(epub_file_path, pdf_file_path)

        return send_file(
            pdf_file_path,
            as_attachment=True,
            download_name='converted.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        error_message = f"Conversion error: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message}), 500

    finally:
        # Clean up temporary files
        if epub_file_path and os.path.exists(epub_file_path):
            os.remove(epub_file_path)
        if pdf_file_path and os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3453)