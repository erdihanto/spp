import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Siswa - Dian Wacana", page_icon="📚")


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

st.title("📚 Manajemen Data Siswa TK-KB-SD Dian Wacana")

# --- Form Tambah Data di Sidebar ---
st.sidebar.header("Tambah Siswa Baru")
with st.sidebar.form("form_tambah"):
  nama = st.text_input("Nama Lengkap")
  nisn = st.text_input("NISN / No. Induk")
  jenjang = st.selectbox("Jenjang", ["KB", "TK", "SD"])
  kelas = st.text_input("Kelas")
  jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
  submit = st.form_submit_button("Simpan Data")

  if submit:
    if nama and nisn and kelas:
      conn = sqlite3.connect("dian_wacana.db")
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO siswa (nama, nisn, jenjang, kelas, jk) VALUES (?, ?, ?,"
          " ?, ?)",
          (nama, nisn, jenjang, kelas, jk),
      )
      conn.commit()
      conn.close()
      st.sidebar.success("Data siswa berhasil ditambahkan!")
      st.rerun()
    else:
      st.sidebar.error("Semua kolom harus diisi!")

# --- Menampilkan Data dalam Tabel ---
st.subheader("Daftar Siswa Terdaftar")
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
  st.dataframe(df, use_container_width=True)
else:
  st.info("Belum ada data siswa.")
