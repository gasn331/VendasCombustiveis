FROM bitnami/spark:3.5.3

# Mudar para o usuário root
USER root

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código do aplicativo e o requirements.txt
COPY . .

# Instalar pacotes necessários
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir virtualenv && \
    virtualenv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Atualizar o PATH para incluir o venv
ENV PATH="/venv/bin:$PATH"

# Comando padrão para iniciar o aplicativo Python
CMD ["spark-submit", "--packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0", "/app/spark_consumer/consumer.py"]
