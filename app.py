import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="EconForecast Rwanda",
    page_icon="🇷🇼",
    layout="wide"
)

# Title
st.title("🇷🇼 EconForecast — Rwanda GDP Growth Dashboard")
st.markdown("Forecasting Rwanda's GDP Growth Rate using ARIMA Time Series Model")
st.divider()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Data/rwanda_gdp_data.csv")
    return df

df = load_data()
df_clean = df[df['Year'] != 1994].reset_index(drop=True)

# ── Key Statistics ──
st.subheader("📊 Key Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Growth Rate", f"{df_clean['GDP_Growth_Rate'].mean():.2f}%")
col2.metric("Highest Growth", f"{df_clean['GDP_Growth_Rate'].max():.2f}%")
col3.metric("Lowest Growth", f"{df_clean['GDP_Growth_Rate'].min():.2f}%")
col4.metric("Latest GDP (USD)", f"${df['GDP_Current_USD'].iloc[0]/1e9:.2f}B")

st.divider()

# ── Forecast Selector ──
st.sidebar.header("⚙️ Forecast Settings")
forecast_years = st.sidebar.slider(
    "Select Forecast Years",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

# ── ARIMA Forecast ──
model = ARIMA(df_clean['GDP_Growth_Rate'], order=(0, 0, 0))
result = model.fit()
forecast = result.get_forecast(steps=forecast_years)
forecast_df = pd.DataFrame({
    'Year': range(2025, 2025 + forecast_years),
    'Forecast': forecast.predicted_mean.values,
    'Lower_CI': forecast.conf_int().iloc[:, 0].values,
    'Upper_CI': forecast.conf_int().iloc[:, 1].values
})

# ── GDP Growth Chart ──
st.subheader("📈 Historical GDP Growth Rate")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=df['Year'], y=df['GDP_Growth_Rate'],
    mode='lines+markers', name='GDP Growth Rate',
    line=dict(color='blue')
))
fig1.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
fig1.add_annotation(x=1994, y=-50, text="Genocide", showarrow=True, font=dict(color="red"))
fig1.add_annotation(x=2020, y=-3.4, text="COVID-19", showarrow=True, font=dict(color="red"))
fig1.update_layout(xaxis_title="Year", yaxis_title="Growth Rate (%)", height=400)
st.plotly_chart(fig1, use_container_width=True)

# ── Forecast Chart ──
st.subheader("🔮 GDP Growth Forecast")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_clean['Year'], y=df_clean['GDP_Growth_Rate'],
    mode='lines+markers', name='Historical', line=dict(color='blue')
))
fig2.add_trace(go.Scatter(
    x=forecast_df['Year'], y=forecast_df['Forecast'],
    mode='lines+markers', name='Forecast', line=dict(color='green', dash='dash')
))
fig2.add_trace(go.Scatter(
    x=pd.concat([forecast_df['Year'], forecast_df['Year'][::-1]]),
    y=pd.concat([forecast_df['Upper_CI'], forecast_df['Lower_CI'][::-1]]),
    fill='toself', fillcolor='rgba(0,255,0,0.1)',
    line=dict(color='rgba(255,255,255,0)'), name='95% Confidence Interval'
))
fig2.add_vline(x=2024, line_dash="dash", line_color="gray")
fig2.update_layout(xaxis_title="Year", yaxis_title="Growth Rate (%)", height=400)
st.plotly_chart(fig2, use_container_width=True)

# ── Forecast Table ──
st.subheader("📋 Forecast Values")
st.dataframe(forecast_df.round(2), use_container_width=True)

# ── Download Button ──
st.divider()
csv = df.to_csv(index=False)
st.download_button(
    label="⬇️ Download Rwanda GDP Data",
    data=csv,
    file_name="rwanda_gdp_data.csv",
    mime="text/csv"
)

st.caption("Data Source: World Bank API | Model: ARIMA(0,0,0) | Author: Jean Pierre NIYOMUGABO")