# Use a imagem base do Python
FROM python:3.12

# Define o diretório de trabalho como /app para melhor organização
WORKDIR /app

# Copia e instala as dependências primeiro para aproveitar o cache do Docker.
# O arquivo .env não deve ser copiado para a imagem por segurança.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta em que a sua aplicação vai rodar
EXPOSE 5000

# Configuração do Gunicorn
CMD ["gunicorn", "app.app:create_app()", "--bind", "0.0.0.0:5000"]