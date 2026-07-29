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
    .action-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff6b6b;
        margin-top: 20px;
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
        <p>Kelola Data Kelompok Bermain (KB), TK, dan SD</p>
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

  # Tampilkan Tabel Utama
  st.dataframe(df, use_container_width=True, hide_index=True)

  # --- PANEL KONTROL AKSI (DIJAMIN MUNCUL) ---
  st.markdown('<div class="action-box">', unsafe_allow_html=True)
  st.markdown(
      "### ⚙️ Panel Aksi (Edit & Hapus Data Berdasarkan ID dari Tabel)"
  )

  # Membuat list pilihan berupa ID beserta Nama Siswa
  pilihan_siswa = {
      f"ID {row['ID']} - {row['Nama Lengkap']} ({row['Jenjang']} - Kelas {row['Kelas']})": row[
          "ID"
      ]
      for index, row in df.iterrows()
  }

  selected_label = st.selectbox(
      "Pilih Siswa yang ingin diedit atau dihapus:",
      options=list(pilihan_siswa.keys()),
  )

  if selected_label:
    target_id = pilihan_siswa[selected_label]

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
      if st.button("✏️ Edit Siswa Ini", use_container_width=True):
        st.session_state["edit_target_id"] = target_id
        st.rerun()

    with col_btn2:
      if st.button(
          "🗑️ Hapus Siswa Ini", type="primary", use_container_width=True
      ):
        conn = sqlite3.connect("dian_wacana.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM siswa WHERE id = ?", (target_id,))
        conn.commit()
        conn.close()
        if "edit_target_id" in st.session_state:
          del st.session_state["edit_target_id"]
        st.success("✅ Data siswa berhasil dihapus!")
        st.rerun()

  st.markdown("</div>", unsafe_allow_html=True)

  # --- FORM EDIT YANG MUNCUL KETIKA TOMBOL EDIT DIKLIK ---
  if st.session_state.get("edit_target_id"):
    current_edit_id = st.session_state["edit_target_id"]

    # Ambil data spesifik siswa yang dipilih
    conn = sqlite3.connect("dian_wacana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nama, nisn, jenjang, kelas, jk FROM siswa WHERE id = ?",
        (current_edit_id,),
    )
    edit_data = cursor.fetchone()
    conn.close()

    if edit_data:
      e_nama_lama, e_nisn_lama, e_jenjang_lama, e_kelas_lama, e_jk_lama = (
          edit_data
      )

      st.markdown("<br>", unsafe_allow_html=True)
      with st.form(key=f"form_edit_id_{current_edit_id}"):
        st.markdown(
            f"### ✏️ Formulir Perubahan Data (ID: {current_edit_id})"
        )
        new_nama = st.text_input("Nama Lengkap", value=e_nama_lama)
        new_nisn = st.text_input("NISN / No. Induk", value=e_nisn_lama)
        new_jenjang = st.selectbox(
            "Jenjang Sekolah",
            ["KB", "TK", "SD"],
            index=["KB", "TK", "SD"].index(e_jenjang_lama),
        )
        new_kelas = st.text_input("Kelas", value=e_kelas_lama)
        new_jk = st.selectbox(
            "Jenis Kelamin",
            ["Laki-laki", "Perempuan"],
            index=["Laki-laki", "Perempuan"].index(e_jk_lama),
        )

        sub_col1, sub_col2 = st.columns(2)
        submit_update = sub_col1.form_submit_button(
            "💾 Simpan Perubahan", use_container_width=True
        )
        cancel_update = sub_col2.form_submit_button(
            "❌ Batal", use_container_width=True
        )

        if submit_update:
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE siswa SET nama=?, nisn=?, jenjang=?, kelas=?, jk=? WHERE"
              " id=?",
              (
                  new_nama,
                  new_nisn,
                  new_jenjang,
                  new_kelas,
                  new_jk,
                  current_edit_id,
              ),
          )
          conn.commit()
          conn.close()
          del st.session_state["edit_target_id"]
          st.success("🎉 Data siswa berhasil diperbarui!")
          st.rerun()

        if cancel_update:
          del st.session_state["edit_target_id"]
          st.rerun()
else:
  st.warning("🎨 Belum ada data siswa yang tersimpan di database.")
