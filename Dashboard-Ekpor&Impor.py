import streamlit as st
import pandas as pd
import plotly.express as px

# ---- KONFIGURASI HALAMAN ----
st.set_page_config(
    page_title="Dashboard Ekspor-Impor",
    page_icon="📦",
    layout="wide"
)

st.markdown("""
    <style>
    /* =======================
       GLOBAL BACKGROUND
    ======================= */
    .stApp {
        background-color: #f5f7fa;
        font-family: "Segoe UI", sans-serif;
    }

    /* Background dengan partikel halus */
    body::before {
        content: "";
        position: fixed;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(99,164,255,0.15) 1px, transparent 1px);
        background-size: 40px 40px;
        animation: movebg 25s linear infinite;
        z-index: -1;
    }
    @keyframes movebg {
        from { background-position: 0 0; }
        to { background-position: 200px 200px; }
    }

    /* =======================
       HEADER STYLE
    ======================= */
    .header {
        background: linear-gradient(135deg, #1f77b4, #63a4ff);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeInDown 1s ease;
    }
    .header h1 {
        font-size: 38px;
        margin: 0;
        font-weight: bold;
        animation: glowText 2s ease-in-out infinite alternate;
    }
    .header p {
        font-size: 18px;
        margin: 5px 0 0;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes glowText {
        from { text-shadow: 0 0 5px #fff, 0 0 10px #63a4ff; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #1f77b4; }
    }

    /* =======================
       SIDEBAR STYLE
    ======================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1f77b4, #63a4ff);
        color: white;
        box-shadow: inset 0 0 30px rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
    }

    /* Partikel Sidebar */
    @keyframes float {
        0% { transform: translateY(0px); opacity: 0.6; }
        50% { transform: translateY(-10px); opacity: 1; }
        100% { transform: translateY(0px); opacity: 0.6; }
    }
    .sidebar-particle {
        position: absolute;
        width: 8px;
        height: 8px;
        background: rgba(255,255,255,0.6);
        border-radius: 50%;
        animation: float 3s ease-in-out infinite;
    }
    .particle1 { top: 50px; left: 20px; animation-delay: 0s; }
    .particle2 { top: 150px; left: 80px; animation-delay: 1s; }
    .particle3 { top: 250px; left: 40px; animation-delay: 2s; }

    /* =======================
       STAT BOX
    ======================= */
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 1s ease;
    }
    .stat-box:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }

    /* =======================
       CHART HEADER
    ======================= */
    .chart-header {
        background: linear-gradient(135deg, #ff7f50, #ffb347);
        padding: 8px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease;
    
        /* Tambahan spacing */
        margin-top: 15px;   /* kasih jarak dari atas */
        margin-bottom: 12px; /* jarak ke chart */
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <!-- =======================
         HTML HEADER
    ======================= -->
    <div class="header">
        <h1>📦 Dashboard Ekspor-Impor Indonesia</h1>
        <p>Visualisasi data ekspor-impor perusahaan ke berbagai negara 🌍</p>
    </div>

    <!-- Partikel Sidebar -->
    <div class="sidebar-particle particle1"></div>
    <div class="sidebar-particle particle2"></div>
    <div class="sidebar-particle particle3"></div>
""", unsafe_allow_html=True)

# ---- UPLOAD FILE ----
uploaded_file = st.file_uploader("📂 Upload file Excel/CSV", type=["xlsx", "csv"])
if uploaded_file:
    # Baca file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # ========================
    # STAT BOXES (Highlight)
    # ========================
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if "Negara Tujuan" in df.columns:
            st.markdown(f"<div class='stat-box'>🌍 {df['Negara Tujuan'].nunique()} Negara Tujuan</div>", unsafe_allow_html=True)
    with col_b:
        if "Jenis Komoditi" in df.columns:
            st.markdown(f"<div class='stat-box'>📦 {df['Jenis Komoditi'].nunique()} Jenis Komoditi</div>", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"<div class='stat-box'>📝 {len(df)} Total Transaksi</div>", unsafe_allow_html=True)

    # ========================
    # FILTERS
    # ========================
    st.sidebar.header("🔍 Filter Data")

    # Filter negara dengan opsi "Pilih Semua"
    if "Negara Tujuan" in df.columns:
        all_negara = df["Negara Tujuan"].unique()
        pilih_semua = st.sidebar.checkbox("Pilih Semua Negara", value=True)
        if pilih_semua:
            negara_filter = all_negara
        else:
            negara_filter = st.sidebar.multiselect("Pilih Negara", options=all_negara, default=all_negara[:5])
    else:
        negara_filter = []

    # Filter komoditi
    if "Jenis Komoditi" in df.columns:
        komoditi_filter = st.sidebar.multiselect("Pilih Komoditi", options=df["Jenis Komoditi"].unique(), default=df["Jenis Komoditi"].unique())
    else:
        komoditi_filter = []

    if len(negara_filter) > 0 and len(komoditi_filter) > 0:
        df_filtered = df[
            (df["Negara Tujuan"].isin(negara_filter)) &
            (df["Jenis Komoditi"].isin(komoditi_filter))
        ]
    elif len(negara_filter) > 0:
        df_filtered = df[df["Negara Tujuan"].isin(negara_filter)]
    elif len(komoditi_filter) > 0:
        df_filtered = df[df["Jenis Komoditi"].isin(komoditi_filter)]
    else:
        df_filtered = df.copy()

    # ========================
    # CHARTS
    # ========================
    col1, col2 = st.columns(2)
    with col1:
        if "Jenis Komoditi" in df_filtered.columns:
            st.markdown("<div class='chart-header'>📊 Top 10 Jenis Komoditi</div>", unsafe_allow_html=True)
            komoditi_count = df_filtered["Jenis Komoditi"].value_counts().reset_index().head(10)
            komoditi_count.columns = ["Komoditi", "Jumlah"]
            fig1 = px.bar(komoditi_count, x="Komoditi", y="Jumlah", color="Komoditi", text="Jumlah")
            fig1.update_traces(textposition="outside")
            st.plotly_chart(fig1, use_container_width=True)
    with col2:
        if "Negara Tujuan" in df_filtered.columns:
            st.markdown("<div class='chart-header'>🌍 Top 10 Negara Tujuan</div>", unsafe_allow_html=True)
            negara_count = df_filtered["Negara Tujuan"].value_counts().reset_index().head(10)
            negara_count.columns = ["Negara", "Jumlah"]
            fig2 = px.bar(negara_count, x="Negara", y="Jumlah", color="Negara", text="Jumlah")
            fig2.update_traces(textposition="outside")
            st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if "Pelabuhan/Banda Tujuan" in df_filtered.columns:
            st.markdown("<div class='chart-header'>⚓ Top 10 Pelabuhan Tujuan</div>", unsafe_allow_html=True)
            pelabuhan_count = df_filtered["Pelabuhan/Banda Tujuan"].value_counts().reset_index().head(10)
            pelabuhan_count.columns = ["Pelabuhan", "Jumlah"]
            fig3 = px.bar(pelabuhan_count, x="Pelabuhan", y="Jumlah", color="Pelabuhan", text="Jumlah")
            fig3.update_traces(textposition="outside")
            st.plotly_chart(fig3, use_container_width=True)
    with col4:
        if "Bank/Pos Bayar" in df_filtered.columns and "Channel Bayar" in df_filtered.columns:
            st.markdown("<div class='chart-header'>💳 Metode Pembayaran</div>", unsafe_allow_html=True)
            bayar_count = df_filtered.groupby(["Bank/Pos Bayar", "Channel Bayar"]).size().reset_index(name="Jumlah")
            fig4 = px.bar(bayar_count, x="Bank/Pos Bayar", y="Jumlah", color="Channel Bayar", text="Jumlah", barmode="group")
            fig4.update_traces(textposition="outside")
            st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        if " Nama Buyer" in df_filtered.columns:
            st.markdown("<div class='chart-header'>🏢 Top 10 Buyer</div>", unsafe_allow_html=True)
            top_10_buyer = df_filtered[' Nama Buyer'].value_counts().head(10).reset_index()
            top_10_buyer.columns = ['Nama Buyer', 'Jumlah Transaksi']
            fig_buyer = px.bar(top_10_buyer, x="Nama Buyer", y="Jumlah Transaksi", color="Nama Buyer", text="Jumlah Transaksi")
            fig_buyer.update_traces(textposition="outside")
            st.plotly_chart(fig_buyer, use_container_width=True)
    with col6:
        if "Nama Exportir/Importir" in df_filtered.columns:
            st.markdown("<div class='chart-header'>🏭 Top 10 Exportir/Importir</div>", unsafe_allow_html=True)
            top_10_exportir = df_filtered['Nama Exportir/Importir'].value_counts().head(10).reset_index()
            top_10_exportir.columns = ['Exportir/Importir', 'Jumlah Transaksi']
            fig_exportir = px.bar(top_10_exportir, x="Exportir/Importir", y="Jumlah Transaksi", color="Exportir/Importir", text="Jumlah Transaksi")
            fig_exportir.update_traces(textposition="outside")
            st.plotly_chart(fig_exportir, use_container_width=True)

    if "Diterbitkan Tanggal" in df_filtered.columns:
        st.markdown("<div class='chart-header'>⏳ Timeline Ekspor</div>", unsafe_allow_html=True)
        df_filtered["Diterbitkan Tanggal"] = pd.to_datetime(df_filtered["Diterbitkan Tanggal"], errors="coerce")
        timeline = df_filtered.dropna(subset=["Diterbitkan Tanggal"]).groupby("Diterbitkan Tanggal").size().reset_index(name="Jumlah")
        if not timeline.empty:
            fig5 = px.line(timeline, x="Diterbitkan Tanggal", y="Jumlah", markers=True)
            st.plotly_chart(fig5, use_container_width=True)

    if "Negara Tujuan" in df_filtered.columns:
        st.markdown("<div class='chart-header'>🌍 Peta Negara Tujuan Ekspor</div>", unsafe_allow_html=True)
        negara_count = df_filtered["Negara Tujuan"].value_counts().reset_index()
        negara_count.columns = ["Negara", "Jumlah"]
        fig6 = px.scatter_geo(negara_count, locations="Negara", locationmode="country names", size="Jumlah", color="Jumlah", hover_name="Negara", projection="natural earth")
        st.plotly_chart(fig6, use_container_width=True)

    if "Latitude" in df_filtered.columns and "Longitude" in df_filtered.columns:
        st.markdown("<div class='chart-header'>🗺️ Peta Interaktif Lokasi (Google Maps Style)</div>", unsafe_allow_html=True)
        fig7 = px.scatter_mapbox(df_filtered, lat="Latitude", lon="Longitude", hover_name="Negara Tujuan", hover_data=["Jenis Komoditi", "Pelabuhan/Banda Tujuan"], color="Negara Tujuan", size_max=15, zoom=1, height=600)
        fig7.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.warning("Dataset belum memiliki kolom Latitude dan Longitude.")

    # Footer
    st.markdown("---")
    st.markdown("<center>👨‍💻 Dibuat dengan ❤️ menggunakan <b>Streamlit & Plotly</b></center>", unsafe_allow_html=True)
