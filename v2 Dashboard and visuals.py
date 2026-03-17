import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="VibeCheck", layout="wide")

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('dataset.csv')
    df = df.dropna(subset=['Stream', 'Views', 'Likes', 'Comments'])
    df = df[df['Views'] > 0]
    df['Engagement_Rate'] = ((df['Likes'] + df['Comments']) / df['Views']) * 100
    return df

df = load_and_clean_data()

# Sidebar
artist_options = ["All Artists"] + sorted(df['Artist'].unique().tolist())
selected_artist = st.sidebar.selectbox("Select Artist", artist_options)

display_df = df if selected_artist == "All Artists" else df[df['Artist'] == selected_artist]

st.title("Artist Performance Dashboard")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Tracks", len(display_df))
col2.metric("Avg Streams", f"{display_df['Stream'].mean()/1e6:.1f}M")
col3.metric("Avg Views", f"{display_df['Views'].mean()/1e6:.1f}M")

# Scatter Plot
fig = px.scatter(display_df, x="Stream", y="Views", color="most_playedon",
                 hover_name="Track", log_x=True, log_y=True)
st.plotly_chart(fig, use_container_width=True)

# Table
st.subheader("Top Tracks")
st.dataframe(display_df.sort_values(by='Stream', ascending=False).head(10))
