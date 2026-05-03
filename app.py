import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Netflix Dashboard", page_icon="🎬", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['country'] = df['country'].str.split(',').str[0].str.strip()
    df['genre'] = df['listed_in'].str.split(',').str[0].str.strip()
    return df

df = load_data()

# Header
st.title("🎬 Netflix Content Dashboard")
st.markdown("*Exploring 8,000+ titles to understand how Netflix's content strategy has evolved*")
st.divider()

# Sidebar filters
st.sidebar.header("Filters")
content_type = st.sidebar.multiselect(
    "Content Type", options=df['type'].dropna().unique(),
    default=df['type'].dropna().unique()
)
year_range = st.sidebar.slider(
    "Year Added", 
    int(df['year_added'].min()), 
    int(df['year_added'].max()),
    (2015, 2021)
)

# Filter data
filtered = df[
    (df['type'].isin(content_type)) &
    (df['year_added'] >= year_range[0]) &
    (df['year_added'] <= year_range[1])
]

# KPI row
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered))
col2.metric("Countries", filtered['country'].nunique())
col3.metric("Genres", filtered['genre'].nunique())

st.divider()

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Content Added Per Year")
    yearly = filtered.groupby('year_added').size().reset_index(name='count')
    fig = px.bar(yearly, x='year_added', y='count', color_discrete_sequence=['#E50914'])
    fig.update_layout(xaxis_title="Year", yaxis_title="Titles Added", plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎬 Movies vs TV Shows")
    type_counts = filtered['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig2 = px.pie(type_counts, names='type', values='count',
                  color_discrete_sequence=['#E50914', '#221F1F'])
    st.plotly_chart(fig2, use_container_width=True)

# Charts row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Top 10 Countries")
    top_countries = filtered['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']
    fig3 = px.bar(top_countries, x='count', y='country', orientation='h',
                  color_discrete_sequence=['#E50914'])
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🎭 Top 10 Genres")
    top_genres = filtered['genre'].value_counts().head(10).reset_index()
    top_genres.columns = ['genre', 'count']
    fig4 = px.bar(top_genres, x='count', y='genre', orientation='h',
                  color_discrete_sequence=['#831010'])
    fig4.update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)

# Key insight
st.divider()
st.subheader("💡 Key Insight")
st.info("Netflix added the most content between 2018–2020, after which growth slowed — likely due to COVID production delays and a shift toward quality over quantity.")