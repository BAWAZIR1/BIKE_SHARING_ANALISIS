import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv('https://raw.githubusercontent.com/BAWAZIR1/BIKE_SHARING_ANALISIS/refs/heads/master/dashboard/day_data.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/BAWAZIR1/BIKE_SHARING_ANALISIS/refs/heads/master/dashboard/hour_data.csv')

# Main content
st.title('Bike Rental Dashboard')

# Sidebar for user inputs
st.sidebar.header("User Input Features")
view_data = st.sidebar.selectbox("View Data", ['Day Data', 'Hour Data'])

# Display data based on user selection
if view_data == 'Day Data':
    st.write("Displaying Day Data")
    st.dataframe(day_df.head())
elif view_data == 'Hour Data':
    st.write("Displaying Hour Data")
    st.dataframe(hour_df.head())

# Convert 'date_time' to datetime format
day_df['date_time'] = pd.to_datetime(day_df['date_time'])
hour_df['date_time'] = pd.to_datetime(hour_df['date_time'])

# Mapping season names
season_mapping = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}
day_df['season'] = day_df['season'].map(season_mapping)

# Binning for temperature, humidity, and windspeed
temperature_bins = pd.cut(day_df['temperature'],
                          bins=[0, 0.2, 0.4, 0.6, 0.8, 1],
                          labels=['Sangat Dingin', 'Dingin', 'Sedang', 'Hangat', 'Panas'])
humidity_bins = pd.cut(day_df['humidity'],
                       bins=[0, 0.2, 0.4, 0.6, 0.8, 1],
                       labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])
windspeed_bins = pd.cut(day_df['windspeed'],
                        bins=[0, 0.2, 0.4, 0.6, 0.8, 1],
                        labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])

# Group data by bins
temperature_group = day_df.groupby( temperature_bins, observed=False)['count'].mean()
humidity_group = day_df.groupby(humidity_bins, observed=False)['count'].mean()
windspeed_group = day_df.groupby(windspeed_bins, observed=False)['count'].mean()

# Group data by day type
day_type = day_df['weekday'].apply(lambda x: 'Hari Kerja' if x in [ 1, 2, 3, 4, 5] else 'Akhir Pekan')
day_type_group = day_df.groupby(day_type)['count'].mean()
holiday_group = day_df.groupby('holiday')['count'].mean()
holiday_group.index = ['Hari Biasa', 'Hari Libur']

usage_per_hour_weekdays = hour_df.groupby(['hour', 'weekday'])['count'].sum().reset_index()
usage_per_hour_weekdays.columns = ['Hour', 'Weekday', 'Total_Rentals']
usage_per_hour_weekdays['Weekday'] = usage_per_hour_weekdays['Weekday'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
        3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    })


# Sidebar option to display scatter plots
if st.sidebar.checkbox("Berdasarakan faktor cuaca", value = True):
    st.subheader("Faktor cuaca yang paling berpengaruh terhadap jumlah penyewaan sepeda")

    # Creating the scatter plots
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))

    # Scatter plot for temperature
    sns.scatterplot(x='temperature', y='count',
                    data=day_df, hue='season', ax=axes[0])
    axes[0].set_title('Pengaruh Suhu terhadap Penyewaan Sepeda')
    axes[0].set_xlabel('Suhu')
    axes[0].set_ylabel('Jumlah Penyewaan')

    # Scatter plot for humidity
    sns.scatterplot(x='humidity', y='count', data=day_df,
                    hue='season', ax=axes[1])
    axes[1].set_title('Pengaruh Kelembaban terhadap Penyewaan Sepeda')
    axes[1].set_xlabel('Kelembaban')

    # Scatter plot for windspeed
    sns.scatterplot(x='windspeed', y='count',
                    data=day_df, hue='season', ax=axes[2])
    axes[2].set_title('Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda')
    axes[2].set_xlabel('Kecepatan Angin')

    plt.tight_layout()
    st.pyplot(fig)

# Sidebar options for visualizations
if st.sidebar.checkbox("Permintaan penyewaan sepeda pada hari kerja dan akhir pekan",value = True):
    st.write("Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    fig1, ax1 = plt.subplots()
    day_type_group.plot(kind='bar', color=['#D3D3D3', '#72BCD4'], ax=ax1)
    ax1.set_title("Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    ax1.set_xlabel("Tipe Hari")
    ax1.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig1)

if st.sidebar.checkbox("Permintaan penyewaan sepeda pada hari libur dan hari biasa",value = True):
    st.write("Rata-rata Penyewaan Sepeda: Hari Libur vs Hari Biasa")
    fig2, ax2 = plt.subplots()
    holiday_group.plot(kind='bar', color=['#72BCD4', '#D3D3D3'], ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Sepeda: Hari Libur vs Hari Biasa")
    ax2.set_xlabel("Status Hari")
    ax2.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig2)

# Plot total rentals by hour across weekdays
if st.sidebar.checkbox("Penyewaan Sepeda per Jam dari Senin hingga Minggu",value = True):
    st.write("Penyewaan Sepeda per Jam dari Senin hingga Minggu")
    fig3, ax3 = plt.subplots()
    sns.lineplot(data=usage_per_hour_weekdays, x='Hour',y='Total_Rentals', hue='Weekday', marker='o', ax=ax3)
    ax3.set_title('Penyewaan Sepeda per Jam dari Senin hingga Minggu')
    ax3.set_xlabel('Jam dalam Sehari')
    ax3.set_ylabel('Total Penyewaan')
    st.pyplot(fig3)
# Footer
st.sidebar.info('Data source: Bike Sharing Dataset')
st.sidebar.text('Created by HUZAIR BAWAZIR (HAJER)')