from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import pandas as pd
import datetime as dt
from google.oauth2.service_account import Credentials
import gspread
import folium
from streamlit_folium import st_folium
import time
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui 
import random
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import hashlib

st.set_page_config(page_title='BrinTechv2', page_icon='✨', layout="centered", initial_sidebar_state="auto", menu_items={'About': "#v1tr4!"})

# ==================== SISTEM LOGIN ====================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database user dengan privilege
USER_DATA = {
    "admin": {
        "password": hash_password("admin123"),
        "privilege": "Administrator",
        "access": "Full Access"
    },
    "operator": {
        "password": hash_password("operator123"),
        "privilege": "Operator",
        "access": "Monitoring & Chart"
    },
    "researcher": {
        "password": hash_password("research123"),
        "privilege": "Researcher",
        "access": "Read-Only"
    },
    "brin": {
        "password": hash_password("brin2025"),
        "privilege": "BRIN Staff",
        "access": "Full Access"
    }
}

def check_login(username, password):
    hashed_password = hash_password(password)
    if username in USER_DATA and USER_DATA[username]["password"] == hashed_password:
        return True, USER_DATA[username]["privilege"], USER_DATA[username]["access"]
    return False, None, None

# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'privilege' not in st.session_state:
    st.session_state['privilege'] = ''
if 'access' not in st.session_state:
    st.session_state['access'] = ''

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['privilege'] = ''
    st.session_state['access'] = ''
    st.rerun()

# Halaman Login
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            image = Image.open("Picture/Alt_Logo_BRIN.png")
            st.image(image, width=200)
        except:
            st.markdown("### 🔬 BRIN")
    
    st.markdown("<h1 style='text-align: center; color: #0068C9;'>BrinTechv3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Inductance-Capacitance Online Monitoring System</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hover help
    with st.expander("ℹ️ Quick Help", expanded=False):
        col_help = st.columns(2)
        with col_help[0]:
            st.markdown("**Masukkan User pasword**")
        with col_help[1]:
            st.markdown("**Features:**")
            st.markdown("• Real-time monitoring\n• Historical charts\n• System info")
    
    # Form Login
    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if submit:
            if username and password:
                success, privilege, access = check_login(username, password)
                if success:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['privilege'] = privilege
                    st.session_state['access'] = access
                    st.success(f"✅ Welcome, {username}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
            else:
                st.warning("⚠️ Please fill in all fields!")
    
    st.markdown("<p style='text-align: center; color: #999; margin-top: 50px;'>© 2024-2025 BRIN</p>", unsafe_allow_html=True)

# Cek login
if not st.session_state['logged_in']:
    login_page()
    st.stop()

# ==================== APLIKASI UTAMA ====================

st.session_state["home_viewed"] = True

# Fungsi load data
def load_data(url):
    try:
        data = pd.read_csv(url, index_col=0, header=None)
        data.columns = data.iloc[0]
        data.index = data.index.astype(str) + ' ' + data.iloc[:, 0].astype(str)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def plot_gauge(indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": indicator_suffix, "font.size": 26},
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={"text": indicator_title, "font": {"size": 28}},
        )
    )
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10, pad=8))
    st.plotly_chart(fig, use_container_width=True)

# Sidebar

# Sidebar
with st.sidebar:
    # Logo
    try:
        image = Image.open("Picture/Alt_Logo_BRIN.png")
        st.image(image, width=200)
    except:
        pass
  
    # Menu
    selected = option_menu("MENU", ["🏡 Home", '⏳ Monitoring', '📈 Chart', '📖 ReadMe', '🗺️ Maps', '🛈 About'],
                          menu_icon="cast", default_index=0)
    
# User Info Card with integrated buttons
    with st.container():
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 18px 15px; border-radius: 12px; color: white; margin-bottom: 20px; margin-top: 15px;'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <div style='background: white; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; margin-right: 12px;'>
                        <span style='font-size: 22px;'>👤</span>
                    </div>
                    <div style='flex: 1;'>
                        <div style='font-weight: 600; font-size: 17px; margin-bottom: 2px;'>{st.session_state['username']}</div>
                        <div style='font-size: 12px; opacity: 0.85;'>{st.session_state['privilege']}</div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 6px; font-size: 11px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.2);'>
                    🔓 {st.session_state['access']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Buttons directly inside the purple card visual area
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_btn"):
                logout()
        with col2:
            if st.button("🔄 Switch", use_container_width=True, key="switch_btn"):
                logout()
    
    st.markdown("---")


# HOME PAGE
if selected == '🏡 Home':
    st.subheader(":rainbow[BrinTechv2: Aplikasi IoT untuk pemantauan Nilai Kapasitansi dan Nilai induktansi] ⚡")
    try:
        image = Image.open('Picture/EFD.jpg')
        st.image(image, use_column_width=True)
    except:
        st.info("📊 Real-time monitoring of inductance and capacitance values")

# MONITORING PAGE
if selected == '⏳ Monitoring':
    url = 'https://docs.google.com/spreadsheets/d/1zwJ0ncYacsFgMlcLSI3tDsBq1KwcGY-r/export?format=csv'
    data = load_data(url)
    
    if data is not None:
        if 'Time' in data.columns:
            data.drop(columns=['Time'], inplace=True)
        data = data.iloc[1:]
        data.reset_index(drop=True, inplace=True)
        
        try:
            last_idx = -1
            Suhu = float(data['T (°C)'].iloc[last_idx])
            Kelembaban = float(data['RH (%)'].iloc[last_idx])
            Arus = float(data['I (A)'].iloc[last_idx])
            Tegangan = float(data['VLL (Volt)'].iloc[last_idx])
            Daya = float(data['P (kW)'].iloc[last_idx])
            Kondisi = str(data['Description'].iloc[last_idx])
            L1 = float(data['L1 (mH)'].iloc[last_idx])
            L2 = float(data['L2 (mH)'].iloc[last_idx])
            C = float(data['C (µF)'].iloc[last_idx])
            
            try:
                tanggal_col = data['Tanggal '].iloc[last_idx] if 'Tanggal ' in data.columns else data['Tanggal'].iloc[last_idx]
                waktu_col = data['Waktu'].iloc[last_idx]
                Waktu = f"{tanggal_col} {waktu_col}"
                tanggal = datetime.strptime(Waktu, "%d/%m/%Y %H:%M:%S")
                tanggal_str = tanggal.strftime("%d %B %Y %H:%M:%S")
            except:
                tanggal_str = datetime.now().strftime("%d %B %Y %H:%M:%S")
            
            st.subheader(':rainbow[E-Monitor Power Station : Web App]', divider='rainbow')
            st.caption(f'🕐 Last Update: {tanggal_str}')
            
            # Status Card
            col3 = st.columns(1)
            with col3[0]:
                ui.card(title="System Status", content=str(Kondisi), 
                       description="Power Station Condition", key="card6").render()
            
            # Gauges
            col1 = st.columns(2)
            with col1[0]:
                plot_gauge(Suhu, "#0068C9", " °C", "Temperature", 100)
            with col1[1]:
                plot_gauge(Kelembaban, "#29B09D", " %", "Humidity", 100)
            
            # Electrical Parameters
            col2 = st.columns(3)
            with col2[0]:
                ui.card(title="Current", content=f"{Arus:.2f}", description="Ampere", key="card3").render()
            with col2[1]:
                ui.card(title="Voltage", content=f"{Tegangan:.2f}", description="Volt", key="card4").render()
            with col2[2]:
                ui.card(title="Power", content=f"{Daya:.2f}", description="kW", key="card5").render()
            
            # L & C Parameters
            st.subheader("Inductance & Capacitance", divider='rainbow')
            col4 = st.columns(3)
            with col4[0]:
                ui.card(title="L1", content=f"{L1:.2f}", description="mH", key="card7").render()
            with col4[1]:
                ui.card(title="L2", content=f"{L2:.2f}", description="mH", key="card8").render()
            with col4[2]:
                ui.card(title="C", content=f"{C:.2f}", description="µF", key="card9").render()
            
            time.sleep(40)
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.dataframe(data.head())
    else:
        st.error("Failed to load data from Google Sheets")

# CHART PAGE
if (selected == '📈 Chart'):
    st.subheader(':rainbow[E-Monitor Power Station Parameter Chart]', divider='rainbow')
    
    # URL yang konsisten
    url = 'https://docs.google.com/spreadsheets/d/1zwJ0ncYacsFgMlcLSI3tDsBq1KwcGY-r/export?format=csv'
    data = load_data(url)
    
    if data is not None:
        if 'Time' in data.columns:
            data.drop(columns=['Time'], inplace=True)
        
        # Ambil data mulai baris ke-2 (skip header)
        data = data.iloc[1:]
        data.reset_index(drop=True, inplace=True)
        
        # Daftar kolom yang tersedia dari CSV - DITAMBAH L1, L2, C
        options = ['T (°C)', 'RH (%)', 'I (A)', 'VLL (Volt)', 'P (kW)', 'L1 (mH)', 'L2 (mH)', 'C (µF)', 'Q (kVAR)', 'Cos Phi']
        
        selected_option = st.selectbox('Pilih Chart', options)    
        
        try:
            # Konversi kolom yang dipilih menjadi numerik
            df = pd.to_numeric(data[selected_option], errors='coerce')
            
            # Buat figure dengan ukuran lebih besar
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot line chart
            df.plot(ax=ax, kind='line', color='#0068C9', linewidth=2, marker='o', markersize=4)
            
            ax.set_xlabel('Data Point', fontsize=12, fontweight='bold')
            ax.set_ylabel(selected_option, fontsize=12, fontweight='bold')
            ax.set_title(f'Grafik {selected_option} - Data Terbaru di Kanan', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Tambahkan informasi nilai terakhir
            last_value = df.iloc[-1]
            ax.axhline(y=last_value, color='r', linestyle='--', alpha=0.5, label=f'Nilai Terakhir: {last_value:.2f}')
            ax.legend()
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Tampilkan statistik
            st.subheader("Statistik Data")
            col_stats = st.columns(4)
            with col_stats[0]:
                st.metric("Nilai Terakhir", f"{df.iloc[-1]:.2f}")
            with col_stats[1]:
                st.metric("Rata-rata", f"{df.mean():.2f}")
            with col_stats[2]:
                st.metric("Maksimum", f"{df.max():.2f}")
            with col_stats[3]:
                st.metric("Minimum", f"{df.min():.2f}")
                
        except Exception as e:
            st.error(f"Error membuat chart: {e}")
            st.write("Kolom yang tersedia:")
            st.write(data.columns.tolist())
    else:
        st.error("Gagal memuat data untuk chart")




# README PAGE
if (selected == '📖 ReadMe'):
    st.header("📖 ReadMe")
    sections = (
        "🔎 About BrintechV2",
        "🛠️ Sistem Kerja Alat",
        "🏆 Kelebihan Alat",
        "🤔 Author Member",
    )
    tabs = st.tabs(sections)
    
    readme1 = """
    
    **BrintechV2** adalah sistem monitoring inovatif yang dikembangkan oleh tim peneliti BRIN untuk 
    mendeteksi kerusakan dini pada sistem kelistrikan di fasilitas LTA3 (Low-speed Aerodynamic Test Facility 3).
    
    ### 🎯 Tujuan Sistem
    
    Sistem ini dirancang untuk:
    - **Mencegah kegagalan sistem** sebelum terjadi kerusakan fatal
    - **Mengoptimalkan jadwal maintenance** berdasarkan kondisi aktual
    - **Mengurangi downtime** operasional peralatan
    - **Meningkatkan keandalan** sistem kelistrikan
    - **Monitoring real-time** kondisi komponen kritis (induktor & kapasitor)
    
    ### ⚡ Prinsip Kerja
    
    Sistem BrintechV2 bekerja dengan cara:
    
    1. **Pengukuran Real-Time**: Sensor mengukur parameter listrik secara kontinyu
       - Tegangan (VLL, VLN)
       - Arus (I)
       - Daya Aktif (P) dan Daya Reaktif (Q)
       - Faktor Daya (Cos φ)
       - Suhu dan Kelembaban lingkungan
    
    2. **Perhitungan Nilai Komponen**: 
       - Menghitung nilai **Induktansi (L1, L2)** secara real-time
       - Menghitung nilai **Kapasitansi (C)** secara real-time
       - Membandingkan dengan nilai nameplate dan baseline
    
    3. **Deteksi Anomali**:
       - Sistem mengidentifikasi penyimpangan nilai dari kondisi normal
       - Mendeteksi degradasi komponen sejak dini
       - Memberikan peringatan sebelum terjadi kegagalan
    
    ### 🔬 Teknologi yang Digunakan
    
    - **IoT (Internet of Things)**: Sensor terhubung ke cloud untuk monitoring jarak jauh
    - **Real-Time Processing**: Data bisa diproses dan ditampilkan secara langsung (future development)
    - **Cloud Storage**: Data tersimpan di Google Sheets untuk aksesibilitas tinggi
    - **Web Dashboard**: Interface berbasis Streamlit untuk visualisasi data
    - **Machine Learning Ready**: Arsitektur data siap untuk implementasi ML di masa depan
    
    ### 📊 Parameter yang Dimonitor
    
    | Parameter | Satuan | Keterangan |
    |-----------|--------|------------|
    | RPM | rpm | Kecepatan putaran motor |
    | Cos φ | - | Faktor daya sistem |
    | V₀ | m/s | Kecepatan udara |
    | P | kW | Daya aktif |
    | VLL | Volt | Tegangan line-to-line |
    | VLN | Volt | Tegangan line-to-neutral |
    | I | Ampere | Arus listrik |
    | Q | kVAR | Daya reaktif |
    | L1, L2 | mH | Induktansi komponen |
    | C | µF | Kapasitansi komponen |
    | T | °C | Suhu lingkungan |
    | RH | % | Kelembaban relatif |
    
    ### 🎓 Manfaat Sistem
    
    **Untuk Operator:**
    - Monitoring kondisi peralatan 24/7 dari mana saja
    - Dashboard intuitif dan mudah dipahami
    - Alert otomatis jika ada anomali (future development)
    
    **Untuk Teknisi Maintenance:**
    - Data historis lengkap untuk analisis trend
    - Predictive maintenance berdasarkan data aktual
    - Dokumentasi kondisi peralatan yang sistematis
    
    **Untuk Manajemen:**
    - Pengambilan keputusan berbasis data
    - Optimalisasi biaya perawatan
    - Compliance dengan standar keselamatan
    
    ### 🔐 Keamanan Data
    
    - Backup otomatis ke cloud storage
    - Access control untuk user berbeda
    - Audit trail untuk semua perubahan data
    
    ### 🌐 Aksesibilitas
    
    Sistem dapat diakses melalui:
    - **Web Browser**: Desktop/Laptop (Chrome, Firefox, Edge)
    - **Mobile**: Smartphone dan tablet (responsive design)
    - **API**: Integrasi dengan sistem lain (future development)
    
    ---
    
    💡 **Inovasi Utama**: Sistem ini merupakan yang pertama di Indonesia yang mengintegrasikan 
    monitoring induktansi dan kapasitansi secara real-time dengan teknologi IoT untuk aplikasi 
    fasilitas aerodinamika.
    """ 
    tabs[0].info(readme1)

    readme2 = """
    
    Dengan nilai arus, tegangan, dan faktor daya yang diukur, daya aktif real-time dapat diperoleh. Dari daya aktif ini, nilai kapasitansi real-time 
    dapat ditentukan menggunakan rumus C = 2 (P*t / V^2). Dengan rumus ini, kapasitansi (C) dari sistem satu fasa atau tiga fasa dapat dihitung.
    
    **Menentukan Nilai L (Induktansi)**
    
    Nilai induktansi real-time dapat ditentukan menggunakan rumus L = 2 (P*t / I^2). Dengan rumus ini, induktansi (L) dari sistem satu fasa atau tiga fasa dapat dihitung.

    **Menentukan Kondisi Filter LCL**
    
    Setelah nilai kapasitansi (C) dan induktansi (L), serta kondisi suhu dan kelembaban real-time, diperoleh, nilai-nilai ini dibandingkan 
    dengan data pelat nama pada kedua komponen dan data pengukuran sebelumnya (perawatan tahunan) untuk menentukan kondisinya.
    """
    tabs[1].success(readme2)
    
    readme3 = """
    Adapun keunggulan aplikasi modul alat yang sedang dalam proses penelitian ini adalah sebagai berikut :
    
    - Dapat menampilkan hasil pengukuran kualitas daya listrik dua panel listrik/mesin listrik sekaligus dalam satu modul alat.
    - Dapat menampilkan hasil pengukuran kualitas daya listrik dalam dua posisi rangkaian berbeda (seri dan paralel) sekaligus dalam satu modul alat.
    - Dapat menampilkan hasil pengukuran nilai kapasitansi secara real time.
    - Dapat menampilkan hasil pengukuran nilai induktansi secara real time.
    - Pengiriman data berbasis teknologi Internet of Things.
    """

    tabs[2].info(readme3)
    
    readme4 = """
    Author alat early fault detection power station ini antara lain : 
    
    - Asep Dadan Hermawan, S.T., M.Sc.                      
    - Tsani Hendro Nugroho, S.T., M.T.                      
    - Fitra Hidiyanto, S.T., M.T.                                       
    - Heri Nugraha, S.T., M.Si.                     
    """

    tabs[3].error(readme4)



# MAPS PAGE
if selected == '🗺️ Maps':
    st.subheader("📍 Location")
    
    try:
        lat, lon = -6.346044170409775, 106.66635703863085
        m = folium.Map(location=[lat, lon], zoom_start=17, tiles='OpenStreetMap')
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup("BRIN LTA3 Facility", max_width=300),
            tooltip="📍 Click for info",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        st_folium(m, width=700, height=500, returned_objects=[])
        st.info(f"📍 Coordinates: {lat}, {lon}")
    except Exception as e:
        st.error(f"Error: {e}")
        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        st.markdown(f"[🗺️ Open in Google Maps]({google_maps_url})")


# ABOUT PAGE
if (selected == '🛈 About'):
    st.subheader(":rainbow[─ ⊹ ⊱ ⋆˚ Brintech Monitoring - BRIN team 𝜗𝜚˚⋆ ⊰ ⊹ ─]")
     
    # Informasi Proyek
    st.header("📋 Informasi Proyek")
    
    col_info = st.columns(2)
    with col_info[0]:
        st.markdown("""
        **🏢 Institusi**  
        Badan Riset dan Inovasi Nasional (BRIN)
        
        **🔬 Divisi**  
        Pusat Riset kelistrikan
        
        **📍 Lokasi**  
        Fasilitas LTA3, Serpong, Tangerang Selatan
        """)
    
    with col_info[1]:
        st.markdown("""
        **📅 Tahun Pengembangan**  
        2024 - 2027
        
        **🎯 Status Proyek**  
        ✅ Development & Testing
        
        **🔖 Versi Aplikasi**  
        v2.0 - BrinTechv2
        """)
    
    st.markdown("---")
    
    # Tim Peneliti
    st.header("👥 Tim Peneliti & Pengembang")
    
    st.markdown("""
    Tim Early Fault Detection System terdiri dari para peneliti dan engineer berpengalaman 
    di bidang sistem kelistrikan, IoT, dan aerodinamika.
    """)
    
    # Menggunakan columns untuk layout card-style
    researchers = [
        {
            "nama": "Asep Dadan Hermawan, S.T., M.Sc.",
            "role": "🎓 Principal Investigator",
            "expertise": "Sistem Kelistrikan & Power Quality",
            "kontribusi": "Lead Researcher, System Architecture Design"
        },
        {
            "nama": "Tsani Hendro Nugroho, S.T., M.T.",
            "role": "🔧 Senior Researcher",
            "expertise": "Electrical Engineering & Instrumentation",
            "kontribusi": "Hardware Integration, Sensor Calibration"
        },
        {
            "nama": "Fitra Hidiyanto, S.T., M.T.",
            "role": "💻 Machine Learning & IoT Engineer",
            "expertise": "Internet of Things, Data Analytics, Web App Programer",
            "kontribusi": "Web App programing, Cloud Integration"
        },
        {
            "nama": "Heri Nugraha, S.T., M.Si.",
            "role": "⚡ Power Systems Specialist",
            "expertise": "Power Electronics & Control Systems",
            "kontribusi": "Algorithm Development, Testing & Validation"
        }
    ]
    
    for i in range(0, len(researchers), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(researchers):
                researcher = researchers[i + j]
                with col:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 10px;">
                        <h4 style="color: #0068C9; margin-bottom: 10px;">{researcher['nama']}</h4>
                        <p style="margin: 5px 0;"><strong>{researcher['role']}</strong></p>
                        <p style="margin: 5px 0; font-size: 0.9em;">📚 {researcher['expertise']}</p>
                        <p style="margin: 5px 0; font-size: 0.9em;">🎯 {researcher['kontribusi']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Teknologi Stack
    st.header("🛠️ Technology Stack")
    
    tech_cols = st.columns(3)
    
    with tech_cols[0]:
        st.markdown("""
        **Frontend**
        - 🐍 Python 3.9+
        - 🎨 Streamlit
        - 📊 Plotly & Matplotlib
        - 🗺️ Folium Maps
        """)
    
    with tech_cols[1]:
        st.markdown("""
        **Backend & Data**
        - ☁️ Google Sheets API
        - 🦆 DuckDB
        - 🐼 Pandas
        - 📡 Real-time streaming
        """)
    
    with tech_cols[2]:
        st.markdown("""
        **Hardware**
        - ⚡ PZEM-004T Sensor
        - 🌡️ DHT22 (Temp & Humidity)
        - 📶 ESP32 Microcontroller
        - 🔌 Current & Voltage Sensors
        """)
    
    st.markdown("---")
    
    # Roadmap Future Development
    st.header("🚀 Roadmap & Future Development")
    
    st.markdown("""
    ### Phase 1 (2025) - ✅ Completed
    - ✅ Basic monitoring system
    - ✅ Real-time data collection
    - ✅ Web dashboard development
    
    ### Phase 2 (2026) - 🔄 In Progress
    - 🔄 Machine Learning integration for predictive maintenance
    - 🔄 Mobile app development (iOS & Android)
    - 🔄 Advanced alerting system with SMS/Email notifications
    
    ### Phase 3 (2027) - 📋 Planned
    - 📋 Multi-facility deployment
    - 📋 AI-powered anomaly detection
    - 📋 Integration with SCADA systems
    - 📋 Automated reporting system
    """)
    
    st.markdown("---")
    
    # Kontak & Dukungan
    st.header("📞 Kontak & Dukungan")
    
    contact_cols = st.columns(2)
    
    with contact_cols[0]:
        st.markdown("""
        **📧 Email**  
        asep042@brin.go.id
        
        **🌐 Website**  
        --https://brintechv2.streamlit.app/-- 
        
        **📱 Hotline**  
        +62 813 1090 5765
        """)
    
    with contact_cols[1]:
        st.markdown("""
        **📍 Alamat**  
        Gedung LTA3  
        BRIN Kawasan Puspiptek  
        Serpong, Tangerang Selatan 15314
        
        **🕐 Jam Operasional**  
        Senin - Jumat: 09:00 - 15:00 WIB
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
        <h4>🇮🇩 Proudly Made in Indonesia</h4>
        <p>© 2024-2025 BRIN - Badan Riset dan Inovasi Nasional</p>
        <p style="font-size: 0.9em; color: #666;">
            Early Fault Detection System | Advancing Indonesia's Aerodynamic Research
        </p>
        <p style="margin-top: 10px;">
            ⭐ <em>Innovation • Precision • Reliability</em> ⭐
        </p>
    </div>
    """, unsafe_allow_html=True)



