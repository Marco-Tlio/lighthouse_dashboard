import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="Dashboard Analítico", layout="wide")
st.title("Dashboard Completo: Clientes e Produtos")

@st.cache_data
def load_clientes_data():
    csv_path = "dados_clientes.csv"
    
    if not os.path.exists(csv_path):
        df_mock = pd.DataFrame({
            'customer_id': ['C-101', 'C-542', 'C-331', 'C-988', 'C-112', 'C-774', 'C-445', 'C-223', 'C-901', 'C-882'],
            'ticket_medio': [1500.50, 1420.00, 1350.75, 1200.00, 1150.20, 1100.00, 1050.80, 1010.00, 990.50, 950.00],
            'diversidade_categorias': [15, 14, 18, 13, 16, 13, 15, 14, 19, 13]
        })
        df_mock.to_csv(csv_path, index=False)
        
    return pd.read_csv(csv_path)

@st.cache_data
def load_produtos_data():
    csv_path = "dados_produtos.csv"
    
    if not os.path.exists(csv_path):
        df_mock = pd.DataFrame({
            'produto': ['Notebook XYZ', 'Cadeira Gamer', 'Monitor 24"', 'Teclado Mecânico', 'Mouse Sem Fio', 'Mesa de Escritório', 'Headset Bluetooth', 'Webcam 1080p', 'Cabo HDMI', 'Filtro de Linha', 'Mousepad', 'Suporte Monitor'],
            'sku': ['NB-XYZ-01', 'CG-B-02', 'MON-24-00', 'TEC-MEC-BR', 'MOU-WL-09', 'MES-ESC-01', 'HDS-BT-01', 'WBC-1080', 'CAB-HDM-02', 'FIL-LIN-05', 'MOU-PAD-01', 'SUP-MON-01'],
            'quantidade_vendida': [10, 5, 12, 30, 50, 4, 25, 15, 100, 40, 60, 20],
            'faturamento_total': [25000.00, 4500.00, 8400.00, 4500.00, 2500.00, 3200.00, 3750.00, 2250.00, 3000.00, 2000.00, 1200.00, 1800.00],
            'custo_total': [27500.00, 5200.00, 9000.00, 4800.00, 2600.00, 2800.00, 3000.00, 2000.00, 1500.00, 1200.00, 500.00, 1000.00] 
        })
        df_mock.to_csv(csv_path, index=False)
        
    return pd.read_csv(csv_path)

@st.cache_data
def load_lucro_clientes_data():
    csv_path = "dados_lucro_clientes.csv"
    
    if not os.path.exists(csv_path):
        df_mock = pd.DataFrame({
            'cliente_id': [101, 542, 331, 988, 112, 774, 445, 223, 901, 882],
            'nome_cliente': ['Tech Solutions LTDA', 'Inovação SA', 'Gamer Store', 'Comercial ABC', 'Escritórios Modernos', 'Tech Tudo', 'Global Imports', 'Atacado Central', 'Mega TI', 'Serviços XYZ'],
            'lucro_acumulado': [12500.00, 9800.50, 8750.00, 7200.25, 6500.00, 5900.80, 5100.00, 4850.50, 4200.00, 3950.00]
        })
        df_mock.to_csv(csv_path, index=False)
        
    return pd.read_csv(csv_path)

@st.cache_data
def load_vendas_dia_semana_data():
    csv_path = "dados_vendas_dia_semana.csv"
    
    if not os.path.exists(csv_path):
        df_mock = pd.DataFrame({
            'dow': [0, 1, 2, 3, 4, 5, 6],
            'dia_semana': ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
            'media_vendas': [1200.50, 3100.20, 3450.00, 3600.75, 3300.90, 4100.00, 2500.00]
        })
        df_mock.to_csv(csv_path, index=False)
        
    return pd.read_csv(csv_path)

st.header("Top 10 Clientes por Ticket Médio")

df_clientes = load_clientes_data()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Tabela de Dados")
    st.dataframe(
        df_clientes.style.format({"ticket_medio": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("Gráfico de Ticket Médio")
    df_chart_clientes = df_clientes.set_index('customer_id')['ticket_medio']
    st.bar_chart(df_chart_clientes, color="#1f77b4") 

st.divider()

st.header("Top 10 Clientes por Lucro Acumulado")

df_lucro_clientes = load_lucro_clientes_data()

col3, col4 = st.columns([1, 2])

with col3:
    st.subheader("Tabela de Lucro")
    st.dataframe(
        df_lucro_clientes.style.format({"lucro_acumulado": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

with col4:
    st.subheader("Gráfico de Lucro Acumulado")
    df_chart_lucro = df_lucro_clientes.set_index('nome_cliente')['lucro_acumulado']
    st.bar_chart(df_chart_lucro, color="#ff7f0e")

st.divider()

st.header("Comparação: Custo vs Lucro por Produto")

df_produtos = load_produtos_data()

df_produtos['lucro_total'] = df_produtos['faturamento_total'] - df_produtos['custo_total']

itens_por_pagina = 10
total_paginas = (len(df_produtos) - 1) // itens_por_pagina + 1

if total_paginas > 1:
    pagina_atual = st.selectbox("Selecione a página de produtos", range(1, total_paginas + 1))
else:
    pagina_atual = 1

indice_inicio = (pagina_atual - 1) * itens_por_pagina
indice_fim = indice_inicio + itens_por_pagina

df_produtos_paginado = df_produtos.iloc[indice_inicio:indice_fim]

col5, col6 = st.columns([1, 2])

with col5:
    st.subheader("Tabela de Detalhes")
    st.dataframe(
        df_produtos_paginado[['produto', 'custo_total', 'lucro_total']].style.format({
            "custo_total": "R$ {:.2f}", 
            "lucro_total": "R$ {:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

with col6:
    st.subheader("Gráfico de Custo e Lucro")
    df_chart_produtos = df_produtos_paginado.set_index('produto')[['custo_total', 'lucro_total']]
    st.bar_chart(df_chart_produtos, color=["#d62728", "#2ca02c"])

st.divider()

st.header("Média de Vendas por Dia da Semana")

df_vendas_semana = load_vendas_dia_semana_data()

dias_selecionados = st.multiselect(
    "Filtrar dias da semana",
    options=df_vendas_semana['dia_semana'].tolist(),
    default=df_vendas_semana['dia_semana'].tolist()
)

df_vendas_semana_filtrado = df_vendas_semana[df_vendas_semana['dia_semana'].isin(dias_selecionados)]

col7, col8 = st.columns([1, 2])

with col7:
    st.subheader("Tabela de Vendas")
    st.dataframe(
        df_vendas_semana_filtrado[['dia_semana', 'media_vendas']].style.format({"media_vendas": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

with col8:
    st.subheader("Gráfico de Vendas")
    
    chart_vendas = alt.Chart(df_vendas_semana_filtrado).mark_square(size=600, color="#9467bd").encode(
        x=alt.X('dia_semana:N', sort=df_vendas_semana_filtrado['dia_semana'].tolist(), title="Dia da Semana"),
        y=alt.Y('media_vendas:Q', title="Média de Vendas (R$)"),
        tooltip=['dia_semana', 'media_vendas']
    ).properties(
        height=350
    )
    
    st.altair_chart(chart_vendas, use_container_width=True)