import streamlit as st

def overall_standings_page(df):
    st.header("Overall Standings")

    overall_standings = df.groupby('Player')['Points'].sum().reset_index()
    overall_standings = overall_standings.sort_values(by='Points', ascending=False)

    st.dataframe(overall_standings)