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