db = db.getSiblingDB('vendas_combustiveis');  // Define o banco de dados
db.createCollection('vendas');            // Cria a coleção 'vendas' dentro do banco de dados
db.createCollection('total_vendas_produto');            // Cria a coleção 'total_vendas_produto' dentro do banco de dados
db.createCollection('vendas_mensais_estado');            // Cria a coleção 'vendas_mensais_estado' dentro do banco de dados
db.createCollection('tendencias_vendas');            // Cria a coleção 'tendencias_vendas' dentro do banco de dados
db.createCollection('vendas_sazonais');            // Cria a coleção 'vendas_sazonais' dentro do banco de dados
db.createCollection('comparativo_regioes');            // Cria a coleção 'comparativo_regioes' dentro do banco de dados