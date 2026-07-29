import sqlite3
import pandas as pd
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Dian Wacana", page_icon="🏫", layout="wide"
)

# --- CSS COLORFUL ---
st.markdown("""
    <style>
    .colorful-header {
        background: linear-gradient(135deg, #FF6B6B, #FFD93D);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        margin-bottom: 25px;
    }
    .colorful-header h1 {
        font-weight: 800;
        margin-bottom: 5px;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .colorful-header p {
        font-weight: 600;
        color: #FFF;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)


# --- HALAMAN 1: BERANDA UTAMA (MURNI TANPA DATABASE) ---
def halaman_beranda():
  st.markdown(
      """
        <div class="colorful-header" style="background: linear-gradient(135deg, #4e54c8, #8f94fb);">
            <h1>🏫 PORTAL UTAMA DIAN WACANA</h1>
            <p>Selamat datang di sistem manajemen informasi sekolah KB, TK, dan SD.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    st.info("### 📌 Informasi Sistem")
    st.write(
        "Gunakan menu navigasi di sebelah kiri untuk berpindah ke halaman"
        " pengelolaan data siswa."
    )
  with col2:
    st.success("### 🚀 Petunjuk")
    st.write(
        "Pilih menu **Data Siswa** pada sidebar untuk mulai melihat dan"
        " mengelola database."
    )


# --- HALAMAN 2: DATA SISWA (DATABASE HANYA AKTIF DI SINI) ---
def halaman_data_siswa():
  # Fungsionalitas Database & Inisialisasi
  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            nisn TEXT,
            jenjang TEXT,
            kelas TEXT,
            jk TEXT
        )
    """)
  conn.commit()
  conn.close()

  st.markdown(
      """
        <div class="colorful-header">
            <h1>🌟 PUSAT DATA SISWA DIAN WACANA 🌟</h1>
            <p>Kelola Data Kelompok Bermain (KB), Taman Kanak-Kanak (TK), dan Sekolah Dasar (SD)</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Form Tambah Data
  with st.form("form_tambah_siswa_colorful"):
    st.markdown("### ✍️ Form Pencatatan Siswa Baru")
    col_a, col_b = st.columns(2)
    with col_a:
      nama = st.text_input("👤 Nama Lengkap Siswa")
      nisn = st.text_input("🆔 NISN / Nomor Induk")
      jenjang = st.selectbox("🎓 Pilih Jenjang Sekolah", ["KB", "TK", "SD"])
    with col_b:
      kelas = st.text_input("🏫 Kelas (Contoh: A, B, atau 1-6)")
      jk = st.selectbox("⚧ Jenis Kelamin", ["Laki-laki", "Perempuan"])

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button(
        "🚀 Simpan Data ke Database", use_container_width=True
    )

    if submit:
      if nama and nisn and kelas:
        conn = sqlite3.connect("dian_wacana.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO siswa (nama, nisn, jenjang, kelas, jk) VALUES (?, ?, ?, ?, ?)",
            (nama, nisn, jenjang, kelas, jk),
        )
        conn.commit()
        conn.close()
        st.success("🎉 Data siswa berhasil disimpan!")
        st.rerun()
      else:
        st.error("⚠️ Mohon isi semua kolom data dengan lengkap.")

  st.markdown("---")

  # Tabel Data Siswa Otomatis
  st.markdown("### 📋 Daftar Seluruh Siswa Terdaftar")
  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute("SELECT id, nama, nisn, jenjang, kelas, jk FROM siswa")
  data_siswa = cursor.fetchall()
  conn.close()

  if data_siswa:
    df = pd.DataFrame(
        data_siswa,
        columns=["ID", "Nama Lengkap", "NISN", "Jenjang", "Kelas", "L/P"],
    )

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
      st.metric(label="📊 Total Keseluruhan Siswa", value=f"{len(df)} Siswa")
    with col_s2:
      total_sd = len(df[df["Jenjang"] == "SD"])
      st.metric(label="🎒 Jenjang SD", value=f"{total_sd} Siswa")
    with col_s3:
      total_kbtk = len(df[df["Jenjang"].isin(["KB", "TK"])])
      st.metric(label="🎨 Jenjang KB & TK", value=f"{total_kbtk} Siswa")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
  else:
    st.warning("🎨 Belum ada data siswa yang tersimpan di database.")


# --- SISTEM NAVIGASI SIDEBAR OTOMATIS ---
pg = st.navigation(
    [
        st.Page(halaman_beranda, title="Beranda Utama", icon="🏫"),
        st.Page(halaman_data_siswa, title="Data Siswa", icon="📚"),
    ]
)

pg.run()
