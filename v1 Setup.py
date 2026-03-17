import streamlit as st
import pandas as pd

st.set_page_config(page_title="VibeCheck", layout="wide")

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('dataset.csv')
    df = df.dropna(subset=['Stream', 'Views', 'Likes', 'Comments'])
    df = df[df['Views'] > 0]
    df['Engagement_Rate'] = ((df['Likes'] + df['Comments']) / df['Views']) * 100
    return df

df = load_and_clean_data()

st.title("Music Analytics Dashboard")
st.dataframe(df.head())
