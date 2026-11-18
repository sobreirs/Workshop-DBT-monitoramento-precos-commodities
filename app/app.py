
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, URL, text
import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho da raiz do projeto
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

# Variáveis de ambiente
DB_HOST = os.getenv("DB_HOST_PROD")
DB_PORT = os.getenv("DB_PORT_PROD")
DB_NAME = os.getenv("DB_NAME_PROD")
DB_USER = os.getenv("DB_USER_PROD")
DB_PASS = os.getenv("DB_PASS_PROD")
DB_SCHEMA = os.getenv("DB_SCHEMA_PROD", "public")

# URL de conexão
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

# Engine
engine = create_engine(DATABASE_URL)


# Buscar dados
def get_data():
    query = text(f"""
        SELECT
            data,
            simbolo,
            valor_fechamento,
            acao,
            quantidade,
            valor,
            ganho
        FROM "{DB_SCHEMA}".dm_commodities
        ORDER BY data DESC, simbolo;
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


# Configuração da página
st.set_page_config(
    page_title="Dashboard de Commodities",
    layout="wide"
)

# Título
st.title("Commodities")

# Descrição
st.write("""
Este dashboard apresenta os dados de commodities e suas movimentações.
""")

# Exibição dos dados
try:
    df = get_data()

    if df.empty:
        st.warning("Nenhum registro encontrado na tabela dm_commodities.")
    else:
        st.metric("Total de registros", len(df))

        st.subheader("Movimentações de Commodities")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(f"Erro ao consultar o banco de dados: {e}")
