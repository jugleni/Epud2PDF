# Epub2PDF Converter

Epub2PDF Converter é um microserviço desenvolvido em Python que permite a conversão de arquivos `.epub` para `.pdf` via API REST. O serviço utiliza Flask para a criação da API e bibliotecas como `EbookLib` e `WeasyPrint` para a manipulação e conversão dos arquivos.

## Funcionalidades

- Conversão de arquivos `.epub` para `.pdf`.
- Suporte a upload de arquivos via requisição HTTP POST.
- Retorno do arquivo PDF convertido diretamente na resposta.
- Preservação de imagens do EPUB original no PDF final.
- Tratamento de problemas de codificação de caracteres.

## Tecnologias Utilizadas

- Python 3.10
- Flask
- EbookLib
- WeasyPrint

## Requisitos

- Docker e Docker Compose instalados.

## Como Configurar

### 1. Clonar o Repositório

```bash
git clone https://github.com/jugleni/Epub2PDF.git
cd Epub2PDF
```

### 2. Construir e Executar o Contêiner

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

### Exemplo de Uso com Postman

1. Abra o Postman.
2. Crie uma nova requisição do tipo POST.
3. Insira a URL: `http://localhost:3453/convert`.
4. Na aba "Body":
   - Selecione "form-data".
   - Adicione uma chave chamada `file`.
   - Clique no dropdown à direita da chave `file` e selecione "File".
   - Clique em "Select Files" e escolha o arquivo .epub que deseja converter.
5. Clique em "Send" para enviar a requisição.
6. O Postman receberá o arquivo PDF convertido como resposta.
7. Para salvar o PDF:
   - Clique no botão "Save Response" (ícone de disquete).
   - Escolha "Save as file".
   - Selecione o local onde deseja salvar o arquivo e dê um nome com a extensão .pdf.

### Exemplo de Uso com cURL

Você também pode usar o cURL para fazer a requisição:

```bash
curl -X POST http://localhost:3453/convert -F "file=@/caminho/para/seu/arquivo.epub" --output converted.pdf
```

Substitua `/caminho/para/seu/arquivo.epub` pelo caminho real do seu arquivo EPUB.

## Como o Serviço Funciona

1. O serviço recebe um arquivo .epub via upload HTTP.
2. O arquivo é temporariamente salvo no servidor.
3. O conteúdo do EPUB é extraído, incluindo texto e imagens.
4. O texto é processado para corrigir problemas de codificação.
5. As imagens são convertidas para base64 e incorporadas no HTML.
6. O HTML resultante é convertido para PDF usando WeasyPrint.
7. O PDF é enviado de volta ao cliente como resposta.
8. Os arquivos temporários são removidos.

## Estrutura do Projeto

```
/epub2pdf-converter
│   ├── app.py              # Código principal do microserviço
│   ├── Dockerfile          # Configuração do contêiner Docker
│   ├── requirements.txt    # Dependências do Python
│   ├── docker-compose.yaml # Configuração do Docker Compose
│   └── README.md           # Este arquivo
```

## Como Remover

Para parar e remover o contêiner:

```bash
docker-compose down
```

Para remover a imagem Docker criada:

```bash
docker rmi epub2pdf-converter_epub_to_pdf_converter
```

Para remover o código-fonte:

```bash
cd ..
rm -rf epub2pdf-converter
```

## Solução de Problemas

Se você encontrar problemas com a conversão:

1. Verifique se o arquivo EPUB é válido e pode ser aberto em outros leitores.
2. Certifique-se de que o arquivo não está corrompido.
3. Para problemas de codificação específicos, verifique os logs do contêiner para mais detalhes.

## Limitações

- EPUBs muito grandes ou com muitas imagens podem causar problemas de memória.
- A qualidade das imagens no PDF depende da qualidade original no EPUB.
- Layouts complexos podem não ser perfeitamente preservados na conversão.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar o projeto.

## Licença

Este projeto é licenciado sob a MIT License.

##Author
Created by Jugleni Krinski