
# Epub2PDF Converter

Epub2PDF Converter é um microserviço desenvolvido em Python que permite a conversão de arquivos `.epub` para `.pdf` via API REST. O serviço utiliza o Flask para a criação da API e bibliotecas como `EbookLib` e `pdfkit` para a manipulação e conversão dos arquivos.

## Funcionalidades

- Conversão de arquivos `.epub` para `.pdf`.
- Suporte a upload de arquivos via requisição HTTP POST.
- Retorno do arquivo PDF convertido diretamente na resposta.

## Tecnologias Utilizadas

- Python 3.10
- Flask
- EbookLib
- pdfkit
- wkhtmltopdf

## Requisitos

- Docker e Docker Compose instalados.
- `wkhtmltopdf` instalado no ambiente Docker para a conversão de HTML para PDF.

## Como Configurar

### 1. Clonar o Repositório

### 1. Clonar o Repositório

```bash
git clone https://github.com/usuario/epub2pdf-converter.git
cd epub2pdf-converter
```

### 2. Configurar o Ambiente Docker

O projeto vem com um Dockerfile e um docker-compose.yaml para configurar o ambiente de forma isolada.

### 3. Construir e Executar o Contêiner

Execute o seguinte comando para construir a imagem e iniciar o microserviço:

```bash
docker-compose up --build
```

O serviço ficará disponível em http://localhost:3453.

## Como Usar

Você pode usar o Postman ou qualquer ferramenta de cliente HTTP para testar a API.

### Endpoint `/convert`

- **Método:** POST
- **Descrição:** Converte um arquivo .epub enviado para .pdf e retorna o PDF convertido.

### Parâmetros da Requisição

- **file:** O arquivo .epub a ser convertido (enviado como multipart/form-data).

### Exemplo de Requisição

Utilizando o curl:

```bash
curl -X POST http://localhost:3453/convert -F "file=@/caminho/para/seu/arquivo.epub" --output converted.pdf
```

Utilizando o Postman:

1. Crie uma nova requisição do tipo POST para http://localhost:5000/convert.
2. No campo "Body", selecione "form-data".
3. Adicione uma chave chamada `file` e carregue o arquivo .epub para ser convertido.
4. Envie a requisição e o arquivo PDF será baixado.

### Exemplo de Resposta

Se a conversão for bem-sucedida, o serviço retornará o arquivo PDF convertido com o código de status 200 OK. Caso haja algum erro, será retornada uma mensagem de erro com o respectivo código de status.

## Estrutura do Projeto

```bash
/epub2pdf-converter
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── docker-compose.yaml
```

- **app.py:** Código principal do microserviço.
- **Dockerfile:** Configura a imagem Docker para o microserviço.
- **requirements.txt:** Lista de dependências do Python.
- **docker-compose.yaml:** Arquivo de configuração para o Docker Compose.

## Personalizações

Se desejar configurar o microserviço para produção, considere:

- Configurar variáveis de ambiente no docker-compose.yaml para gerenciamento seguro de configurações.
- Utilizar um proxy reverso (como Nginx) para lidar com requisições HTTPS.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar o projeto.

## Licença

Este projeto é licenciado sob a MIT License.

## Nota

Para rodar fora do Docker, você precisará instalar o wkhtmltopdf manualmente e configurar as bibliotecas Python. Veja as instruções em wkhtmltopdf.org para instalação.
