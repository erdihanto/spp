import streamlit as st

st.set_page_config(
    page_title="Sistem Informasi Dian Wacana", page_icon="🏫", layout="wide"
)

st.title("🏫 Selamat Datang di Portal TK-KB-SD Dian Wacana")
st.write(
    "Silakan pilih menu di samping (sidebar) untuk mengakses fitur aplikasi."
)

st.markdown("---")

# Tampilan Halaman Utama / Dashboard Sederhana
col1, col2 = st.columns(2)

with col1:
  st.info("### 📌 Informasi Sekolah")
  st.write(
      "Aplikasi ini digunakan untuk mengelola data administrasi dan kesiswaan"
      " unit Kelompok Bermain (KB), Taman Kanak-Kanak (TK), dan Sekolah Dasar"
      " (SD) Dian Wacana."
  )

with col2:
  st.success("### 🚀 Navigasi Cepat")
  st.write(
      "Gunakan menu **Data Siswa** pada panel sebelah kiri untuk melihat,"
      " menambah, atau mengelola data siswa."
  )
