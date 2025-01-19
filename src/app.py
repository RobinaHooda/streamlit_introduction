import streamlit as st

welcome_page = st.Page("welcomepage.py", title="Strona powitalna", icon="👋")
stations_page = st.Page("stations.py", title="Stacje", icon="🗼")
map_page = st.Page("map.py", title="Mapa stacji", icon="🌍")
sensor_data_page = st.Page("current/sensor_data.py", title="Dane z sensorów", icon="📡")
plot_page = st.Page("current/plot.py", title="Wykres najnowszych pomiarów", icon="📈")

pg = st.navigation({"Ogólne": [welcome_page, map_page, stations_page], "Aktualne dane": [sensor_data_page, plot_page]})
pg.run()