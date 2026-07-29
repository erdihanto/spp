import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Dian Wacana", page_icon="🏫", layout="wide"
)

# --- SIDEBAR: Menu Navigasi (Tanpa Database) ---
st.sidebar.title("🏫 Menu Utama")
st.sidebar.write("Silakan pilih menu di bawah:")

# Pilihan menu menggunakan Radio Button di Sidebar
menu_pilihan = st.sidebar.radio(
    "Navigasi:", ["Beranda (Home)", "Kelola Data Siswa"]
)

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi TK - KB - SD Dian Wacana")

# --- KONTROL TAMPILAN BERDASARKAN MENU ---

if menu_pilihan == "Beranda (Home)":
  # Halaman Utama (Murni Informasi)
  st.title("🏫 Selamat Datang di Portal TK-KB-SD Dian Wacana")
  st.write(
      "Aplikasi ini digunakan untuk mengelola data administrasi dan kesiswaan"
      " unit Kelompok Bermain (KB), Taman Kanak-Kanak (TK), dan Sekolah Dasar"
      " (SD) Dian Wacana."
  )

  st.markdown("---")

  col1, col2 = st.columns(2)

  with col1:
    st.info("### 📌 Informasi Sekolah")
    st.write(
        "Gunakan menu navigasi **Kelola Data Siswa** di panel sebelah kiri untuk"
        " mulai memasukkan atau melihat data."
    )

  with col2:
    st.success("### 🚀 Petunjuk Penggunaan")
    st.write(
        "Klik pilihan **Kelola Data Siswa** pada sidebar untuk membuka form"
        " tambah data dan tabel siswa."
    )

elif menu_pilihan == "Kelola Data Siswa":
  # Bagian ini mengarahkan pengguna ke file terpisah (data_siswa.py) 
  # atau memuat komponen datanya secara aman.
  # Pastikan file 'data_siswa.py' ada di dalam folder 'pages/'
  
  st.title("📂 Pindah Halaman")
  st.write("Anda memilih menu **Kelola Data Siswa**.")
  st.write(
      "Silعة klik tautan atau menu halaman **Data Siswa** yang otomatis muncul di"
      " bagian atas/bawah sidebar bawaan Streamlit, atau gunakan tombol di"
      " bawah ini:"
  )

  # Tombol alternatif untuk pindah halaman jika menggunakan struktur pages/
  if st.button("👉 Buka Halaman Data Siswa"):
    st.switch_page("pages/data_siswa.py")
