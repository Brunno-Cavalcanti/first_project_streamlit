import os
import streamlit as st
import pandas as pd
import pyodbc

server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = (
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

try:
    conn = pyodbc.connect(conn_str)
    st.success("Conectado ao banco SQL Server!")
except Exception as e:
    st.error(f"Erro na conexão: {e}")
    st.stop()

query = "SELECT TOP 10 * FROM negociacao"
df = pd.read_sql(query, conn)
st.dataframe(df)
