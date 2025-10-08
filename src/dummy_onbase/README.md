# Flask PDF Uploader

A simple Flask app to upload individual PDF files or ZIP archives containing multiple PDFs. Uploaded files are stored with a timestamp and unique ID.

## Features

- Upload a single `.pdf` file
- Upload a `.zip` file containing multiple PDFs
- View and download uploaded PDFs
- Filter documents by date range

## Requirements

- Python 3.11+ (if running without Docker)
- Docker (recommended for deployment)

---

## 🐳 Run with Docker

### 1. Build the Docker image

```bash
docker build -t pdf-uploader .
```

### 2. Run the container
```bash
docker run -d -p 49123:5000 -v $(pwd)/data:/app/data pdf-uploader
```