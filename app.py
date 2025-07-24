import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
client = gspread.authorize(creds)

# Spreadsheet setup
SPREADSHEET_KEY = "1ftJI3Yk0ebPipAoS8CnfZ8LzRJ5zgaQDaN3rtQSPNHs"
sheet_names = [
    "OPSI 2 - Data Voucher",
    "OPSI 2 - Riwayat Klaim Ticketin",
    "OPSI 2 - Riwayat Klaim Hotel"
]

@st.cache_data(ttl=600)
def load_data():
    data = {}
    for sheet in sheet_names:
        ws = client.open_by_key(SPREADSHEET_KEY).worksheet(sheet)
        df = pd.DataFrame(ws.get_all_records())
        data[sheet] = df
    return data

data = load_data()

# Sidebar filter
st.sidebar.title("🔎 Filter Kode Voucher")
kode_list = data["OPSI 2 - Data Voucher"]["Kode Voucher"].dropna().unique().tolist()
selected_kode = st.sidebar.selectbox("Pilih Kode Voucher", kode_list)

# Main content
st.title("🎫 Dashboard Klaim Voucher Mitra Tours")
st.write(f"Menampilkan detail untuk **Kode Voucher: {selected_kode}**")

st.subheader("📋 Data Voucher")
df_voucher = data["OPSI 2 - Data Voucher"]
st.dataframe(df_voucher[df_voucher["Kode Voucher"] == selected_kode])

st.subheader("🎟️ Riwayat Klaim Ticketin")
df_ticketin = data["OPSI 2 - Riwayat Klaim Ticketin"]
st.dataframe(df_ticketin[df_ticketin["Kode Voucher"] == selected_kode])

st.subheader("🏨 Riwayat Klaim Hotel")
df_hotel = data["OPSI 2 - Riwayat Klaim Hotel"]
st.dataframe(df_hotel[df_hotel["Kode Voucher"] == selected_kode])

st.markdown("---")
st.markdown("📌 Data otomatis diambil dari Google Sheets dan diperbarui setiap 10 menit.")
