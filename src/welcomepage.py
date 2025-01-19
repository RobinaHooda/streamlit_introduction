import streamlit as st

st.session_state.selected_station_id = None
st.session_state.selected_station_name = None
st.session_state.selected_sensor_id = None
st.session_state.selected_sensor_attribute = None

st.markdown(
	"""
	# Witaj w AirQualityApp!
	AirQuality to system informatyczny do przechowywania, przetwarzania i wizualizacji danych o jakości powietrza na podstawie publicznie dostępnego API (https://powietrze.gios.gov.pl/pjp/content/api). System ma wspierać analizę danych historycznych, ich agregację oraz umożliwiać interaktywne wizualizacje w przystępnej formie dla użytkowników.
	""")

st.sidebar.success("Wybierz zakładkę z powyższych")