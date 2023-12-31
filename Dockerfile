# Use a imagem base do Python
FROM python:3.12

# Define o diretório de trabalho dentro do contêiner
WORKDIR /

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt requirements.txt

COPY settings.toml settings.toml

COPY .env .env

# Instale as dependências
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório local para o diretório de trabalho
COPY . .

# Exponha a porta em que a sua aplicação vai rodar (ajuste de acordo com a sua aplicação)
EXPOSE 8000

# Configuração do Gunicorn
CMD ["gunicorn", "app.app:create_app()", "--bind", "0.0.0.0:8000"]