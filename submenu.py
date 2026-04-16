import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("📺 MENU")
st.sidebar.divider()

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "Home"

with st.sidebar.expander("⏳ Monitoring", expanded=True):
    if st.button("Overview", key="mon1", use_container_width=True):
        st.session_state.page = "Monitoring - Overview"
    if st.button("Sensor 1", key="mon2", use_container_width=True):
        st.session_state.page = "Monitoring - Sensor 1"
    if st.button("Sensor 2", key="mon3", use_container_width=True):
        st.session_state.page = "Monitoring - Sensor 2"

with st.sidebar.expander("📈 Chart", expanded=False):
    if st.button("Overview", key="chart1", use_container_width=True):
        st.session_state.page = "Chart - Overview"
    if st.button("RPM", key="chart2", use_container_width=True):
        st.session_state.page = "Chart - RPM"
    if st.button("Temperature", key="chart3", use_container_width=True):
        st.session_state.page = "Chart - Temperature"

if st.sidebar.button("📖 ReadMe", use_container_width=True):
    st.session_state.page = "ReadMe"

if st.sidebar.button("🗺️ Maps", use_container_width=True):
    st.session_state.page = "Maps"

if st.sidebar.button("ℹ️ About", use_container_width=True):
    st.session_state.page = "About"

st.title(st.session_state.page)

if st.session_state.page == "Home":
    st.write("Ini halaman Home")
elif st.session_state.page == "Monitoring - Overview":
    st.write("Ini halaman Monitoring Overview")
elif st.session_state.page == "Monitoring - Sensor 1":
    st.write("Ini halaman Monitoring Sensor 1")
elif st.session_state.page == "Monitoring - Sensor 2":
    st.write("Ini halaman Monitoring Sensor 2")
elif st.session_state.page == "Chart - Overview":
    st.write("Ini halaman Chart Overview")
elif st.session_state.page == "Chart - RPM":
    st.line_chart({"RPM": [1200, 1300, 1280, 1450]})
elif st.session_state.page == "Chart - Temperature":
    st.line_chart({"Temp": [70, 71, 73, 72]})
elif st.session_state.page == "ReadMe":
    st.write("Ini halaman ReadMe")
elif st.session_state.page == "Maps":
    st.write("Ini halaman Maps")
elif st.session_state.page == "About":
    st.write("Ini halaman About")
