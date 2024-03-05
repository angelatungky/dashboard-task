import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


# Read the data
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

min_date = pd.to_datetime(day_df["dteday"].min())  # Convert min_date to datetime object
max_date = pd.to_datetime(day_df["dteday"].max())  # Convert max_date to datetime object

with st.sidebar:
    st.image("data/bicycle.jpg", width=300)
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
