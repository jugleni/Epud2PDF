import os
from flask import Flask, request, send_file, jsonify
import ebooklib
from ebooklib import epub
import pdfkit
import tempfile

app = Flask(__name__)

def epub_to_pdf(epub_file_path, pdf_file_path):
    # Lê o arquivo EPUB
    book = epub.read_epub(epub_file_path)
    html_content = ""

    # Itera pelos itens do livro e extrai o conteúdo HTML
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content += item.get_content().decode("utf-8")

    # Converte o conteúdo HTML para PDF
    options = {
        'encoding': 'UTF-8',
    }
    pdfkit.from_string(html_content, pdf_file_path, options=options)

@app.route('/convert', methods=['POST'])
def convert_epub_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.epub'):
        return jsonify({"error": "File format not supported. Please upload a .epub file"}), 400

    # Salva o arquivo .epub temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as temp_epub_file:
        epub_file_path = temp_epub_file.name
        file.save(epub_file_path)

    # Cria um arquivo PDF temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
        pdf_file_path = temp_pdf_file.name

    try:
        # Converte o .epub para .pdf
        epub_to_pdf(epub_file_path, pdf_file_path)
        # Retorna o PDF convertido para o usuário
        return send_file(pdf_file_path, as_attachment=True, download_name='converted.pdf')
    finally:
        # Remove os arquivos temporários
        os.remove(epub_file_path)
        os.remove(pdf_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3453)
