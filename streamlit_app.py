import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import pydeck as pdk

# Import the page functions
from race_results_page import race_results_page
from overall_standings_page import overall_standings_page

st.set_page_config(
    page_title="SPEED Travel Pic Games",
    layout="wide"
)

data = [
    {
        "location": "LOC 1",
        "coordinates": "-15.791277810112314, -47.893439364157246",
        "result": [{
            "player": "Player A",
            "coordinates": "-15.802116448481316, -47.998390221864",
            "points": 25,
        },{
            "player": "Player B",
            "coordinates": "-15.816271949268668, -48.157440178909525",
            "points": 20,
        },{
            "player": "Player C",
            "coordinates": "-15.921692671792977, -47.76694973960758",
            "points": 18,
        }]
    },
    {
        "location": "LOC 2",
        "coordinates": "-23.550520, -46.633309",
        "result": [{
            "player": "Player B",
            "coordinates": "-23.560000, -46.640000",
            "points": 25,
        },{
            "player": "Player A",
            "coordinates": "-23.570000, -46.650000",
            "points": 20,
        },{
            "player": "Player C",
            "coordinates": "-23.580000, -46.660000",
            "points": 15,
        }]
    },
    {
        "location": "LOC 3",
        "coordinates": "34.052235, -118.243683",
        "result": [{
            "player": "Player C",
            "coordinates": "34.060000, -118.250000",
            "points": 25,
        },{
            "player": "Player B",
            "coordinates": "34.070000, -118.260000",
            "points": 20,
        },{
            "player": "Player A",
            "coordinates": "34.080000, -118.270000",
            "points": 18,
        }]
    }
]

flattened_data = []
for round in data:
    location = round['location']
    round_coordinates_str = round['coordinates'].split(',')
    round_lat = float(round_coordinates_str[0])
    round_lon = float(round_coordinates_str[1])
    round_coords = (round_lat, round_lon) # Tuple for geodesic

    for result in round['result']:
        player_coordinates_str = result['coordinates'].split(',')
        player_lat = float(player_coordinates_str[0])
        player_lon = float(player_coordinates_str[1])
        player_coords = (player_lat, player_lon) # Tuple for geodesic

        # Calculate distance using geodesic
        distance = geodesic(round_coords, player_coords).km

        flattened_data.append({
            'Location': location,
            'Round Lat': round_lat,
            'Round Lon': round_lon,
            'Player': result['player'],
            'Player Lat': player_lat,
            'Player Lon': player_lon,
            'Points': result['points'],
            'Distance': distance
        })

df_results = pd.DataFrame(flattened_data)


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Round Results", "Overall Standings"])

# Call the appropriate page function based on the selection
if page == "Round Results":
    race_results_page(df_results)
elif page == "Overall Standings":
    overall_standings_page(df_results)