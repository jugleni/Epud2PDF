# Epub2PDF Converter

Epub2PDF Converter is a Python microservice that enables the conversion of `.epub` files to `.pdf` through a REST API. The service uses Flask for API creation and libraries such as `EbookLib` and `WeasyPrint` for file manipulation and conversion.

## Features

- Convert `.epub` files to `.pdf`
- File upload support via HTTP POST request
- Direct PDF file return in the response
- Preservation of original EPUB images in final PDF
- Character encoding handling

## Technologies Used

- Python 3.10
- Flask
- EbookLib
- WeasyPrint

## Requirements

- Docker and Docker Compose installed

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jugleni/Epub2PDF.git
cd Epub2PDF
```

### 2. Docker Setup and Usage

Build and start the container:

```bash
docker-compose up --build
```

The service will be available at http://localhost:3453.

## How to Use

You can use Postman or any HTTP client tool to test the API.

## Detailed API Documentation

### Basic Endpoint Information

- **Endpoint:** `/convert`
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Parameter:** file (EPUB file)
- **Response:** PDF file
- **Service URL:** http://localhost:3453

### Testing Methods

#### 1. Using Postman

**Basic Setup:**
1. Create new POST request to `http://localhost:3453/convert`
2. Go to "Body" tab
3. Select "form-data"
4. Add key `file` (Type: File)
5. Upload your EPUB file

**Detailed Testing Steps:**
1. **Request Configuration:**
   - Method: POST
   - URL: http://localhost:3453/convert
   - Headers: None required (auto-set by Postman)
   
2. **File Upload:**
   - In Body tab → form-data
   - Key: `file`
   - Click dropdown next to key → Select 'File'
   - Value: Click 'Select Files' → Choose EPUB file

3. **Sending and Receiving:**
   - Click 'Send'
   - Expected Response Code: 200 OK
   - Response Type: application/pdf

4. **Saving the PDF:**
   - Click 'Save Response' button (disk icon)
   - Select 'Save as File'
   - Choose location and name (use .pdf extension)

#### 2. Using cURL

```bash
curl -X POST \
  -F "file=@/path/to/your/book.epub" \
  http://localhost:3453/convert \
  --output converted.pdf
```

Expected Output:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 15.2M  100 14.2M  100 1021k   4.2M   307k  0:00:03  0:00:03 --:--:-- 4.5M
```

#### 3. Using Python

```python
import requests

url = 'http://localhost:3453/convert'
files = {'file': open('book.epub', 'rb')}
response = requests.post(url, files=files)

with open('output.pdf', 'wb') as f:
    f.write(response.content)
```

### Response Scenarios

1. **Successful Conversion:**
   - Status: 200 OK
   - Content-Type: application/pdf
   - Body: Binary PDF data

2. **Error Responses:**
   ```json
   // 400 Bad Request
   {"error": "No file provided"}

   // 415 Unsupported Media Type
   {"error": "Invalid file format. Please upload an EPUB file"}

   // 500 Internal Server Error
   {"error": "Conversion failed"}
   ```

### Conversion Process Details

1. File Upload: EPUB received via HTTP POST
2. Temporary Storage: File saved temporarily
3. Content Extraction:
   - Text content extracted
   - Images processed
   - Character encoding fixed
4. Conversion Steps:
   - Images converted to base64
   - HTML template generated
   - WeasyPrint processes HTML to PDF
5. Response: PDF returned to client
6. Cleanup: Temporary files removed

## Docker Operations

### Basic Commands

```bash
# Start service
docker-compose up --build

# Stop service
docker-compose stop

# Remove container
docker-compose down

# View logs
docker-compose logs -f
```

### Container Management

1. **Monitoring:**
   - View logs: `docker-compose logs -f`
   - Check container status: `docker ps`

2. **Resource Management:**
   - Default port: 3453
   - Memory usage varies with EPUB size
   - CPU usage spikes during conversion

3. **Troubleshooting:**
   - Check container status
   - Verify port availability
   - Monitor resource usage
   - Review conversion logs

## Technical Limitations

1. **File Size:**
   - Maximum recommended: 50MB
   - Larger files may cause memory issues

2. **Content:**
   - Complex layouts may not preserve perfectly
   - Image quality matches source
   - Some CSS properties might not convert

3. **Performance:**
   - Processing time varies with file size
   - Memory usage scales with content complexity
   - Multiple simultaneous conversions may impact performance

## Project Structure

```
/epub2pdf-converter
│   ├── app.py              # Main microservice code
│   ├── Dockerfile          # Docker container configuration
│   ├── requirements.txt    # Python dependencies
│   ├── docker-compose.yaml # Docker Compose configuration
│   └── README.md           # This file
```

## Troubleshooting

If you encounter issues with the conversion:

1. Ensure the EPUB file is valid and can be opened in other readers.
2. Make sure the file is not corrupted.
3. For specific encoding issues, check the container logs for more details.

## Contribution

Contributions are welcome! Feel free to open issues and pull requests to improve the project.

## License

This project is licensed under the MIT License.