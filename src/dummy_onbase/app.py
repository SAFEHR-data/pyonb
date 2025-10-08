from flask import Flask, request, send_from_directory, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import uuid
import zipfile

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = sorted(f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf'))
    return render_template('upload.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return "No file uploaded", 400

    if uploaded_file.filename.endswith('.pdf'):
        return save_pdf_file(uploaded_file)

    if uploaded_file.filename.endswith('.zip'):
        return extract_and_save_pdfs_from_zip(uploaded_file)

    return "Invalid file type", 400

def save_pdf_file(file):
    timestamp = datetime.now().strftime('%Y%m%d')
    doc_id = str(uuid.uuid4())[:8]
    original = os.path.splitext(file.filename)[0]
    filename = f"{original}_{doc_id}_{timestamp}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return f"PDF uploaded as {filename}<br><a href='/'>Back</a>", 200

def extract_and_save_pdfs_from_zip(file):
    try:
        with zipfile.ZipFile(file) as zip_ref:
            seen = set()
            count = 0
            for member in zip_ref.infolist():
                filename = os.path.basename(member.filename)

                # Skip directories, hidden files, __MACOSX, or already-seen names
                if (not filename or
                    not filename.lower().endswith('.pdf') or
                    '__macosx' in member.filename.lower() or
                    filename in seen):
                    continue

                seen.add(filename)

                with zip_ref.open(member) as pdf_file:
                    timestamp = datetime.now().strftime('%Y%m%d')
                    doc_id = str(uuid.uuid4())[:8]
                    original = os.path.splitext(filename)[0]
                    saved_filename = f"{original}_{doc_id}_{timestamp}.pdf"
                    filepath = os.path.join(UPLOAD_FOLDER, saved_filename)
                    with open(filepath, 'wb') as f:
                        f.write(pdf_file.read())
                    count += 1
        return f"{count} PDF(s) extracted and uploaded<br><a href='/'>Back</a>", 200
    except zipfile.BadZipFile:
        return "Invalid ZIP file", 400


@app.route('/document/<filename>', methods=['GET'])
def get_document_by_filename(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/documents', methods=['GET'])
def get_documents_in_range():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return "Missing start or end parameter", 400

    try:
        start_date = datetime.strptime(start, '%Y%m%d')
        end_date = datetime.strptime(end, '%Y%m%d')
    except ValueError:
        return "Invalid date format. Use YYYYMMDD.", 400

    results = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.pdf'):
            parts = filename.rsplit('_', 2)
            if len(parts) == 3:
                _, doc_id, date_str = parts
                date_str = date_str.replace('.pdf', '')
                try:
                    file_date = datetime.strptime(date_str, '%Y%m%d')
                    if start_date <= file_date <= end_date:
                        results.append({
                            "doc_id": doc_id,
                            "date": date_str,
                            "file_name": filename
                        })
                except ValueError:
                    continue

    return jsonify({"documents": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

