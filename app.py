import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import urllib

st.set_page_config(layout="wide", page_title="📊 Stock Dashboard")

# --- DB connection ---
tidb_user = st.secrets["tidb"]["user"]
tidb_password = st.secrets["tidb"]["password"]
tidb_host = st.secrets["tidb"]["host"]
tidb_port = st.secrets["tidb"]["port"]
tidb_db = st.secrets["tidb"]["database"]
tidb_ssl_ca = st.secrets["tidb"]["ssl_ca"]

tidb_password_enc = urllib.parse.quote_plus(tidb_password)

engine = create_engine(
    f"mysql+pymysql://{tidb_user}:{tidb_password_enc}@{tidb_host}:{tidb_port}/{tidb_db}?ssl_ca={tidb_ssl_ca}"
)

# --- Load tables function ---
@st.cache_data(ttl=300)
def load_table(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

# Load tables
vol = load_table("volatility_analysis")
cum = load_table("cumulative_return")
sector = load_table("sector_performance")
corr = load_table("stock_correlation")
monthly = load_table("top5_gainers_losers")

st.title("📊 Data-Driven Stock Analysis Dashboard")


# --- Sample Data ---
data = {
    'Ticker': ['ADANIENT', 'ADANIPORTS', 'BEL', 'TRENT', 'ONGC', 'BPCL', 'SHRIRAMFIN', 'COALINDIA', 'HINDALCO', 'NTPC'],
    'std_dev_daily_return': [0.028, 0.026, 0.023, 0.023, 0.022, 0.021, 0.021, 0.021, 0.020, 0.020]
}
vol = pd.DataFrame(data)

st.subheader("Volatility (Top 10)")

vol_top10 = vol.sort_values("std_dev_daily_return", ascending=False).head(10)

# Define a custom color map
# You'll need to define colors for all tickers if you want full control.
# If a ticker is not in the map, Plotly will assign a default color.
custom_colors = {
    'ADANIENT': '#3E0703',  
    'ADANIPORTS': '#116D6E', 
    'BEL': '#910A67',       
    'TRENT': '#FCDAB7',     
    'ONGC': '#9467bd',      
    'BPCL': '#8c564b',      
    'SHRIRAMFIN': '#e377c2', 
    'COALINDIA': '#7f7f7f',  
    'HINDALCO': '#C30E59',   
    'NTPC': 'maroon'        
}

# Create the bar chart with custom colors
fig = px.bar(vol_top10,
             x="Ticker",
             y="std_dev_daily_return",
             labels={"std_dev_daily_return": "Volatility"},
             color="Ticker", # Still use Ticker for coloring, but the map will override defaults
             color_discrete_map=custom_colors) # Apply the custom color map

st.plotly_chart(fig, use_container_width=True)

# --- Cumulative Return Over Time ---
st.subheader("Cumulative Return (Top 5 Stocks)")

# Ensure numeric
cum["cumulative_return"] = pd.to_numeric(cum["cumulative_return"], errors="coerce")
cum["date"] = pd.to_datetime(cum["date"])

top5_tickers = cum.groupby("Ticker").last()["cumulative_return"].nlargest(5).index.tolist()
df_top5 = cum[cum["Ticker"].isin(top5_tickers)].pivot(index="date", columns="Ticker", values="cumulative_return")
st.plotly_chart(px.line(df_top5, x=df_top5.index, y=df_top5.columns), use_container_width=True)

# --- Sector-wise Performance ---
st.subheader("Sector-wise Performance")

# Ensure 'yearly_return' is numeric
sector["yearly_return"] = pd.to_numeric(sector["yearly_return"], errors="coerce")

# Group by sector and calculate average yearly return
sector_avg = sector.groupby("sector", as_index=False)["yearly_return"].mean()

# Sort sectors by average return descending
sector_avg = sector_avg.sort_values("yearly_return", ascending=False)

# Optional: round values for display
sector_avg["yearly_return"] = sector_avg["yearly_return"].round(2)

# Create bar chart
fig_sector = px.bar(
    sector_avg,
    x="sector",
    y="yearly_return",
    color="yearly_return",
    color_continuous_scale=px.colors.sequential.Sunset,
    labels={"yearly_return": "Avg Yearly Return", "sector": "Sector"},
    text="yearly_return",
    height=600
)

# Improve layout for readability
fig_sector.update_layout(
    title="Average Yearly Return by Sector",
    xaxis_title="Sector",
    yaxis_title="Average Yearly Return",
    coloraxis_colorbar=dict(title="Return"),
    template="plotly_white",
    xaxis_tickangle=-45,
    uniformtext_minsize=10,
    uniformtext_mode='hide',
    title_font_size=24,
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14
)

st.plotly_chart(fig_sector, use_container_width=True)

# --- Stock Correlation Heatmap ---
st.subheader("Stock Correlation Heatmap")

# Pivot correlation table
corr_matrix = corr.pivot(index="Ticker_1", columns="Ticker_2", values="Correlation")
st.plotly_chart(px.imshow(corr_matrix, color_continuous_scale="RdBu", zmin=-1, zmax=1), use_container_width=True)

# --- Monthly Gainers & Losers ---
st.subheader("Monthly Top 5 Gainers & Losers")
month = st.selectbox("Select Month", monthly["Month"].unique())

month_df = monthly[monthly["Month"] == month]
# Ensure numeric
month_df["Monthly_Return"] = pd.to_numeric(month_df["Monthly_Return"], errors="coerce")

gainers = month_df.sort_values("Monthly_Return", ascending=False).head(5)
losers = month_df.sort_values("Monthly_Return").head(5)

st.write("**Top 5 Gainers**")
st.dataframe(gainers[["Ticker","Monthly_Return","Rank","Type"]])

st.write("**Top 5 Losers**")
st.dataframe(losers[["Ticker","Monthly_Return","Rank","Type"]])
