# Usar uma imagem base oficial do Python
FROM python:3.10-slim

# Instalar dependências do sistema necessárias para WeasyPrint
RUN apt-get update && \
    apt-get install -y build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Criar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências para o contêiner
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do aplicativo para o contêiner
COPY app.py .

# Expor a porta que o Flask usará
EXPOSE 3453

# Comando para rodar o aplicativo
CMD ["python", "-u", "app.py"]