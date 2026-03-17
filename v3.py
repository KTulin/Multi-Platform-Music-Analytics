
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="VibeCheck: Music Intelligence", layout="wide", page_icon="🎧")

# Custom CSS for a Professional Dark Theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #1DB954; /* Spotify Green */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #161b22;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1DB954 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('dataset.csv')
    df = df.dropna(subset=['Stream', 'Views', 'Likes', 'Comments'])
    df = df[df['Views'] > 0]
    df['Engagement_Rate'] = ((df['Likes'] + df['Comments']) / df['Views']) * 100
    return df

df = load_and_clean_data()

# --- 3. SIDEBAR STYLING ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/vinyl.png", width=80)
    st.title("Control Room")
    st.divider()
    artist_options = ["All Artists"] + sorted(df['Artist'].unique().tolist())
    selected_artist = st.selectbox("🎯 Target Artist", artist_options)
    
    st.divider()
    with st.expander("📊 Global Quick Stats"):
        st.write(f"**Top Track:** {df.loc[df['Stream'].idxmax()]['Track']}")
        st.write(f"**Viral Leader:** {df.groupby('Artist')['Engagement_Rate'].mean().idxmax()}")

# Filtering logic
display_df = df if selected_artist == "All Artists" else df[df['Artist'] == selected_artist]

# --- 4. NAVIGATION TABS ---
tab1, tab2 = st.tabs(["📊 PERFORMANCE INSIGHTS", "🔥 ENGAGEMENT LAB"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.title("🎵 Artist Performance Matrix")
    st.caption(f"Real-time analytics for {selected_artist}")
    
    # Modern Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tracks", len(display_df))
    m2.metric("Avg Spotify", f"{display_df['Stream'].mean()/1e6:.1f}M")
    m3.metric("Avg YouTube", f"{display_df['Views'].mean()/1e6:.1f}M")
    m4.metric("Avg Engagement", f"{display_df['Engagement_Rate'].mean():.2f}%")
    
    st.divider()
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        fig = px.scatter(display_df, x="Stream", y="Views", 
                         color="most_playedon", hover_name="Track",
                         size="Stream", log_x=True, log_y=True,
                         color_discrete_map={'Spotify': '#1DB954', 'Youtube': '#FF0000'},
                         template="plotly_dark", title="Streaming Presence Density")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📋 Top Tracks")
        st.dataframe(display_df[['Track', 'Stream', 'most_playedon']].sort_values(by='Stream', ascending=False), height=400)

    # ML SECTION
    with st.container():
        st.divider()
        st.header("🤖 AI Matchmaker")
        st.write("Find songs with a similar 'Vibe' profile.")
        sl1, sl2, sl3 = st.columns(3)
        u_dance = sl1.slider("Danceability", 0.0, 1.0, 0.5)
        u_energy = sl2.slider("Energy", 0.0, 1.0, 0.5)
        u_acoustic = sl3.slider("Acousticness", 0.0, 1.0, 0.5)

        if st.button("Predict Similar Tracks", use_container_width=True):
            features = ['Danceability', 'Energy', 'Acousticness']
            X_scaled = StandardScaler().fit_transform(df[features])
            user_input = StandardScaler().fit([[u_dance, u_energy, u_acoustic]]).transform([[u_dance, u_energy, u_acoustic]])
            indices = NearestNeighbors(n_neighbors=5).fit(X_scaled).kneighbors(user_input)[1]
            
            cols = st.columns(5)
            for idx, i in enumerate(indices[0]):
                with cols[idx]:
                    st.success(f"**{df.iloc[i]['Track']}**")
                    st.caption(df.iloc[i]['Artist'])

# --- TAB 2: ENGAGEMENT ---
# --- TAB 2: THE ENGAGEMENT LAB (V2 - "THE RESEARCH SUITE") ---
with tab2:
    st.title("🔥 The Viral Factor & Engagement Lab")
    st.markdown("#### Deep-Dive into Fan Loyalty vs. Passive Reach")
    
    # 1. TOP ROW: HIGH-LEVEL ENGAGEMENT METRICS
    st.divider()
    e_col1, e_col2, e_col3, e_col4 = st.columns(4)
    
    # Logic for metrics based on selection
    if selected_artist == "All Artists":
        top_val = df['Engagement_Rate'].max()
        avg_val = df['Engagement_Rate'].mean()
        most_viral_name = df.loc[df['Engagement_Rate'].idxmax()]['Artist']
    else:
        top_val = display_df['Engagement_Rate'].max()
        avg_val = display_df['Engagement_Rate'].mean()
        most_viral_name = display_df.loc[display_df['Engagement_Rate'].idxmax()]['Track']

    e_col1.metric("Highest Engagement", f"{top_val:.2f}%")
    e_col2.metric("Platform Average", f"{avg_val:.2f}%")
    e_col3.metric("Engagement Leader", most_viral_name)
    e_col4.metric("Data Points", len(display_df))

    st.divider()

    # 2. MIDDLE ROW: THE MAIN VISUAL + CONTEXT TABLE
    col_chart, col_stats = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📊 Engagement Velocity")
        if selected_artist == "All Artists":
            # Showing top 15 Global
            top_engaged = df.groupby('Artist')['Engagement_Rate'].mean().sort_values(ascending=False).head(15).reset_index()
            fig_viral = px.bar(top_engaged, x='Engagement_Rate', y='Artist', orientation='h',
                              color='Engagement_Rate', color_continuous_scale='Reds',
                              template="plotly_dark")
        else:
            # Showing Artist Tracks
            artist_tracks = display_df.sort_values(by='Engagement_Rate', ascending=False).head(15)
            fig_viral = px.bar(artist_tracks, x='Engagement_Rate', y='Track', orientation='h',
                              color='Engagement_Rate', color_continuous_scale='Blues',
                              template="plotly_dark")
        
        fig_viral.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_viral, use_container_width=True)

    with col_stats:
        st.subheader("🏆 Viral Leaderboard")
        # Creating a simplified ranking table
        rank_df = display_df[['Track', 'Engagement_Rate']].sort_values(by='Engagement_Rate', ascending=False).head(10)
        rank_df['Engagement_Rate'] = rank_df['Engagement_Rate'].map('{:,.2f}%'.format)
        st.table(rank_df) # Using st.table instead of dataframe for a cleaner "report" look

    # 3. BOTTOM ROW: THE "LOGIC" SECTION
    st.divider()
    st.subheader("🧪 Viral Logic Breakdown")
    c_a, c_b, c_c = st.columns(3)
    
    with c_a:
        st.info("**What is Engagement Rate?**\n\nIt is the ratio of Likes and Comments to total Views. It measures how many people moved from 'Watching' to 'Interacting'.")
    with c_b:
        st.warning("**The Passive Zone (< 1%)**\n\nHigh views but low engagement usually suggests the song is on a massive background playlist or used as ad-supported content.")
    with c_c:
        st.success("**The Viral Zone (> 5%)**\n\nThis is the 'Sweet Spot'. Songs in this range have a dedicated fanbase that actively wants to support the artist.")


