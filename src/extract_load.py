import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, URL
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
DB_SCHEMA = os.getenv("DB_SCHEMA_PROD")

# URL de Conexão
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


def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)

    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    
    return dados


def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)

    return pd.concat(todos_dados)


def salvar_no_postgres(df, schema='public'):
    df.to_sql(
        'commodities',
        engine,
        if_exists='replace',
        index=True,
        index_label='Date',
        schema=schema)


if __name__ == "__main__":
    commodities =  ['CL=f', 'GC=f', 'SI=f']
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema='public')