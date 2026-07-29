import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Siswa - Dian Wacana", page_icon="📚")


# --- Inisialisasi Database (Hanya ada di file halaman data siswa) ---
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
st.write("Gunakan formulir di bawah ini untuk menambahkan data siswa baru.")

# --- FORM TAMBAH DATA DI TENGAH (CENTER) ---
with st.form("form_tambah_siswa_tengah"):
  st.subheader("Formulir Tambah Siswa Baru")

  col_a, col_b = st.columns(2)
  with col_a:
    nama = st.text_input("Nama Lengkap")
    nisn = st.text_input("NISN / No. Induk")
    jenjang = st.selectbox("Jenjang", ["KB", "TK", "SD"])
  with col_b:
    kelas = st.text_input("Kelas")
    jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

  submit = st.form_submit_button("Simpan Data Siswa")

  if submit:
    if nama and nisn and kelas:
      conn = sqlite3.connect("dian_wacana.db")
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO siswa (nama, nisn, jenjang, kelas, jk) VALUES (?, ?, ?, ?,"
          " ?)",
          (nama, nisn, jenjang, kelas, jk),
      )
      conn.commit()
      conn.close()
      st.success("Data siswa berhasil ditambahkan!")
    else:
      st.error("Semua kolom harus diisi!")

st.markdown("---")

# --- TOMBOL VIEW DATA & TABEL DI BAWAHNYA ---
st.subheader("Data Siswa Terdaftar")

# Tombol untuk melihat/memuat data
if st.button("👁️ View Data Siswa"):
  st.session_state["tampilkan_data"] = True

# Cek apakah tombol view data sudah pernah diklik
if st.session_state.get("tampilkan_data", False):
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
    st.info("Belum ada data siswa di dalam database.")
else:
  st.write(
      "Klik tombol **View Data Siswa** di atas untuk menampilkan daftar siswa."
  )
