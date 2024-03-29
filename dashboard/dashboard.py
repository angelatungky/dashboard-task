import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Read the data
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

min_date = pd.to_datetime(day_df["dteday"].min())  # Convert min_date to datetime object
max_date = pd.to_datetime(day_df["dteday"].max())  # Convert max_date to datetime object

with st.sidebar:
    st.image("https://raw.githubusercontent.com/angelatungky/dashboard-task/main/dashboard/bicycle.jpg", width=300)
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_hour_df = hour_df[(pd.to_datetime(hour_df['dteday']).dt.date >= start_date) & (pd.to_datetime(hour_df['dteday']).dt.date <= end_date)]
filtered_day_df = day_df[(pd.to_datetime(day_df['dteday']).dt.date >= start_date) & (pd.to_datetime(day_df['dteday']).dt.date <= end_date)]

st.header("Bike Rental Service Dashboard")
# Function to plot the bar chart
st.subheader("Bike Rental based on Weather Condition")
def plot_weather_bar_chart():
    # Group by weather situation and sum casual and registered users
    weather_grouped = filtered_hour_df.groupby('weathersit')[['casual', 'registered']].sum()

    # Determine the dominant weather situation
    dominant_weather = weather_grouped['registered'].idxmax()

    # Get the unique weather situations and their counts
    weather_situations = weather_grouped.index
    counts = weather_grouped.sum(axis=1)

    # Create a new Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot registered users
    ax.bar([str(ws) for ws in weather_situations], weather_grouped['registered'], color='tab:blue' if dominant_weather == 'registered' else 'grey', label='Registered')

    # Plot casual users
    ax.bar([str(ws) for ws in weather_situations], weather_grouped['casual'], color='grey' if dominant_weather == 'casual' else 'tab:blue', alpha=0.5, label='Casual')

    ax.set_title("Number of Bike Rentals by Weather Situation")
    ax.set_ylabel("Number of Rentals")
    ax.set_xlabel("Weather Situation")

    # Modify legend colors
    ax.legend(facecolor='lightgrey', edgecolor='black')

    # Show the plot
    st.pyplot(fig)


# Function to plot the pie chart
def plot_season_pie_chart():
    # Get counts of bike rentals for each season
    season_counts = filtered_day_df.groupby('season')['cnt'].sum()

    # Define labels for seasons
    season_labels = ['Spring', 'Summer', 'Fall', 'Winter']

    # Ensure that the length of season_labels matches the number of unique seasons in the data
    unique_seasons = filtered_day_df['season'].unique()
    season_labels = [season_labels[i - 1] for i in unique_seasons]

    # Define colors for each season
    colors = ['#8B4513', '#FFF8DC', '#93C572', '#E67F0D']

    # Determine the index of the largest season
    largest_season_index = season_counts.idxmax()

    # Create explode values with 0.1 for the largest season and 0 for others
    explode = [0.1 if season == largest_season_index else 0 for season in season_counts.index]

    # Create a new Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot the pie chart
    ax.pie(
        x=season_counts,
        labels=season_labels,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode
    )
    ax.set_title("Bike Rental Demand Across Different Seasons")

    # Show the plot
    st.pyplot(fig)

# Plot the charts based on the selected time range
plot_weather_bar_chart()
st.subheader("Bike Rental based on Season")
plot_season_pie_chart()

# Ensure 'dteday' column is in datetime format
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

rfm_df = hour_df.groupby(by="hr", as_index=False).agg({
    "dteday": "max",  # mengambil tanggal penyewaan sepeda terakhir
    "instant": "nunique",  # menghitung jumlah penyewaan sepeda
    "cnt": "sum"  # menghitung jumlah revenue yang dihasilkan
})

rfm_df.columns = ["hr", "last_order_date", "frequency", "monetary"]

# menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm_df["last_order_date"] = rfm_df["last_order_date"].dt.date
recent_date = hour_df["dteday"].dt.date.max()
rfm_df["recency"] = rfm_df["last_order_date"].apply(lambda x: (recent_date - x).days)

rfm_df.drop("last_order_date", axis=1, inplace=True)

# Define a single color for the RFM bar chart analysis
rfm_color = '#ABEBC6'

# Sort rfm_df by recency, frequency, and monetary and select top 5
rfm_df_recency = rfm_df.sort_values(by="recency", ascending=True).head(5)
rfm_df_frequency = rfm_df.sort_values(by="frequency", ascending=False).head(5)
rfm_df_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)

# Create subplots for RFM analysis
st.subheader("RFM Analysis: Best Rental Hours")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

# Plot by Recency
sns.barplot(y="recency", x="hr", data=rfm_df_recency, color=rfm_color, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)

# Plot by Frequency
sns.barplot(y="frequency", x="hr", data=rfm_df_frequency, color=rfm_color, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

# Plot by Monetary
sns.barplot(y="monetary", x="hr", data=rfm_df_monetary, color=rfm_color, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

# Set suptitle
plt.suptitle("Best Rental Hours Based on RFM Parameters", fontsize=20)

# Show the plot
st.pyplot(fig)
