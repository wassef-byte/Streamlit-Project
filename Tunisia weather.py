import requests
import pandas as pd
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Set up your OpenWeatherMap API key and location coordinates
api_key = '####'  # Replace with your OpenWeatherMap API key
latitude = 36.8065  # Latitude of Tunis
longitude = 10.1815  # Longitude of Tunis

# Set the start and end dates for data retrieval
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 1, 10)
dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# List to hold weather data
weather_data = []

# Loop through each date to get data
for date in dates:
    unix_timestamp = int(date.timestamp())  # Convert date to UNIX timestamp
    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine"
    params = {
        'lat': latitude,
        'lon': longitude,
        'dt': unix_timestamp,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract required data and append to list
    for hour_data in data.get('hourly', []):
        weather_data.append({
            'Date': datetime.fromtimestamp(hour_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'City': 'Tunis',
            'Temperature': hour_data.get('temp'),
            'Humidity': hour_data.get('humidity'),
            'Wind Speed': hour_data.get('wind_speed'),
            'Rainfall': hour_data.get('rain', {}).get('1h', 0)  # Rain in last hour, 0 if not available
        })

# Convert list to DataFrame and save to CSV
df = pd.DataFrame(weather_data)
df.to_csv('tunis_weather_data.csv', index=False)
print("Weather data saved to 'tunis_weather_data.csv'")
st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("Generate Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("Waiting on file upload...")