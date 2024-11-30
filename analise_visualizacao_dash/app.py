import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://mongodb_container:27017/")
db = client["vendas_combustiveis"]
collection = db["vendas"]
# Criar a aplicação Dash
app = dash.Dash(__name__)
combustiveis_dict = [{'label': 'ETANOL HIDRATADO', 'value': 'ETANOL HIDRATADO'},
                     {'label': 'GASOLINA', 'value': 'GASOLINA C'},
                     {'label': 'ÓLEO DIESEL', 'value': 'ÓLEO DIESEL'},
                     {'label': 'GASOLINA DE AVIAÇÃO', 'value': 'GASOLINA DE AVIAÇÃO'},
                     {'label': 'QUEROSENE ILUMINANTE', 'value': 'QUEROSENE ILUMINANTE'},
                     {'label': 'QUEROSENE DE AVIAÇÃO', 'value': 'QUEROSENE DE AVIAÇÃO'},
                     {'label': 'GLP', 'value': 'GLP'},
                     {'label': 'ÓLEO COMBUSTÍVEL', 'value': 'ÓLEO COMBUSTÍVEL'}]


# Layout da aplicação
def generate_app_layout():
    return html.Div(
        style={'backgroundColor': '#f7f7f7', 'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
        children=[
            html.H1("Análises de Vendas de Combustíveis",
                    style={'textAlign': 'center', 'color': '#2196F3', 'fontSize': '3em', 'marginBottom': '40px'}),

            # Gráfico Interativo de Mapa
            html.Div([
                html.H2("Consumo de Combustíveis por Estado e Ano",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),

                html.Label("Ano", style={"font-weight": "bold", "margin-bottom": "10px"}),
                dcc.Dropdown(
                    id='dropdown-ano',
                    options=[{'label': str(year), 'value': year} for year in range(1990, 2024)],
                    value=2023,  # Valor padrão
                    clearable=False,
                    style={'marginBottom': '20px', 'width': '50%'},
                    className='custom-dropdown'
                ),
                html.Label("Produto", style={"font-weight": "bold", "margin-bottom": "10px"}),
                dcc.Dropdown(
                    id='dropdown-produto',

                    options=combustiveis_dict,
                    value='ETANOL HIDRATADO',  # Valor padrão
                    clearable=False,
                    style={'marginBottom': '20px', 'width': '50%'},
                    className='custom-dropdown'
                ),
                dcc.Graph(id='mapa-consumo',
                          style={'border': '1px solid #ddd', 'borderRadius': '10px',
                                 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'height': '500px'})
            ], style={'marginBottom': '40px'}),

            # Gráfico de Pizza
            html.Div([
                html.H2("Distribuição de Vendas Totais por Estado",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),
                dcc.Graph(id='pie-chart')
            ]),

            # Gráfico de Tendência ao Longo do Tempo
            html.Div([
                html.H2("Tendência de Consumo por Estado ao Longo do Tempo",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),
                html.Label("Produto", style={"font-weight": "bold", "margin-bottom": "10px"}),
                dcc.Dropdown(
                    id='dropdown-produto-tendencia',
                    options=combustiveis_dict,
                    value='ETANOL HIDRATADO',  # Valor padrão
                    clearable=False,
                    style={'marginBottom': '20px', 'width': '50%'},
                    className='custom-dropdown'
                ),
                dcc.Graph(id='line-plot',
                          style={'border': '1px solid #ddd', 'borderRadius': '10px',
                                 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'height': '500px'})
            ], style={'marginBottom': '40px'}),

            # Gráfico de Variação de Vendas Mensais
            html.Div([
                html.H2("Variação Mensal de Vendas em um Ano",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),
                html.Label("Estado", style={"font-weight": "bold", "margin-bottom": "10px"}),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': 'ACRE', 'value': 'ACRE'},
                        {'label': 'ALAGOAS', 'value': 'ALAGOAS'},
                        {'label': 'AMAPÁ', 'value': 'AMAPÁ'},
                        {'label': 'AMAZONAS', 'value': 'AMAZONAS'},
                        {'label': 'BAHIA', 'value': 'BAHIA'},
                        {'label': 'CEARÁ', 'value': 'CEARÁ'},
                        {'label': 'DISTRITO FEDERAL', 'value': 'DISTRITO FEDERAL'},
                        {'label': 'ESPÍRITO SANTO', 'value': 'ESPÍRITO SANTO'},
                        {'label': 'GOIÁS', 'value': 'GOIÁS'},
                        {'label': 'MARANHÃO', 'value': 'MARANHÃO'},
                        {'label': 'MATO GROSSO', 'value': 'MATO GROSSO'},
                        {'label': 'MATO GROSSO DO SUL', 'value': 'MATO GROSSO DO SUL'},
                        {'label': 'MINAS GERAIS', 'value': 'MINAS GERAIS'},
                        {'label': 'PARÁ', 'value': 'PARÁ'},
                        {'label': 'PARAÍBA', 'value': 'PARAÍBA'},
                        {'label': 'PARANÁ', 'value': 'PARANÁ'},
                        {'label': 'PERNAMBUCO', 'value': 'PERNAMBUCO'},
                        {'label': 'PIAUÍ', 'value': 'PIAUÍ'},
                        {'label': 'RIO DE JANEIRO', 'value': 'RIO DE JANEIRO'},
                        {'label': 'RIO GRANDE DO NORTE', 'value': 'RIO GRANDE DO NORTE'},
                        {'label': 'RIO GRANDE DO SUL', 'value': 'RIO GRANDE DO SUL'},
                        {'label': 'RONDÔNIA', 'value': 'RONDÔNIA'},
                        {'label': 'RORAIMA', 'value': 'RORAIMA'},
                        {'label': 'SANTA CATARINA', 'value': 'SANTA CATARINA'},
                        {'label': 'SÃO PAULO', 'value': 'SÃO PAULO'},
                        {'label': 'SERGIPE', 'value': 'SERGIPE'},
                        {'label': 'TOCANTINS', 'value': 'TOCANTINS'}
                    ],
                    value='GOIÁS',  # Valor padrão
                    style={'marginBottom': '20px', 'width': '50%'},
                    className='custom-dropdown'
                ),
                dcc.Graph(id='area-chart')
            ]),

            # Gráfico de Box Plot para Análise de Outliers
            html.Div([
                html.H2("Análise de Outliers nas Vendas por Estado",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),
                dcc.Graph(id='box-plot')
            ]),

            # Gráfico de Heatmap
            html.Div([
                html.H2("Heatmap de Consumo por Estado e Ano",
                        style={'color': '#2196F3', 'fontSize': '2em', 'marginBottom': '20px'}),
                dcc.Graph(id='heatmap')
            ])
        ]
    )


# Callback para o gráfico de mapa interativo
@app.callback(
    Output('mapa-consumo', 'figure'),
    [Input('dropdown-ano', 'value'),
     Input('dropdown-produto', 'value')]
)
def update_map(selected_ano, selected_produto):
    # Consultar dados da coleção
    data = list(collection.find({'ano': str(selected_ano), 'produto': selected_produto}))
    df = pd.DataFrame(data)

    # Converter nomes de estados para siglas
    state_to_sigla = {
        'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPÁ': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA',
        'CEARÁ': 'CE', 'DISTRITO FEDERAL': 'DF', 'ESPÍRITO SANTO': 'ES', 'GOIÁS': 'GO',
        'MARANHÃO': 'MA', 'MATO GROSSO': 'MT', 'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG',
        'PARÁ': 'PA', 'PARAÍBA': 'PB', 'PARANÁ': 'PR', 'PERNAMBUCO': 'PE', 'PIAUÍ': 'PI',
        'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN', 'RIO GRANDE DO SUL': 'RS',
        'RONDÔNIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SÃO PAULO': 'SP',
        'SERGIPE': 'SE', 'TOCANTINS': 'TO'
    }

    df['unidade_federacao'] = df['unidade_federacao'].map(state_to_sigla)
    df['vendas'] = df['vendas'].astype(float)
    sales_by_state = df.groupby('unidade_federacao', as_index=False)['vendas'].sum()

    # Criar um mapa coroplético
    fig = px.choropleth(
        sales_by_state,
        locations='unidade_federacao',
        locationmode='geojson-id',
        color='vendas',
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        featureidkey="properties.sigla",
        hover_name='unidade_federacao',
        title=f"Consumo de {selected_produto} em {selected_ano}",
        labels={'vendas': 'Vendas(m3)', 'unidade_federacao': 'Estado'}
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig


# Callback para o gráfico de pizza
@app.callback(
    Output('pie-chart', 'figure'),
    Input('dropdown-ano', 'value')
)
def update_pie_chart(selected_year):
    data = list(collection.find({'ano': str(selected_year)}))
    df = pd.DataFrame(data)

    df['vendas'] = df['vendas'].astype(float)
    sales_by_state = df.groupby('unidade_federacao', as_index=False)['vendas'].sum()

    fig = px.pie(sales_by_state, names='unidade_federacao', values='vendas', labels={'unidade_federacao': 'Estado', 'vendas': 'Vendas(m3)'})
    return fig


# Callback para o gráfico de linha (Tendência de Consumo)
@app.callback(
    Output('line-plot', 'figure'),
    Input('dropdown-produto-tendencia', 'value')
)
def update_line_plot(selected_produto):
    # Filtrar dados com base no produto selecionado
    query = {'produto': selected_produto}
    data = list(collection.find(query))
    df = pd.DataFrame(data)

    if df.empty:
        return px.line(title=f"Sem dados para {selected_produto}")

    # Converter dados para o formato necessário
    df['vendas'] = df['vendas'].astype(float)
    df_grouped = df.groupby(['ano', 'unidade_federacao'], as_index=False)['vendas'].sum()

    # Criar gráfico de linha com todas as linhas representando os estados
    fig = px.line(df_grouped, x='ano', y='vendas', color='unidade_federacao',
                  title=f'Tendência de Consumo de {selected_produto} por Estado ao Longo do Tempo')

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Consumo (Vendas)",
        title_font_size=20,
        legend_title="Estado"
    )
    return fig


# Callback para o gráfico de área
@app.callback(
    Output('area-chart', 'figure'),
    Input('state-dropdown', 'value')
)
def update_area_chart(selected_state):
    data = list(collection.find({'unidade_federacao': selected_state}))
    df = pd.DataFrame(data)

    df['vendas'] = df['vendas'].astype(float)
    df_grouped = df.groupby(['mes'], as_index=False)['vendas'].sum()

    fig = px.area(df_grouped, x='mes', y='vendas', title=f'Variação Mensal de Vendas em {selected_state}', labels={'mes':'Mes', 'vendas': 'Vendas(m3)'})
    return fig


# Callback para o gráfico de box plot
@app.callback(
    Output('box-plot', 'figure'),
    Input('dropdown-ano', 'value')
)
def update_box_plot(selected_year):
    data = list(collection.find({'ano': str(selected_year)}))
    df = pd.DataFrame(data)

    df['vendas'] = df['vendas'].astype(float)
    fig = px.box(df, x='unidade_federacao', y='vendas', labels={'unidade_federacao': 'Estado', 'vendas': 'Vendas(m3)'})
    return fig


# Callback para o gráfico de heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('dropdown-ano', 'value')
)
def update_heatmap(selected_year):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    df['vendas'] = df['vendas'].astype(float)
    sales_by_state_year = df.groupby(['unidade_federacao', 'ano'], as_index=False)['vendas'].sum()

    fig = px.density_heatmap(sales_by_state_year, x='unidade_federacao', y='ano', z='vendas',
                             labels={'ano': 'Ano', 'unidade_federacao': 'Estado', 'vendas': 'Vendas(m3)'})
    return fig


# Executar a aplicação
if __name__ == '__main__':
    app.layout = generate_app_layout()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
