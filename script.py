import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autentikasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = st.secrets["google"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# Load spreadsheet by key
SPREADSHEET_KEY = "1ftJI3Yk0ebPipAoS8CnfZ8LzRJ5zgaQDaN3rtQSPNHs"
sheet_names = [
    "OPSI 2 - Data Voucher",
    "OPSI 2 - Riwayat Klaim Ticketin",
    "OPSI 2 - Riwayat Klaim Hotel"
]

@st.cache_data(ttl=600)  # refresh setiap 10 menit
def load_data():
    data = {}
    for name in sheet_names:
        worksheet = client.open_by_key(SPREADSHEET_KEY).worksheet(name)
        data[name] = pd.DataFrame(worksheet.get_all_records())
    return data

data = load_data()

# Sidebar: Filter berdasarkan Kode Voucher
st.sidebar.title("🔎 Filter Pencarian")
kode_list = data["OPSI 2 - Data Voucher"]["Kode Voucher"].unique().tolist()
selected_kode = st.sidebar.selectbox("Pilih Kode Voucher", kode_list)

# Judul
st.title("🎫 Dashboard Voucher dan Klaim")
st.markdown(f"Menampilkan data terkait voucher: **{selected_kode}**")

# Tampilkan Data Voucher
st.subheader("📋 Data Voucher")
filtered_voucher = data["OPSI 2 - Data Voucher"][data["OPSI 2 - Data Voucher"]["Kode Voucher"] == selected_kode]
st.dataframe(filtered_voucher)

# Tampilkan Riwayat Klaim Ticketin
st.subheader("🎟️ Riwayat Klaim Ticketin")
filtered_ticketin = data["OPSI 2 - Riwayat Klaim Ticketin"][data["OPSI 2 - Riwayat Klaim Ticketin"]["Kode Voucher"] == selected_kode]
st.dataframe(filtered_ticketin)

# Tampilkan Riwayat Klaim Hotel
st.subheader("🏨 Riwayat Klaim Hotel")
filtered_hotel = data["OPSI 2 - Riwayat Klaim Hotel"][data["OPSI 2 - Riwayat Klaim Hotel"]["Kode Voucher"] == selected_kode]
st.dataframe(filtered_hotel)

# Footer
st.markdown("---")
st.markdown("📌 *Data otomatis diambil dari Google Sheets dan akan diperbarui setiap 10 menit.*")
