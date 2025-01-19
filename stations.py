import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder

url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
response = requests.get(url)

if response.status_code == 200:
    stations = response.json()
else:
    stations = []

station_data = [
    {
        "ID": station["id"],
        "Nazwa Stacji": station["stationName"],
        "Miasto": station["city"]["name"],
        "Ulica": station["addressStreet"],
        "Województwo": station["city"]["commune"]["provinceName"],
        "Powiat": station["city"]["commune"]["districtName"],
        "Gmina": station["city"]["commune"]["communeName"],
        "Szerokość": float(station["gegrLat"]),
        "Długość": float(station["gegrLon"]),
    }
    for station in stations
]

stations_df = pd.DataFrame(station_data)

st.write("### Wszystkie stacje")
search_query = st.text_input("Wyszukaj w stacjach:")
filtered_df = stations_df.copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
    ]
    
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection("single")
for col in filtered_df.columns:
    gb.configure_column(col, autoWidth=True)

gb.configure_columns(["ID", "Nazwa Stacji", "Szerokość", "Długość"], hide=True)

grid_options = gb.build()
grid_response = AgGrid(
    filtered_df,
	gridOptions=grid_options,
)

selected_row = pd.DataFrame(grid_response.get("selected_rows", []))
if not selected_row.empty:
    selected_station = selected_row.iloc[0]
    st.session_state.selected_station_id = selected_station["ID"]
    st.session_state.selected_station_name = selected_station["Nazwa Stacji"]
    st.switch_page("current/sensor_data.py")