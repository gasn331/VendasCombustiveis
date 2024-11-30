from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import sum, col, regexp_replace
from pyspark.sql.types import StringType, DecimalType, StructType, StructField
from pymongo import MongoClient


# Função para iniciar a sessão Spark
def start_spark_session():
    spark = SparkSession.builder \
        .appName("Vendas Processamento") \
        .getOrCreate()
    return spark


# Função para inserir dados no MongoDB
def insert_to_mongo(data, collection_name):
    try:
        client = MongoClient("mongodb://mongodb_container:27017/vendas_combustiveis")
        db = client.vendas_combustiveis
        collection = db[collection_name]

        if data:
            # Converte cada linha do DataFrame para dicionário
            data_dicts = []
            for row in data:
                row_dict = row.asDict()
                # Armazenar vendas como string
                if "vendas" in row_dict and row_dict["vendas"] is not None:
                    row_dict["vendas"] = str(row_dict["vendas"])  # Converte para string
                data_dicts.append(row_dict)

            # Verifica se a lista de dicionários contém dados
            if data_dicts:
                collection.insert_many(data_dicts)
                print(f"Inserido {len(data_dicts)} documentos na coleção {collection_name}.")
            else:
                print(f"Nenhum dado para inserir na coleção {collection_name}.")
        else:
            print(f"Nenhum dado coletado para {collection_name}.")
    except Exception as e:
        print(f"Erro ao inserir dados no MongoDB: {e}")
    finally:
        client.close()


# Função principal para processar o CSV
def process_csv_and_store(csv_path):
    # Inicia a sessão Spark
    spark = start_spark_session()

    # Definindo o esquema da tabela
    schema = StructType([
        StructField("ANO", StringType(), True),
        StructField("MÊS", StringType(), True),
        StructField("GRANDE REGIÃO", StringType(), True),
        StructField("UNIDADE DA FEDERAÇÃO", StringType(), True),
        StructField("PRODUTO", StringType(), True),
        StructField("VENDAS", StringType(), True)  # Inicialmente String
    ])

    # Lê os dados do arquivo CSV com separador `;`
    vendas_df = spark.read.csv(csv_path, schema=schema, sep=';', header=True, nullValue='', escape='"',
                               ignoreLeadingWhiteSpace=True)

    # Mapeamento para renomear colunas
    column_mapping = {
        "ANO": "ano",
        "MÊS": "mes",
        "GRANDE REGIÃO": "grande_regiao",
        "UNIDADE DA FEDERAÇÃO": "unidade_federacao",
        "PRODUTO": "produto",
        "VENDAS": "vendas"
    }

    # Renomeando as colunas
    for original, novo in column_mapping.items():
        vendas_df = vendas_df.withColumnRenamed(original, novo)

    # Converte a coluna 'vendas' de String para Decimal (3 casas decimais)
    vendas_df = vendas_df.withColumn("vendas", regexp_replace(col("vendas"), ",", ".").cast(DecimalType(10, 3)))

    # Verifique se o DataFrame foi preenchido corretamente
    vendas_df.show()

    # Armazenando dados originais no MongoDB
    insert_to_mongo(vendas_df.collect(), "vendas")

    # Chamando as funções de análise
    total_vendas_produto(vendas_df)
    vendas_mensais_estado(vendas_df)
    tendencias_vendas(vendas_df)
    comparativo_regioes(vendas_df)

    print("Dados processados e armazenados no MongoDB.")


# Total de vendas por produto
def total_vendas_produto(vendas_df):
    total_vendas = vendas_df.groupBy("produto").agg(sum("vendas").alias("total_vendas"))

    # Converte para string antes de armazenar no MongoDB
    total_vendas = total_vendas.withColumn("total_vendas", col("total_vendas").cast(StringType()))

    insert_to_mongo(total_vendas.collect(), "total_vendas_produto")


# Vendas mensais por estado
def vendas_mensais_estado(vendas_df):
    vendas_mensais = vendas_df.groupBy("ano", "mes", "unidade_federacao").agg(sum("vendas").alias("vendas_mensal"))

    # Converte para string antes de armazenar no MongoDB
    vendas_mensais = vendas_mensais.withColumn("vendas_mensal", col("vendas_mensal").cast(StringType()))

    insert_to_mongo(vendas_mensais.collect(), "vendas_mensais_estado")


# Análise de tendências de vendas
def tendencias_vendas(vendas_df):
    # Agrupa por ano e produto, somando as vendas
    total_vendas = vendas_df.groupBy("ano", "produto").agg(F.sum("vendas").alias("total_vendas"))

    # Para cada ano, encontra o produto com o maior total de vendas
    max_vendas_per_ano = total_vendas.groupBy("ano").agg(
        F.max("total_vendas").alias("max_vendas")
    )

    # Realiza o join para obter o produto correspondente ao maior total de vendas
    tendencias = max_vendas_per_ano.join(total_vendas, (max_vendas_per_ano["ano"] == total_vendas["ano"]) & (
                max_vendas_per_ano["max_vendas"] == total_vendas["total_vendas"]), how="inner")

    # Seleciona as colunas necessárias: ano, produto e total de vendas
    tendencias = tendencias.select(max_vendas_per_ano["ano"], total_vendas["produto"], total_vendas["total_vendas"])

    # Converte para string antes de armazenar no MongoDB
    tendencias = tendencias.withColumn("total_vendas", F.col("total_vendas").cast(StringType()))

    insert_to_mongo(tendencias.collect(), "tendencias_vendas")


# Comparativo de vendas entre regiões
def comparativo_regioes(vendas_df):
    comparativo = vendas_df.groupBy("grande_regiao", "produto").agg(sum("vendas").alias("vendas_regiao"))

    # Converte para string antes de armazenar no MongoDB
    comparativo = comparativo.withColumn("vendas_regiao", col("vendas_regiao").cast(StringType()))

    insert_to_mongo(comparativo.collect(), "comparativo_regioes")


if __name__ == "__main__":
    process_csv_and_store("resources/vendas-combustiveis-m3-1990-2024.csv")
