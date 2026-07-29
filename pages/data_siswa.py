import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL & TOMBOL ---
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

st.markdown("### 📋 Daftar Seluruh Siswa Terdaftar")

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

  # --- DAFTAR BARIS DENGAN TOMBOL EDIT & HAPUS YANG DIPERBAIKI ---
  for row in data_siswa:
    s_id, s_nama, s_nisn, s_jenjang, s_kelas, s_jk = row

    with st.container():
      # Menggunakan proporsi kolom yang lebih luas agar tombol tidak tersembunyi
      cols = st.columns([2.5, 1.8, 0.8, 1, 1, 1, 1])
      cols[0].write(f"**{s_nama}**")
      cols[1].write(f"NISN: {s_nisn}")
      cols[2].write(f"**{s_jenjang}**")
      cols[3].write(f"Kelas: {s_kelas}")
      cols[4].write(f"{s_jk}")

      # Tombol Edit
      with cols[5]:
        if st.button("✏️ Edit", key=f"btn_edit_{s_id}"):
          st.session_state[f"editing_{s_id}"] = True

      # Tombol Hapus
      with cols[6]:
        if st.button("🗑️ Hapus", key=f"btn_hapus_{s_id}", type="primary"):
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute("DELETE FROM siswa WHERE id = ?", (s_id,))
          conn.commit()
          conn.close()
          st.success(f"Data {s_nama} berhasil dihapus!")
          st.rerun()

    # Form Edit Interaktif jika tombol Edit diklik
    if st.session_state.get(f"editing_{s_id}", False):
      with st.form(f"form_edit_{s_id}"):
        st.markdown(f"**Edit Data: {s_nama}**")
        e_nama = st.text_input("Nama Lengkap", value=s_nama, key=f"en_{s_id}")
        e_nisn = st.text_input("NISN", value=s_nisn, key=f"ei_{s_id}")
        e_jenjang = st.selectbox(
            "Jenjang",
            ["KB", "TK", "SD"],
            index=["KB", "TK", "SD"].index(s_jenjang),
            key=f"ej_{s_id}",
        )
        e_kelas = st.text_input("Kelas", value=s_kelas, key=f"ek_{s_id}")
        e_jk = st.selectbox(
            "Jenis Kelamin",
            ["Laki-laki", "Perempuan"],
            index=["Laki-laki", "Perempuan"].index(s_jk),
            key=f"eg_{s_id}",
        )

        col_sub1, col_sub2 = st.columns(2)
        update_btn = col_sub1.form_submit_button("💾 Perbarui Data")
        batal_btn = col_sub2.form_submit_button("❌ Batal")

        if update_btn:
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE siswa SET nama=?, nisn=?, jenjang=?, kelas=?, jk=? WHERE"
              " id=?",
              (e_nama, e_nisn, e_jenjang, e_kelas, e_jk, s_id),
          )
          conn.commit()
          conn.close()
          st.session_state[f"editing_{s_id}"] = False
          st.success("Data berhasil diperbarui!")
          st.rerun()

        if batal_btn:
          st.session_state[f"editing_{s_id}"] = False
          st.rerun()

    st.markdown(
        "<hr style='margin: 5px 0px; border-top: 1px solid #ddd;'>",
        unsafe_allow_html=True,
    )
else:
  st.warning("🎨 Belum ada data siswa yang tersimpan di database.")
