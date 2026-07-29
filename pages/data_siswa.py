import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL & TOMBOL AKSI ---
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
    .row-card {
        background-color: #fcfcfc;
        border: 1px solid #eaeaea;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
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
        <p>Kelola Data Kelompok Bermain (KB), TK, dan SD dengan Tombol Aksi Langsung</p>
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

st.markdown("### 📋 Daftar Seluruh Siswa & Aksi")

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

  # --- DAFTAR BARIS DENGAN TOMBOL EDIT & HAPUS YANG NYATA ---
  for row in data_siswa:
    s_id, s_nama, s_nisn, s_jenjang, s_kelas, s_jk = row

    with st.container():
      st.markdown('<div class="row-card">', unsafe_allow_html=True)
      # Membagi kolom dengan proporsi stabil agar tombol tampil sempurna
      c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 1.3, 0.7, 0.8, 1, 0.8, 0.8])

      c1.markdown(f"**{s_nama}**")
      c2.markdown(f"NISN: {s_nisn}")
      c3.markdown(f"**{s_jenjang}**")
      c4.markdown(f"Kls: {s_kelas}")
      c5.markdown(f"{s_jk}")

      # Tombol Edit
      with c6:
        if st.button("✏️ Edit", key=f"edit_{s_id}"):
          st.session_state[f"edit_mode_{s_id}"] = True

      # Tombol Hapus
      with c7:
        if st.button("🗑️ Hapus", key=f"hapus_{s_id}"):
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute("DELETE FROM siswa WHERE id = ?", (s_id,))
          conn.commit()
          conn.close()
          st.success(f"Data {s_nama} berhasil dihapus!")
          st.rerun()

      st.markdown("</div>", unsafe_allow_html=True)

    # --- FORM POP-UP / EDIT KETIKA TOMBOL EDIT DIKLIK ---
    if st.session_state.get(f"edit_mode_{s_id}", False):
      with st.form(key=f"form_edit_baris_{s_id}"):
        st.markdown(f"#### ✏️ Perbarui Data: {s_nama}")
        new_nama = st.text_input("Nama Lengkap", value=s_nama)
        new_nisn = st.text_input("NISN", value=s_nisn)
        new_jenjang = st.selectbox(
            "Jenjang",
            ["KB", "TK", "SD"],
            index=["KB", "TK", "SD"].index(s_jenjang),
        )
        new_kelas = st.text_input("Kelas", value=s_kelas)
        new_jk = st.selectbox(
            "Jenis Kelamin",
            ["Laki-laki", "Perempuan"],
            index=["Laki-laki", "Perempuan"].index(s_jk),
        )

        col_f1, col_f2 = st.columns(2)
        simpan_edit = col_f1.form_submit_button("💾 Simpan Perubahan")
        batal_edit = col_f2.form_submit_button("❌ Batal")

        if simpan_edit:
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE siswa SET nama=?, nisn=?, jenjang=?, kelas=?, jk=? WHERE"
              " id=?",
              (new_nama, new_nisn, new_jenjang, new_kelas, new_jk, s_id),
          )
          conn.commit()
          conn.close()
          st.session_state[f"edit_mode_{s_id}"] = False
          st.success("Data berhasil diperbarui!")
          st.rerun()

        if batal_edit:
          st.session_state[f"edit_mode_{s_id}"] = False
          st.rerun()
else:
  st.warning("🎨 Belum ada data siswa yang tersimpan di database.")
