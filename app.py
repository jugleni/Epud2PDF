import os
import sys
from flask import Flask, request, send_file, jsonify
import ebooklib
from ebooklib import epub
import tempfile
from weasyprint import HTML
import html
import base64

app = Flask(__name__)

def decode_html_entities(text):
    return html.unescape(text)

def epub_to_pdf(epub_file_path, pdf_file_path):
    print(f"epub_file_path: {epub_file_path}", file=sys.stderr)
    print(f"pdf_file_path: {pdf_file_path}", file=sys.stderr)
    print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
    print(f"Files in current directory: {os.listdir()}", file=sys.stderr)
    
    # Lê o arquivo EPUB
    book = epub.read_epub(epub_file_path)
    html_content = ""
    
    # Dicionário para armazenar as imagens
    images = {}

    # Itera pelos itens do livro e extrai o conteúdo HTML e imagens
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8', errors='ignore')
            content = decode_html_entities(content)
            html_content += content
        elif item.get_type() == ebooklib.ITEM_IMAGE:
            # Armazena a imagem com sua ID
            images[item.id] = base64.b64encode(item.content).decode('utf-8')

    # Substitui as referências de imagem pelos dados base64
    for image_id, image_data in images.items():
        html_content = html_content.replace(f'src="{image_id}"', f'src="data:image/png;base64,{image_data}"')

    # Adiciona meta tag para especificar a codificação
    html_content = f'<meta charset="UTF-8">\n{html_content}'

    # Salva o conteúdo HTML em um arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html_file:
        temp_html_path = temp_html_file.name
        temp_html_file.write(html_content)

    print(f"Temporary HTML file path: {temp_html_path}", file=sys.stderr)

    try:
        # Converte o conteúdo HTML para PDF usando WeasyPrint
        HTML(temp_html_path).write_pdf(pdf_file_path)
    except Exception as e:
        print(f"Error during PDF conversion: {str(e)}", file=sys.stderr)
        raise
    finally:
        # Remove o arquivo HTML temporário
        os.remove(temp_html_path)

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
        return send_file(pdf_file_path, as_attachment=True, download_name='converted.pdf', mimetype='application/pdf')
    except Exception as e:
        print(f"Error in conversion process: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500
    finally:
        # Remove os arquivos temporários
        os.remove(epub_file_path)
        os.remove(pdf_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3453)