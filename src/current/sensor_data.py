import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data
def fetch_station_sensors(station_id):
    url = f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}"
    response = requests.get(url)

    if response.status_code == 200:
        sensors = response.json()
    else:
        sensors = []

    return sensors

@st.cache_data
def fetch_sensor_measurements(sensor_id):
	url = f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}"
	response = requests.get(url)

	if response.status_code == 200:
		measurements = response.json()
	else:
		measurements = []

	return measurements

station_id = st.session_state.selected_station_id
station_name = st.session_state.selected_station_name

if not station_id:
    st.warning("Nie wybrano żadnej stacji.")
else:
    sensors = fetch_station_sensors(station_id)
    sensor_results = []
    for sensor in sensors:
        sensor_data = fetch_sensor_measurements(sensor["id"])
        print(sensor_data)
        if sensor_data:
            if sensor_data["values"][0]["value"]:
                latest_measurement = sensor_data["values"][0]
            else:
                latest_measurement = sensor_data["values"][1]
            sensor_results.append({
                "Sensor": sensor["param"]["paramName"],
                "ID Sensora": sensor["id"],
                "Data": latest_measurement["date"],
                "Wartość": latest_measurement["value"]
            })

    results_df = pd.DataFrame(sensor_results)
    st.write(f"### Najnowsze dane z sensorów na stacji {station_id}. {station_name}")
    gb_sensors = GridOptionsBuilder.from_dataframe(results_df)
    gb_sensors.configure_selection("single")
    gb_sensors.configure_auto_height(autoHeight=True)

    gb_sensors.configure_columns(["ID Sensora"], hide=True)

    grid_options_sensors = gb_sensors.build()
    grid_response_sensors = AgGrid(
        results_df,
        gridOptions=grid_options_sensors,
        fit_columns_on_grid_load=True,
    )
    selected_sensor_row = pd.DataFrame(grid_response_sensors.get("selected_rows", []))
    if not selected_sensor_row.empty:
        selected_sensor = selected_sensor_row.iloc[0]
        st.session_state.selected_sensor_id = selected_sensor["ID Sensora"]
        st.session_state.selected_sensor_attribute = selected_sensor["Sensor"]
        st.switch_page("current/plot.py")