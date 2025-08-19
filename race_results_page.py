import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_extras.stylable_container import stylable_container

def race_results_page(df):
    st.header("SPEED Travel Pic Games")

    # Get unique locations for the selector
    locations = df['Location'].unique().tolist()

    # Add a selector for the race location
    selected_location = st.selectbox("Select Round", locations)

    # Filter the DataFrame based on the selected location
    filtered_df = df[df['Location'] == selected_location].sort_values(by='Points', ascending=False)

    # Display podium
    st.subheader("Podium")

    img = 'https://visitesaopaulo.com/wp-content/uploads/2021/01/AS00106-Ponte-Estaiada.jpg'
    if (selected_location == 'LOC 1'): 
        img = 'https://www.shutterstock.com/image-photo/brasilia-brazil-november-19-view-600nw-360540041.jpg'

    if len(filtered_df) >= 3:
        col1_1, col1_2, col1_3 = st.columns(3, vertical_alignment='bottom')
        with stylable_container(
            key="right_aligned_column",
            css_styles="""
                div[data-testid="stMetric"] {
                text-align: center;
            }
            """
        ):
            with col1_1: 
                col2nd_1, col2nd_2 = st.columns([0.15, 0.85], vertical_alignment='bottom')
                with col2nd_2:
                    st.image(img)
                    st.metric("2nd Place", filtered_df.iloc[1]['Player'], f"{filtered_df.iloc[1]['Points']} points")
            with col1_2:
                    st.image(img)
                    st.metric("1st Place", filtered_df.iloc[0]['Player'], f"{filtered_df.iloc[0]['Points']} points")
            with col1_3:
                col2nd_1, col2nd_2 = st.columns([0.85, 0.15], vertical_alignment='bottom')
                with col2nd_1:
                    st.image(img)
                    st.metric("3rd Place", filtered_df.iloc[2]['Player'], f"{filtered_df.iloc[2]['Points']} points")
    elif len(filtered_df) == 2:
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                st.metric("1st Place", filtered_df.iloc[0]['Player'], f"{filtered_df.iloc[0]['Points']} points")
            with col1_2:
                st.metric("2nd Place", filtered_df.iloc[1]['Player'], f"{filtered_df.iloc[1]['Points']} points")
    elif len(filtered_df) == 1:
        st.metric("1st Place", filtered_df.iloc[0]['Player'], f"{filtered_df.iloc[0]['Points']} points")
    else:
        st.write("No results for this race yet.")


## MAP   
    st.subheader("Player Locations")
    map_data = filtered_df[['Player Lat', 'Player Lon', 'Player', 'Round Lat', 'Round Lon', 'Location', 'Distance']].rename(columns={'Player Lat': 'lat', 'Player Lon': 'lon', 'Round Lat': 'round_lat', 'Round Lon': 'round_lon'})

    map_data['Player_Distance_Text'] = map_data.apply(lambda row: f"{row['Player']} ({row['Distance']:.2f} km)", axis=1)


    race_location_data = map_data[['round_lat', 'round_lon', 'Location']].drop_duplicates().rename(columns={'round_lat': 'lat', 'round_lon': 'lon', 'Location': 'Player'})
    map_data = pd.concat([map_data, race_location_data], ignore_index=True)

    print(selected_location)
    print(map_data)
    print('FILTRADA')
    print(map_data[map_data['Player'] != selected_location])

    players_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data[map_data['Player'] != selected_location], # Filter out the race location row
        get_position=['lon', 'lat'],
        get_color='[200, 30, 0, 160]',
        get_radius=10, # Set radius in pixels
        radius_units='pixels', # Use pixel units for radius
        pickable=True,
    )

    location_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data[map_data['Player'] == selected_location], # Filter out the race location row
        get_position=['lon', 'lat'],
        get_color='[0, 255, 0, 255]',
        get_radius=10, # Set radius in pixels
        radius_units='pixels', # Use pixel units for radius
        pickable=True,
    )

    player_distance_layer = pdk.Layer(
        "TextLayer",
        data=map_data[map_data['Player'] != map_data['Location']], # Filter out the race location row
        get_position=['lon', 'lat'],
        get_text="Player_Distance_Text", # Use the pre-formatted text column
        get_color=[0, 0, 0, 255],
        get_size=15, # Increased text size
        get_alignment_baseline="'bottom'",
        get_pixel_offset=[0, -20], # Offset text to be above the icon
    )

    view_state = pdk.ViewState(latitude=map_data["lat"].mean(), longitude=map_data["lon"].mean(), zoom=10, pitch=0)

    r = pdk.Deck(layers=[location_layer, players_layer, player_distance_layer], initial_view_state=view_state, map_style='light')

    st.pydeck_chart(r)


    # Display the filtered DataFrame
    st.subheader("Round Results Table")
    st.dataframe(filtered_df[['Player', 'Distance', 'Points']])
