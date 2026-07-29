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
    .box-action {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #ff6b6b;
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
        <p>Kelola Data Kelompok Bermain (KB), TK, dan SD dengan Mudah & Aman</p>
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

  # --- MENAMPILKAN TABEL DENGAN FITUR SELECTION (UNTUK MUNCULKAN TOMBOL AKSI) ---
  st.info(
      "👇 **Petunjuk Aksi:** Masukkan **ID Siswa** yang ingin diedit atau dihapus"
      " pada kolom panel di bawah ini, lalu klik tombol **Edit** atau"
      " **Hapus**."
  )

  # Tampilkan tabel interaktif
  event = st.dataframe(
      df,
      use_container_width=True,
      hide_index=True,
      selection_mode="single-row",
      on_select="rerun",
  )

  # Ambil ID baris yang sedang dipilih di tabel
  selected_rows = event.selection.get("rows", [])

  st.markdown('<div class="box-action">', unsafe_allow_html=True)
  st.markdown("### ⚙️ Panel Aksi Data Terpilih")

  if selected_rows:
    selected_index = selected_rows[0]
    selected_id = int(df.iloc[selected_index]["ID"])
    selected_nama = df.iloc[selected_index]["Nama Lengkap"]

    st.success(
        f"✅ Siswa dipilih: **{selected_nama}** (ID Database: {selected_id})"
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      if st.button("✏️ Edit Data Terpilih", use_container_width=True):
        st.session_state["active_edit_id"] = selected_id
        st.rerun()

    with col_btn2:
      if st.button(
          "🗑️ Hapus Data Terpilih",
          type="primary",
          use_container_width=True,
      ):
        conn = sqlite3.connect("dian_wacana.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM siswa WHERE id = ?", (selected_id,))
        conn.commit()
        conn.close()
        st.success(f"Data siswa {selected_nama} berhasil dihapus!")
        if "active_edit_id" in st.session_state:
          del st.session_state["active_edit_id"]
        st.rerun()
  else:
    st.warning(
        "⚠️ Belum ada baris tabel yang diklik/dipilih. Silakan klik salah satu"
        " baris pada tabel di atas untuk memunculkan tombol Edit & Hapus."
    )
  st.markdown("</div>", unsafe_allow_html=True)

  # --- FORM EDIT MUNCUL JIKA TOMBOL EDIT DIKLIK ---
  if st.session_state.get("active_edit_id"):
    edit_id = st.session_state["active_edit_id"]

    # Ambil data lama berdasarkan ID
    conn = sqlite3.connect("dian_wacana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nama, nisn, jenjang, kelas, jk FROM siswa WHERE id = ?",
        (edit_id,),
    )
    current_data = cursor.fetchone()
    conn.close()

    if current_data:
      c_nama, c_nisn, c_jenjang, c_kelas, c_jk = current_data

      st.markdown("<br>", unsafe_allow_html=True)
      with st.form(key=f"form_edit_db_{edit_id}"):
        st.markdown(f"### ✏️ Form Edit Data: {c_nama} (ID: {edit_id})")
        e_nama = st.text_input("Nama Lengkap", value=c_nama)
        e_nisn = st.text_input("NISN", value=c_nisn)
        e_jenjang = st.selectbox(
            "Jenjang",
            ["KB", "TK", "SD"],
            index=["KB", "TK", "SD"].index(c_jenjang),
        )
        e_kelas = st.text_input("Kelas", value=c_kelas)
        e_jk = st.selectbox(
            "Jenis Kelamin",
            ["Laki-laki", "Perempuan"],
            index=["Laki-laki", "Perempuan"].index(c_jk),
        )

        col_f1, col_f2 = st.columns(2)
        save_btn = col_f1.form_submit_button(
            "💾 Simpan Perubahan", use_container_width=True
        )
        cancel_btn = col_f2.form_submit_button(
            "❌ Batal", use_container_width=True
        )

        if save_btn:
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE siswa SET nama=?, nisn=?, jenjang=?, kelas=?, jk=? WHERE"
              " id=?",
              (e_nama, e_nisn, e_jenjang, e_kelas, e_jk, edit_id),
          )
          conn.commit()
          conn.close()
          del st.session_state["active_edit_id"]
          st.success("✅ Perubahan data berhasil disimpan!")
          st.rerun()

        if cancel_btn:
          del st.session_state["active_edit_id"]
          st.rerun()
else:
  st.warning("🎨 Belum ada data siswa yang tersimpan di database.")
