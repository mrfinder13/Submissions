import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set style for seaborn
sns.set(style='dark')

# Load data
all_df = pd.read_csv("all_data.csv")

# Mengubah nama kolom
all_df.rename(columns={
    'dteday': 'dateday',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mapping data untuk kemudahan pembacaan
mappings = {
    'month': {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
    'season': {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'},
    'weekday': {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'},
    'weather_cond': {1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy',
                     3: 'Light Snow/Rain', 4: 'Severe Weather'}
}
for col, mapping in mappings.items():
    all_df[col] = all_df[col].map(mapping)

# Mengubah tipe data
all_df['dateday'] = pd.to_datetime(all_df['dateday'])

# Daftar kolom yang akan diubah ke kategori
categorical_cols = ['season', 'month', 'holiday', 'weekday', 'workingday', 'weather_cond']
for col in categorical_cols:
    all_df[col] = all_df[col].astype('category')

# Streamlit title
st.title("Bike Rental Data Analysis")

# Sidebar for user interaction
st.sidebar.header("Exploratory Data Analysis Options")
option = st.sidebar.selectbox(
    "Pilih Visualisasi",
    ["Rata-rata Penyewaan Sepeda Berdasarkan Hari", 
     "Penyewaan Sepeda oleh Pengguna Kasual vs Terdaftar",
     "Penyewaan Sepeda Berdasarkan Kondisi Cuaca", 
     "Pengaruh Suhu terhadap Penyewaan Sepeda",
     "Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda"]
)

# Visualizations and Analysis
if option == "Rata-rata Penyewaan Sepeda Berdasarkan Hari":
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
    grouped_data = all_df.groupby('weekday').agg({'count': 'mean'}).reset_index()
    plt.figure(figsize=(10,6))
    sns.barplot(x='weekday', y='count', data=grouped_data)
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot()

elif option == "Penyewaan Sepeda oleh Pengguna Kasual vs Terdaftar":
    st.subheader("Penyewaan Sepeda oleh Pengguna Kasual vs Terdaftar")
    grouped_data = all_df.groupby('weekday').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()
    
    plt.figure(figsize=(10,6))
    sns.barplot(x='weekday', y='casual', data=grouped_data, label='Casual', color='skyblue')
    sns.barplot(x='weekday', y='registered', data=grouped_data, label='Registered', color='salmon')
    plt.title('Rata-rata Penyewaan Sepeda oleh Pengguna Kasual dan Terdaftar per Hari')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    plt.legend(title='Jenis Pengguna')
    st.pyplot()

elif option == "Penyewaan Sepeda Berdasarkan Kondisi Cuaca":
    st.subheader("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    weather_df = all_df.groupby('weather_cond').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()
    
    # Kasual
    plt.figure(figsize=(10,6))
    sns.barplot(x='weather_cond', y='casual', data=weather_df)
    plt.title('Rata-rata Penyewaan Sepeda oleh Pengguna Kasual berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Penyewaan Sepeda Kasual')
    st.pyplot()
    
    # Terdaftar
    plt.figure(figsize=(10,6))
    sns.barplot(x='weather_cond', y='registered', data=weather_df)
    plt.title('Rata-rata Penyewaan Sepeda oleh Pengguna Terdaftar berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Penyewaan Sepeda Terdaftar')
    st.pyplot()

elif option == "Pengaruh Suhu terhadap Penyewaan Sepeda":
    st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='temp', y='casual', data=all_df, label='Casual Users', color='blue')
    sns.scatterplot(x='temp', y='registered', data=all_df, label='Registered Users', color='orange')
    plt.title('Pengaruh Suhu terhadap Penyewaan Sepeda oleh Pengguna Kasual dan Terdaftar')
    plt.xlabel('Suhu (Temp)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend()
    st.pyplot()

elif option == "Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda":
    st.subheader("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='windspeed', y='casual', data=all_df, label='Casual Users', color='blue')
    sns.scatterplot(x='windspeed', y='registered', data=all_df, label='Registered Users', color='orange')
    plt.title('Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda oleh Pengguna Kasual dan Terdaftar')
    plt.xlabel('Kecepatan Angin (Windspeed)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend()
    st.pyplot()
