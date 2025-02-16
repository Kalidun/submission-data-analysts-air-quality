import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Dashboard Air Quality",
    page_icon="📊",
    #   layout="wide",
)

def get_station_location(df):
    return df["Station"].unique()[0]


def get_data_count(df):
    return len(df)


def create_yearly_polution_df(df):
    yearly_polution_df = df.groupby(by="Year").agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "NO2": "mean",
        "CO": "mean",
        "SO2": "mean",
        "O3": "mean"
    })
    return yearly_polution_df

def create_daily_polution_df(df):
    daily_polution_df = df.groupby(by="Date").agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "NO2": "mean",
        "CO": "mean",
        "SO2": "mean",
        "O3": "mean"
    })
    return daily_polution_df

def create_daily_weather_df(df):
    daily_weather_df = df.groupby(by="Date").agg({
        "TEMP": "mean",
        "PRES": "mean",
        "DEWP": "mean",
        "RAIN": "mean",
        "Wind_Speed": "mean"
    })
    return daily_weather_df

def create_hourly_data_df(df):
    last_day = pd.to_datetime(df["Date"]).dt

    last_day_df = df[df["Year"] == last_day.year.max()][df["Month"] == last_day.month.max()][df["Day"] == last_day.day.max()]

    return last_day_df

df = pd.read_csv("dashboard/cleaned_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

min_date = df["Date"].min()
max_date = df["Date"].max()

st.title("Dashboard Air Quality")
st.subheader("Visualisasi Data")

with st.sidebar:
    st.subheader("Filter Data")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date.date(),
        value=[min_date.date(), max_date.date()]
    )

    start_date = pd.to_datetime(start_date).replace(hour=23)
    end_date = pd.to_datetime(end_date).replace(hour=23)

    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

st.columns(2)
col1, col2 = st.columns(2)

with col1:
    station = get_station_location(filtered_df)
    st.metric(
        "Station :",
        value=station,
    )

with col2:
    data_count = get_data_count(filtered_df)
    st.metric(
        "Jumlah Data :",
        value=data_count,
    )

with st.container():
    st.subheader("Rentang Waktu")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Mulai: {start_date}")

    with col2:
        st.write(f"Selesai: {end_date}")
        
        
plt.figure(figsize=(10, 5))
yearly_polution_df = create_yearly_polution_df(df)

plt.plot(yearly_polution_df.index, yearly_polution_df["PM2.5"], marker='o', label='PM2.5', color='blue')
plt.plot(yearly_polution_df.index, yearly_polution_df["PM10"], marker='s', label='PM10', color='red')
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Polusi")
plt.title("Rata-rata Polusi per Tahun")
plt.legend()
st.pyplot(plt)

st.subheader("Rata-rata Polusi per Hari")
plt.figure(figsize=(10, 5))
daily_polution_df = create_daily_polution_df(filtered_df)

plt.plot(daily_polution_df.index, daily_polution_df["PM2.5"], marker='o', label='Polusi PM2.5', color='blue')
plt.plot(daily_polution_df.index, daily_polution_df["PM10"], marker='s', label='Polusi PM10', color='red')
plt.xlabel("Tanggal")
plt.ylabel("Rata-rata Polusi")
plt.title("Rata-rata Polusi per Hari")
plt.legend()
st.pyplot(plt)

st.subheader("Informasi Lainnya")
plt.figure(figsize=(10, 5))
daily_weather_df = create_daily_weather_df(filtered_df)

plt.plot(daily_weather_df.index, daily_weather_df["TEMP"], marker='o', label='Suhu Udara', color='blue')
plt.plot(daily_weather_df.index, daily_weather_df["DEWP"], marker='*', label='Kelembapan', color='green')
plt.xlabel("Tanggal")
plt.ylabel("Informasi lainnya")
plt.title("Rata-rata")
plt.legend()
st.pyplot(plt)

st.subheader("Curah Hujan")

plt.figure(figsize=(10, 5))
plt.plot(daily_weather_df.index, daily_weather_df["RAIN"], marker='o', label='Curah Hujan', color='blue')
plt.xlabel("Tanggal")
plt.ylabel("Curah Hujan")
plt.title("Curah Hujan per Hari")
plt.legend()
st.pyplot(plt)

st.subheader(f"Rata-rata Polusi pada {end_date.date()}")

hourly_data = create_hourly_data_df(filtered_df)

plt.figure(figsize=(10, 5))
plt.plot(hourly_data["Hour"], hourly_data["PM2.5"], marker='o', label='PM2.5', color='blue')
plt.plot(hourly_data["Hour"], hourly_data["PM10"], marker='s', label='PM10', color='red')

plt.xlabel("Jam")
plt.ylabel("Rata-rata Polusi")
plt.title(f"Rata-rata Polusi pada {end_date.date()}")
plt.xticks(range(24))
plt.legend()

st.pyplot(plt)