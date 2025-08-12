import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px

def get_secret(key):
    return st.secrets.get(key) if hasattr(st, "secrets") and key in st.secrets else None

server = get_secret("DB_SERVER")
database = get_secret("DB_NAME")
username = get_secret("DB_USER")
password = get_secret("DB_PASS")
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
except Exception as e:
    st.error(f"Erro na conexão: {e}")
    st.stop()

# Buscar dados sem provisionado
query = """
SELECT cod_fornecedor, cod_laboratorio, valor
FROM lancamento_conta_corrente
WHERE tipo <> 'provisionado'
"""

df = pd.read_sql(query, conn)

# Agrupar por fornecedor e laboratório
saldo_fornecedor = df.groupby('cod_fornecedor')['valor'].sum().reset_index()
saldo_laboratorio = df.groupby('cod_laboratorio')['valor'].sum().reset_index()

st.title("Saldo Real (excluindo provisionados)")

# Mostrar tabela fornecedor
st.subheader("Tabela - Saldo por Fornecedor")
st.dataframe(saldo_fornecedor)

# Gráfico pizza fornecedor
fig_forn = px.pie(saldo_fornecedor, values='valor', names='cod_fornecedor', title='Saldo por Fornecedor')
st.plotly_chart(fig_forn)

# Mostrar tabela laboratório
st.subheader("Tabela - Saldo por Laboratório")
st.dataframe(saldo_laboratorio)

# Gráfico pizza laboratório
fig_lab = px.pie(saldo_laboratorio, values='valor', names='cod_laboratorio', title='Saldo por Laboratório')
st.plotly_chart(fig_lab)
