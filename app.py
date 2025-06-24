import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")

my_pass = os.getenv('rds_pass')
endpoint = os.getenv('rds_end')
user_rds= os.getenv('rds_user')

# RDS PostgreSQL connection settings

host = endpoint
database = "newsdb"
user = user_rds
password = my_pass

@st.cache_data(ttl=300)
def load_data():
    conn = psycopg2.connect(
        host=host,
        port = 5432,
        database=database,
        user=user,
        password=password
    )
    df = pd.read_sql(
        "SELECT title, description, sentiment, published_at FROM news_articles ORDER BY published_at DESC LIMIT 20",
        conn
    )
    conn.close()
    return df

st.title(" News Sentiment Analysis")
data = load_data()

st.dataframe(data, use_container_width=True)
