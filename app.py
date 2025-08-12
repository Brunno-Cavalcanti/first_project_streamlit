import os
import streamlit as st
import pandas as pd
import pyodbc

def get_secret(key):
    return st.secrets.get(key) if hasattr(st, "secrets") and key in st.secrets else os.getenv(key)

server = get_secret("DB_SERVER")
database = get_secret("DB_NAME")
username = get_secret("DB_USER")
password = get_secret("DB_PASS")
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    st.success("Conectado ao banco SQL Server!")
except Exception as e:
    st.error(f"Erro na conexão: {e}")
    st.stop()

query = "SELECT TOP 10 * FROM negociacao"
df = pd.read_sql(query, conn)
st.dataframe(df)
