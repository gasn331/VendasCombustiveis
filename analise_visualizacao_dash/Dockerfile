# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que o Dash usará
EXPOSE 8050

# Comando para iniciar a aplicação Dash
CMD ["bash"]
