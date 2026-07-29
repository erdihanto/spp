import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL & MODEREN ---
st.markdown("""
    <style>
    /* Header Halaman dengan Gradien Terang & Ceria */
    .colorful-header {
        background: linear-gradient(135deg, #FF6B6B, #FFD93D);
        padding: 30px;
        border-radius: 15px;
        color: #2D3436;
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

    /* Kotak Form Input dengan Aksen Warna Warni */
    .form-container {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #6C5CE7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* Kartu Statistik Warna-Warni */
    .stat-card {
        background: linear-gradient(135deg, #00B894, #00CEC9);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 184, 148, 0.2);
    }
    </style>
""", unsafe_allow_html=True)


# --- Inisialisasi Database ---
def init_db():
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


init_db()

# --- HEADER COLORFUL ---
st.markdown("""
    <div class="colorful-header">
        <h1>🌟 PUSAT DATA SISWA DIAN WACANA 🌟</h1>
        <p>Kelola Data Kelompok Bermain (KB), Taman Kanak-Kanak (TK), dan Sekolah Dasar (SD)</p>
    </div>
""", unsafe_allow_html=True)

# --- FORM TAMBAH DATA (DI TENGAH DENGAN STYLE KARTU) ---
with st.container():
  st.markdown("### ✍️ Form Pencatatan Siswa Baru")
  with st.form("form_tambah_siswa_colorful"):
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
        st.success(
            "🎉 Hore! Data siswa baru berhasil disimpan dengan penuh warna!"
        )
        st.rerun()
      else:
        st.error("⚠️ Ups! Mohon isi semua kolom data dengan lengkap ya.")

st.markdown("---")

# --- TABEL DATA SISWA (AUTO-LOAD & COLORFUL STATS) ---
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

  # Bagian Statistik Interaktif
  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    st.metric(
        label="📊 Total Keseluruhan Siswa",
        value=f"{len(df)} Siswa",
        delta="Aktif Belajar",
    )
  with col_s2:
    total_sd = len(df[df["Jenjang"] == "SD"])
    st.metric(label="🎒 Jenjang SD", value=f"{total_sd} Siswa")
  with col_s3:
    total_kbtk = len(df[df["Jenjang"].isin(["KB", "TK"])])
    st.metric(label="🎨 Jenjang KB & TK", value=f"{total_kbtk} Siswa")

  st.markdown("<br>", unsafe_allow_html=True)

  # Menampilkan tabel dengan gaya bawaan Streamlit yang bersih
  st.dataframe(df, use_container_width=True)
else:
  st.warning(
      "🎨 Belum ada data siswa yang tersimpan. Yuk, mulai isi formulir di atas"
      " untuk menghidupkan tabel ini!"
  )
