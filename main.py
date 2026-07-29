import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Dian Wacana", page_icon="🏫", layout="wide"
)

# --- SIDEBAR: Menu Utama ---
st.sidebar.title("🏫 Menu Utama")
st.sidebar.write("Silakan pilih menu di bawah:")

# Navigasi halaman menggunakan Streamlit Pages otomatis
# Pastikan file data_siswa.py berada di dalam folder 'pages/'

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi TK - KB - SD Dian Wacana")

# --- KONTROL HALAMAN UTAMA ---
st.title("🏫 Selamat Datang di Portal TK-KB-SD Dian Wacana")
st.write(
    "Aplikasi ini digunakan untuk mengelola data administrasi dan kesiswaan unit"
    " Kelompok Bermain (KB), Taman Kanak-Kanak (TK), dan Sekolah Dasar (SD)"
    " Dian Wacana."
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
  st.info("### 📌 Informasi Sekolah")
  st.write(
      "Gunakan menu navigasi di panel sebelah kiri untuk mengakses halaman"
      " pengelolaan data siswa."
  )

with col2:
  st.success("### 🚀 Petunjuk Penggunaan")
  st.write(
      "Klik menu **Data Siswa** yang ada di sidebar untuk melakukan input data"
      " dan melihat daftar siswa."
  )
