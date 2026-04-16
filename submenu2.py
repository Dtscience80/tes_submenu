import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

# ---------- Fungsi tiap "halaman" ----------
def home_page():
    st.title("🏠 Home")
    st.write("Ini adalah halaman Home.")

def monitoring_overview():
    st.title("⏳ Monitoring - Overview")
    st.write("Ini halaman overview monitoring.")

def monitoring_sensor1():
    st.title("⏳ Monitoring - Sensor 1")
    st.write("Ini halaman monitoring untuk Sensor 1.")

def monitoring_sensor2():
    st.title("⏳ Monitoring - Sensor 2")
    st.write("Ini halaman monitoring untuk Sensor 2.")

def chart_overview():
    st.title("📈 Chart - Overview")
    st.write("Ini halaman overview chart.")

def chart_rpm():
    st.title("📈 Chart - RPM")
    st.line_chart({"RPM": [1200, 1300, 1250, 1450, 1500]})

def chart_temp():
    st.title("📈 Chart - Temperature")
    st.line_chart({"Temperature": [70, 72, 71, 75, 74]})

def readme_page():
    st.title("📖 ReadMe")
    st.write("Isi penjelasan aplikasi.")

def maps_page():
    st.title("🗺️ Maps")
    st.write("Halaman peta.")

def about_page():
    st.title("ℹ️ About")
    st.write("Tentang aplikasi ini.")

# ---------- Sidebar ----------
st.sidebar.title("📺 MENU")
st.sidebar.divider()

main_menu = st.sidebar.radio(
    "Pilih Menu",
    ["Home", "Monitoring", "Chart", "ReadMe", "Maps", "About"],
    label_visibility="collapsed"
)

submenu = None

if main_menu == "Monitoring":
    submenu = st.sidebar.radio(
        "Pilih Submenu Monitoring",
        ["Overview", "Sensor 1", "Sensor 2"],
        label_visibility="visible"
    )

elif main_menu == "Chart":
    submenu = st.sidebar.radio(
        "Pilih Submenu Chart",
        ["Overview", "RPM", "Temperature"],
        label_visibility="visible"
    )

# ---------- Routing ----------
if main_menu == "Home":
    home_page()

elif main_menu == "Monitoring":
    if submenu == "Overview":
        monitoring_overview()
    elif submenu == "Sensor 1":
        monitoring_sensor1()
    elif submenu == "Sensor 2":
        monitoring_sensor2()

elif main_menu == "Chart":
    if submenu == "Overview":
        chart_overview()
    elif submenu == "RPM":
        chart_rpm()
    elif submenu == "Temperature":
        chart_temp()

elif main_menu == "ReadMe":
    readme_page()

elif main_menu == "Maps":
    maps_page()

elif main_menu == "About":
    about_page()
