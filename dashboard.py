import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi awal Streamlit
st.set_page_config(page_title="🚲 Bike Sharing Dashboard", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/Belvanz/proyek-analisis-data/refs/heads/main/Bike-sharing-dataset/day.csv")  
    hour_df = pd.read_csv("https://raw.githubusercontent.com/Belvanz/proyek-analisis-data/refs/heads/main/Bike-sharing-dataset/hour.csv")
    
    # Konversi tanggal
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    
    return day_df, hour_df

# Muat data
day_df, hour_df = load_data()

# Sidebar: Filter Interaktif
st.sidebar.header("🎚️ Filter Data")
min_date, max_date = day_df["dteday"].min(), day_df["dteday"].max()

# Filter Rentang Tanggal
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Filter Berdasarkan Musim
season_options = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
selected_season = st.sidebar.multiselect(
    "Pilih Musim", options=season_options.keys(), default=list(season_options.keys()), format_func=lambda x: season_options[x]
)

# Terapkan Filter
filtered_day_df = day_df[
    (day_df["dteday"] >= pd.Timestamp(start_date)) & 
    (day_df["dteday"] <= pd.Timestamp(end_date)) &
    (day_df["season"].isin(selected_season))
]

# Dashboard: Tampilan Metrik Utama
st.title("🚲 Bike Sharing Dashboard")
st.markdown("📍 **Analisis pola penyewaan sepeda berdasarkan dataset bike sharing.**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Penyewaan", value=int(filtered_day_df["cnt"].sum()))

with col2:
    st.metric("📈 Rata-rata Penyewaan Harian", value=int(filtered_day_df["cnt"].mean()))

with col3:
    st.metric("🏆 Penyewaan Tertinggi", value=int(filtered_day_df["cnt"].max()))

with col4:
    st.metric("🔻 Penyewaan Terendah", value=int(filtered_day_df["cnt"].min()))

# Total Penyewaan Sepeda Berdasarkan Musim
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

# Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan
st.subheader("📅 Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=filtered_day_df["workingday"], y=filtered_day_df["cnt"], estimator=sum, palette="Set2", ax=ax)
ax.set_xticklabels(["Akhir Pekan", "Hari Kerja"])
ax.set_xlabel("Tipe Hari")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan")
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
