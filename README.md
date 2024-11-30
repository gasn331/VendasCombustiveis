
# Projeto de Vendas de Combustíveis - Análise e Visualização

Este projeto é uma aplicação de análise de dados de vendas de combustíveis, com processamento de dados utilizando **Apache Spark** e visualização por meio de uma aplicação **Dash**. O sistema é orquestrado com **Docker** para facilitar a configuração e execução de todos os serviços necessários.

## Serviços

O projeto está composto pelos seguintes serviços no **Docker Compose**:

1. **MongoDB**: Banco de dados para armazenar os dados processados.
2. **Spark (Master)**: O Apache Spark para processamento de dados em larga escala.
3. **Spark Worker**: Um worker para o Apache Spark, responsável por executar tarefas distribuídas.
4. **Spark Consumer**: Um consumidor que utiliza o Spark para consumir dados de um tópico Kafka (ou outra origem de dados), processá-los e armazená-los no MongoDB.
5. **Aplicação Dash**: Interface web que exibe gráficos e insights a partir dos dados processados pelo Spark.

## Pré-requisitos

Antes de rodar o projeto, é necessário garantir que você tenha o **Docker** e o **Docker Compose** instalados em sua máquina.

- **Docker**: [Instruções de instalação do Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instruções de instalação do Docker Compose](https://docs.docker.com/compose/install/)

## Estrutura do Projeto

A estrutura de diretórios do projeto é a seguinte:

```plaintext
.
├── Dockerfile               # Dockerfile do Spark Consumer
├── docker-compose.yml       # Arquivo para orquestrar os containers
├── requirements.txt         # Dependências do projeto
├── mongo.conf               # Arquivo de configuração do MongoDB
├── analise_visualizacao_dash/  # Código da aplicação Dash
│   ├── Dockerfile           # Dockerfile da aplicação Dash
│   ├── app.py               # Código principal da aplicação Dash
│   ├── requirements.txt     # Dependências do Dash
│   ├── assets/              # assets do app do Dash
│   │   └── styles.css       # Arquivo de definição de classes CSS para os assets do dashboard
├── spark_consumer/          # Código do Spark Consumer (processamento de dados)
│   ├── __init__.py          # Dockerfile da aplicação Dash
│   ├── config.py            # Dockerfile da aplicação Dash
│   └── consumer.py          # Código Python do consumidor Spark
├── database/                # Código do Spark Consumer (processamento de dados)
├── mongo-init/              # Código do Spark Consumer (processamento de dados)
└──  resources/              # Código do Spark Consumer (processamento de dados)
```

## Como Rodar

Para rodar o projeto, siga os passos abaixo:

1. **Clonar o repositório** (se necessário):
   ```bash
   git clone <url_do_repositorio>
   cd <diretorio_do_projeto>
   ```

2. **Criar e iniciar os containers** com Docker Compose:
   - Execute o comando abaixo para construir as imagens e iniciar os containers:
     ```bash
     docker-compose up --build
     ```
   - O Docker Compose irá criar os containers para o MongoDB, Spark, e a aplicação Dash.


3. **Executando o Dash para Visualização de Gráficos**

Para visualizar os gráficos, siga os passos abaixo:

4. **Acesse o container do Dash:**
   O primeiro passo é acessar o container onde o aplicativo Dash está rodando. Utilize o comando abaixo para acessar o terminal interativo do container:

   ```bash
   docker exec -it dash_app bash
   ``` 
5. Executar o aplicativo Dash

Dentro do container, execute o aplicativo Dash utilizando o comando:

```bash
python app.py
```

6. **Acessar o Dashboard**

Após o comando ser executado, o Dash estará em funcionamento e você poderá visualizar os gráficos no seu navegador. Acesse o dashboard em:
http://localhost:8050


## Considerações Finais

Esse projeto foi desenvolvido para oferecer uma solução de análise e visualização de dados de vendas de combustíveis de maneira eficiente e escalável utilizando o Apache Spark e o Dash.
