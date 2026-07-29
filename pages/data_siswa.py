import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL ---
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

# --- FORM TAMBAH DATA (DALAM EXPANDER) ---
with st.expander("➕ Klik di sini untuk Tambah Siswa Baru", expanded=False):
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

# --- AMBIL DATA DARI DATABASE ---
conn = sqlite3.connect("dian_wacana.db")
cursor = conn.cursor()
cursor.execute("SELECT id, nama, nisn, jenjang, kelas, jk FROM siswa")
data_siswa = cursor.fetchall()
conn.close()

st.markdown("### 📋 Daftar & Pengelolaan Data Siswa")

if data_siswa:
  df = pd.DataFrame(
      data_siswa,
      columns=["ID", "Nama Lengkap", "NISN", "Jenjang", "Kelas", "L/P"],
  )

  # Statistik Singkat
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
  st.info(
      "💡 **Tips:** Anda dapat mengedit langsung teks di dalam tabel di bawah ini,"
      " lalu klik tombol **Simpan Perubahan**."
  )

  # --- MENGGUNAKAN DATA EDITOR AGAR MUDAH DIEDIT & DIHAPUS ---
  edited_df = st.data_editor(
      df,
      num_rows="dynamic",
      use_container_width=True,
      key="datatable_siswa",
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

  col_btn1, col_btn2 = st.columns(2)

  # Tombol Simpan Perubahan (Edit)
  with col_btn1:
    if st.button(
        "💾 Simpan Perubahan Data",
        type="primary",
        use_container_width=True,
    ):
      conn = sqlite3.connect("dian_wacana.db")
      cursor = conn.cursor()
      # Kosongkan tabel lalu masukkan ulang data yang sudah diedit/dihapus
      cursor.execute("DELETE FROM siswa")
      for index, row in edited_df.iterrows():
        cursor.execute(
            "INSERT INTO siswa (id, nama, nisn, jenjang, kelas, jk) VALUES (?,"
            " ?, ?, ?, ?, ?)",
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
      st.success("✅ Perubahan data berhasil disimpan ke database!")
      st.rerun()

  # Tombol Hapus Baris Terpilih
  with col_btn2:
    if st.button("🗑️ Hapus Baris / Reset", use_container_width=True):
      st.warning(
          "Untuk menghapus baris, gunakan ikon tempat sampah di sebelah kiri"
          " baris tabel, lalu klik 'Simpan Perubahan Data'."
      )

else:
  st.warning("🎨 Belum ada data siswa yang tersimpan di database.")
