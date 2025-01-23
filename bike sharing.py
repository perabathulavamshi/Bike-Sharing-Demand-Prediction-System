import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
 
# Load the dataset
data = pd.read_csv(r"C:\Users\ADMIN\Downloads\NYC-BikeShare-2015-2017-combined.csv")
 
# Data Preparation
data['Trip_Duration_in_min'] = data['Trip Duration'] / 60  # Convert trip duration to minutes
data['Gender'] = data['Gender'].replace({1: 'Male', 2: 'Female', 0: 'Unknown'})  # Map gender values
 
# EDA: Summary Statistics
total_trips = len(data)
unique_bikes = data['Bike ID'].nunique()
average_trip_duration = data['Trip_Duration_in_min'].mean()
most_popular_start_station = data['Start Station Name'].mode()[0]
most_popular_end_station = data['End Station Name'].mode()[0]
total_customers = data[data['User Type'] == 'Customer'].shape[0]
total_subscribers = data[data['User Type'] == 'Subscriber'].shape[0]
 
# Aggregated Insights
average_trip_duration_by_user_type = data.groupby('User Type')['Trip_Duration_in_min'].mean()
trips_by_hour = pd.to_datetime(data['Start Time']).dt.hour.value_counts().sort_index()
trips_by_gender = data['Gender'].value_counts().reset_index()
trips_by_gender.columns = ['Gender', 'Count']  # Rename for consistency
 
# Visualization: Trips by Start Station
station_trip_counts = data['Start Station Name'].value_counts().reset_index()
station_trip_counts.columns = ['Station', 'Trip Count']
 
# Visualization: Trip Durations
trip_duration_hist = px.histogram(
    data,
    x='Trip_Duration_in_min',
    nbins=50,
    title="Distribution of Trip Durations (minutes)"
)
 
# Visualization: User Type Distribution
user_type_pie = px.pie(
    data,
    names='User Type',
    title="User Type Distribution"
)
 
# Visualization: Trips by Hour of Day
trips_by_hour_bar = px.bar(
    x=trips_by_hour.index,
    y=trips_by_hour.values,
    labels={'x': 'Hour of Day', 'y': 'Number of Trips'},
    title="Trips by Hour of Day"
)
 
# Visualization: Gender Distribution
gender_bar = px.bar(
    trips_by_gender,
    x='Gender',
    y='Count',
    labels={'Gender': 'Gender', 'Count': 'Number of Trips'},
    title="Trips by Gender"
)
 
# Create the Dash app
app = dash.Dash(__name__)
 
app.layout = html.Div([
    html.H1("Bike Sharing Dashboard"),
 
    # EDA Section
    html.H2("Exploratory Data Analysis"),
    html.Div([
        html.P(f"Total Trips: {total_trips}"),
        html.P(f"Unique Bikes: {unique_bikes}"),
        html.P(f"Average Trip Duration (minutes): {average_trip_duration:.2f}"),
        html.P(f"Most Popular Start Station: {most_popular_start_station}"),
        html.P(f"Most Popular End Station: {most_popular_end_station}"),
        html.P(f"Total Customers: {total_customers}"),
        html.P(f"Total Subscribers: {total_subscribers}"),
        html.H3("Average Trip Duration by User Type:"),
        html.Ul([html.Li(f"{user_type}: {duration:.2f} minutes") 
                 for user_type, duration in average_trip_duration_by_user_type.items()])
    ]),
 
    # Visualizations Section
    html.H2("Visualizations"),
    dcc.Graph(
        figure=px.bar(
            station_trip_counts,
            x='Station',
            y='Trip Count',
            title="Trips by Start Station"
        )
    ),
    dcc.Graph(figure=trip_duration_hist),
    dcc.Graph(figure=user_type_pie),
    dcc.Graph(figure=trips_by_hour_bar),
    dcc.Graph(figure=gender_bar)
])
 
if __name__ == "__main__":
    app.run_server(debug=True)