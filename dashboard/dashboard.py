
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load dataset
main_data = pd.read_csv("D:/Bangkit/Proyek AKhir/Bike-sharing-dataset/main_data.csv", sep=";")
main_data['dteday'] = pd.to_datetime(main_data['dteday'], format="%d/%m/%Y")



# Menentukan rentang tanggal yang sesuai dengan DataFrame
min_date = main_data['dteday'].min()
max_date = main_data['dteday'].max()

# Konfigurasi date input
with st.sidebar:
    st.image("https://i.pinimg.com/originals/ca/65/54/ca655453eb79fe8db19601dfcf53ed95.jpg")
    selected_date = st.sidebar.date_input('Pilih Tanggal', min_value=min_date, max_value=max_date, value=min_date)

# Title
st.markdown("<h1 style='text-align: center;'>Visualisasi Data Bike Share</h1>", unsafe_allow_html=True)

# Total Users Info
total_users_2011 = main_data[main_data['yr'] == 0]['cnt'].sum()
total_users_2012 = main_data[main_data['yr'] == 1]['cnt'].sum()

selected_month = selected_date.month
selected_year = selected_date.year
# Memecah total users menjadi dua kolom
col1, col2 = st.columns(2)
with col1:
    st.write('## Total Tahun 2011')
    st.write('#',total_users_2011)

with col2:
    st.write('## Total Tahun 2012')
    st.write('#',total_users_2012)

# Total peminjaman sepeda per jam sesuai dengan hari inputan user
selected_day = selected_date.day

# Filter data untuk tanggal yang dipilih
selected_date_data = main_data[(main_data['dteday'].dt.day == selected_day) & (main_data['dteday'].dt.month == selected_month) & (main_data['dteday'].dt.year == selected_year)]

# Menghitung total peminjaman sepeda per jam
total_rentals_per_hour = selected_date_data.groupby(selected_date_data['hr'])['cnt'].sum()

# Buat line chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(total_rentals_per_hour.index, total_rentals_per_hour.values, marker='o', color='purple', linestyle='-')

# Tambahkan judul dan label sumbu
ax.set_title(f'Total Number of Bike Rentals per Hour for {selected_date.strftime("%d %B %Y")}')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Number of Bike Rentals')

# Konfigurasi sumbu x untuk menampilkan label jam yang sesuai
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: int(x)))

# Tampilkan grid
ax.grid(True)

# Tampilkan line chart
st.pyplot(fig)

col3, col4 = st.columns(2)
with col3:
     # Total peminjaman sepeda pada hari libur dan hari kerja
     total_rentals_holiday = main_data[(main_data['holiday'] == 1) & (main_data['dteday'].dt.month == selected_month) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
     total_rentals_workday = main_data[(main_data['holiday'] == 0) & (main_data['dteday'].dt.month == selected_month) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
     # Buat diagram batang
     fig, ax = plt.subplots(figsize=(8, 6))
     ax.bar(['Holiday', 'Workday'], [total_rentals_holiday / 1000, total_rentals_workday / 1000], color=['blue', 'red'])
     # Tambahkan judul dan label sumbu
     ax.set_title(f'Total Number of Bike Rentals on Holiday and Workday for {selected_date.strftime("%B %Y")}')
     ax.set_xlabel('Day')
     ax.set_ylabel('Total Number of Bike Rentals (thousands)')
     # Tampilkan diagram batang
     st.pyplot(fig)
with col4:
    # Total peminjaman berdasarkan musim
    total_rentals_spring = main_data[(main_data['season'] == 1) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
    total_rentals_summer = main_data[(main_data['season'] == 2) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
    total_rentals_fall = main_data[(main_data['season'] == 3) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
    total_rentals_winter = main_data[(main_data['season'] == 4) & (main_data['dteday'].dt.year == selected_year)]['cnt'].sum()
    # Buat diagram batang
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Spring', 'Summer', 'Fall', 'Winter'], [total_rentals_spring / 1000, total_rentals_summer / 1000, total_rentals_fall / 1000, total_rentals_winter / 1000], color=['green', 'yellow', 'orange', 'blue'])
    # Tambahkan judul dan label sumbu
    ax.set_title(f'Total Number of Bike Rentals by Season for {selected_year}')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Number of Bike Rentals (thousands)')
    # Tampilkan diagram batang
    st.pyplot(fig)

# Plot
total_casual_2011 = main_data[main_data['yr'] == 0]['casual'].sum()
total_casual_2012 = main_data[main_data['yr'] == 1]['casual'].sum()
total_registered_2011 = main_data[main_data['yr'] == 0]['registered'].sum()
total_registered_2012 = main_data[main_data['yr'] == 1]['registered'].sum()

# Membuat plot
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Plot untuk casual
axes[0].bar(['2011', '2012'], [total_casual_2011 / 1000, total_casual_2012 / 1000], color='skyblue')
axes[0].set_title('Total Casual Users')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Total Users (thousands)')
axes[0].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

# Plot untuk registered
axes[1].bar(['2011', '2012'], [total_registered_2011 / 1000, total_registered_2012 / 1000], color='orange')
axes[1].set_title('Total Registered Users')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Total Users (thousands)')
axes[1].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

plt.tight_layout()
st.pyplot(fig)
