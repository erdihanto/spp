import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)

# --- CSS COLORFUL ---
st.markdown("""
    <style>
    .colorful-header {
        background: linear-gradient(135deg, #FF6B6B, #FFD93D);
        padding: 25px;
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

# --- HEADER ---
st.markdown("""
    <div class="colorful-header">
        <h1>🌟 PUSAT DATA SISWA DIAN WACANA 🌟</h1>
        <p>Kelola Data, Edit Langsung, dan Hapus Data dengan Mudah</p>
    </div>
""", unsafe_allow_html=True)

# --- FORM TAMBAH DATA ---
with st.expander("➕ Klik di sini untuk Tambah Siswa Baru", expanded=True):
  with st.form("form_tambah_siswa"):
    col_a, col_b = st.columns(2)
    with col_a:
      nama = st.text_input("👤 Nama Lengkap")
      nisn = st.text_input("🆔 NISN / No. Induk")
      jenjang = st.selectbox("🎓 Jenjang", ["KB", "TK", "SD"])
    with col_b:
      kelas = st.text_input("🏫 Kelas")
      jk = st.selectbox("⚧ Jenis Kelamin", ["Laki-laki", "Perempuan"])

    submit = st.form_submit_button(
        "🚀 Simpan Data Baru", use_container_width=True
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
        st.success("🎉 Data berhasil disimpan!")
        st.rerun()
      else:
        st.error("⚠️ Mohon isi semua kolom!")

st.markdown("---")

# --- AMBIL DATA ---
conn = sqlite3.connect("dian_wacana.db")
cursor = conn.cursor()
cursor.execute("SELECT id, nama, nisn, jenjang, kelas, jk FROM siswa")
data_siswa = cursor.fetchall()
conn.close()

st.markdown("### 📋 Tabel Data Siswa (Bisa Diedit & Dihapus Langsung)")

if data_siswa:
  df = pd.DataFrame(
      data_siswa,
      columns=["ID", "Nama Lengkap", "NISN", "Jenjang", "Kelas", "L/P"],
  )

  st.info(
      "💡 **Cara Edit & Hapus:**\n"
      "1. **Edit:** Klik langsung teks di kolom tabel mana saja lalu ubah.\n"
      "2. **Hapus:** Sorot baris tabel lalu klik ikon tempat sampah (🗑️) di"
      " sebelah kiri baris.\n"
      "3. Setelah selesai, klik tombol **💾 Simpan Perubahan ke Database** di"
      " bawah."
  )

  # Tabel interaktif bawaan Streamlit yang menyediakan fitur edit sel dan hapus baris secara instan
  edited_df = st.data_editor(
      df,
      num_rows="dynamic",
      use_container_width=True,
      hide_index=True,
      key="editor_siswa",
      column_config={
          "ID": st.column_config.NumberColumn("ID", disabled=True),
          "Jenjang": st.column_config.SelectboxColumn(
              "Jenjang", options=["KB", "TK", "SD"], required=True
          ),
          "L/P": st.column_config.SelectboxColumn(
              "Jenis Kelamin",
              options=["Laki-laki", "Perempuan"],
              required=True,
          ),
      },
  )

  if st.button(
      "💾 Simpan Perubahan ke Database", type="primary", use_container_width=True
  ):
    conn = sqlite3.connect("dian_wacana.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM siswa")
    for _, row in edited_df.iterrows():
      cursor.execute(
          "INSERT INTO siswa (id, nama, nisn, jenjang, kelas, jk) VALUES (?, ?,"
          " ?, ?, ?, ?)",
          (
              row["ID"],
              row["Nama Lengkap"],
              row["NISN"],
              row["Jenjang"],
              row["Kelas"],
              row["L/P"],
          ),
      )
    conn.commit()
    conn.close()
    st.success("✅ Perubahan berhasil disimpan ke database!")
    st.rerun()

else:
  st.warning("🎨 Belum ada data siswa di database.")
