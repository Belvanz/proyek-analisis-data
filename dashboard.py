import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# **Pindahkan set_page_config() ke bagian paling atas**
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/Belvanz/proyek-analisis-data/refs/heads/main/Bike-sharing-dataset/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/Belvanz/proyek-analisis-data/refs/heads/main/Bike-sharing-dataset/hour.csv")
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])  
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Sidebar: Filter Rentang Tanggal
st.sidebar.header("Filter Data")
min_date, max_date = day_df["dteday"].min(), day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Filter Data Berdasarkan Rentang Tanggal
filtered_day_df = day_df[(day_df["dteday"] >= pd.Timestamp(start_date)) & 
                         (day_df["dteday"] <= pd.Timestamp(end_date))]

# Header Dashboard
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis pola penyewaan sepeda berdasarkan dataset bike sharing.")

# Pola Penyewaan Sepeda Berdasarkan Musim
st.subheader("📊 Total Penyewaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=filtered_day_df["season"], y=filtered_day_df["cnt"], estimator=sum, palette="coolwarm", ax=ax)
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Pola Penyewaan Sepeda Berdasarkan Jam dalam Sehari
st.subheader("🕒 Pola Penyewaan Sepeda Berdasarkan Jam dalam Sehari")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hour_df["hr"], y=hour_df["cnt"], estimator="mean", ci=None, marker="o", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Pola Penyewaan Sepeda Berdasarkan Jam")
ax.grid(True)
st.pyplot(fig)

# Tren Penyewaan Sepeda dalam Setahun
st.subheader("📅 Tren Penyewaan Sepeda dalam Setahun")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="mnth", y="cnt", data=filtered_day_df, estimator="mean", ci=None, marker="o", color="blue", ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda dalam Setahun")
ax.grid(True)
st.pyplot(fig)

# Hubungan Suhu dengan Penyewaan Sepeda
st.subheader("🌡️ Hubungan Suhu dengan Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x="temp", y="cnt", data=filtered_day_df, alpha=0.5, color="red", ax=ax)
ax.set_xlabel("Suhu (Normalized)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Hubungan Suhu dan Penyewaan Sepeda")
ax.grid(True)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("📌 **Dashboard ini dibuat untuk menganalisis pola penggunaan sepeda berdasarkan musim, waktu, dan cuaca.**")
