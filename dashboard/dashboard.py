import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

gabungan = pd.read_csv('main_data.csv')

gabungan['waktu'] = pd.to_datetime(gabungan[['year', 'month', 'day', 'hour']])
gabungan['year'] = gabungan['waktu'].dt.year

def musim(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

gabungan['season'] = gabungan['waktu'].dt.month.apply(musim)

st.sidebar.title('Dashboard Interaktif Kualitas Udara')
st.sidebar.write("Gunakan kontrol di bawah untuk memfilter data:")
station = st.sidebar.selectbox('Pilih Stasiun:', ['Guanyuan', 'Gucheng'])
parameter = st.sidebar.selectbox('Pilih Parameter:', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN'])
visual_type = st.sidebar.selectbox('Pilih Tipe Visualisasi:', ['Rata-rata Tahunan', 'Rata-rata Musiman', 'Variasi Bulanan', 'Scatterplot'])

df_filtered = gabungan[gabungan['station'] == station]

if visual_type == 'Rata-rata Tahunan':
    st.subheader(f'Rata-rata Tahunan {parameter} di Stasiun {station}')
    df_tahunan = df_filtered.groupby('year')[parameter].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(x='year', y=parameter, data=df_tahunan, ax=ax)
    plt.title(f'Rata-rata Tahunan {parameter} di Stasiun {station}')
    plt.xlabel('Tahun')
    plt.ylabel(f'Rata-rata {parameter}')
    st.pyplot(fig)

elif visual_type == 'Rata-rata Musiman':
    st.subheader(f'Rata-rata {parameter} Berdasarkan Musim - {station}')
    df_season = df_filtered.groupby('season')[parameter].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(x='season', y=parameter, data=df_season, ax=ax)
    plt.title(f'Rata-rata {parameter} Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel(f'Rata-rata {parameter}')
    st.pyplot(fig)

elif visual_type == 'Variasi Bulanan':
    st.subheader(f'Variasi Bulanan {parameter} di Stasiun {station}')
    df_filtered['bulan_dan_tahun'] = df_filtered['waktu'].dt.to_period('M')
    df_bulanan = df_filtered.groupby('bulan_dan_tahun')[parameter].mean().reset_index()
    df_bulanan['bulan_dan_tahun'] = df_bulanan['bulan_dan_tahun'].astype(str)

    fig, ax = plt.subplots()
    sns.lineplot(x='bulan_dan_tahun', y=parameter, data=df_bulanan, marker='o', ax=ax)
    plt.title(f'Variasi Bulanan {parameter} di Stasiun {station}')
    plt.xlabel('Bulan-Tahun')
    plt.ylabel(f'Rata-rata {parameter}')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif visual_type == 'Scatterplot':
    if parameter == 'PM2.5':
        st.subheader(f'Korelasi antara {parameter} dan Temperatur di Stasiun {station}')
        fig, ax = plt.subplots()
        sns.scatterplot(x='TEMP', y=parameter, data=df_filtered, ax=ax)
        plt.title(f'Hubungan antara Temperatur dan {parameter} di Stasiun {station}')
        plt.xlabel('Temperatur (°C)')
        plt.ylabel(f'{parameter} (Konsentrasi)')
        st.pyplot(fig)
    elif parameter == 'PM10':
        st.subheader(f'Korelasi antara {parameter} dan Tekanan Udara di Stasiun {station}')
        fig, ax = plt.subplots()
        sns.scatterplot(x='PRES', y=parameter, data=df_filtered, ax=ax)
        plt.title(f'Hubungan antara Tekanan Udara dan {parameter} di Stasiun {station}')
        plt.xlabel('Tekanan Udara (hPa)')
        plt.ylabel(f'{parameter} (Konsentrasi)')
        st.pyplot(fig)
