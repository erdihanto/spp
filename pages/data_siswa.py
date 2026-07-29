import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manajemen Data Siswa - Dian Wacana", page_icon="📚", layout="wide"
)


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

st.title("📚 Manajemen Data Siswa - Dian Wacana")
st.write(
    "Gunakan halaman ini untuk menambah, melihat, dan mengelola data siswa"
    " dengan tombol interaktif."
)

# --- 1. FORM TAMBAH DATA ---
with st.expander("➕ Tambah Data Siswa Baru", expanded=True):
  with st.form("tambah_siswa_form"):
    nama = st.text_input("Nama Lengkap")
    nisn = st.text_input("NISN")
    jenjang = st.selectbox("Jenjang", ["KB", "TK", "SD"])
    kelas = st.text_input("Kelas")
    jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    submitted = st.form_submit_button("Simpan Data")
    if submitted:
      if nama and nisn and kelas:
        conn = sqlite3.connect("dian_wacana.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO siswa (nama, nisn, jenjang, kelas, jk) VALUES (?, ?, ?, ?, ?)",
            (nama, nisn, jenjang, kelas, jk),
        )
        conn.commit()
        conn.close()
        st.success("Data berhasil ditambahkan!")
        st.rerun()
      else:
        st.error("Mohon isi semua kolom dengan lengkap.")

st.markdown("---")

# --- 2. AMBIL DAN TAMPILKAN DATA ---
conn = sqlite3.connect("dian_wacana.db")
cursor = conn.cursor()
cursor.execute("SELECT id, nama, nisn, jenjang, kelas, jk FROM siswa")
rows = cursor.fetchall()
conn.close()

st.subheader("Daftar Siswa Tersimpan")

if rows:
  df = pd.DataFrame(
      rows, columns=["ID", "Nama", "NISN", "Jenjang", "Kelas", "L/P"]
  )
  st.dataframe(df, use_container_width=True)
else:
  st.warning(
      "Belum ada data siswa di dalam database. Silakan isi form di atas terlebih"
      " dahulu."
  )

st.markdown("---")
st.markdown("### ⚙️ Menu Aksi Data (Edit & Hapus)")

# --- 3. MENU AKSI & TOMBOL (DIJAMIN SELALU MUNCUL) ---
if rows:
  id_list = df["ID"].tolist()
  selected_id = st.selectbox(
      "Pilih ID Siswa untuk diedit atau dihapus:", options=id_list
  )

  if selected_id:
    conn = sqlite3.connect("dian_wacana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nama, nisn, jenjang, kelas, jk FROM siswa WHERE id = ?",
        (selected_id,),
    )
    s_data = cursor.fetchone()
    conn.close()

    if s_data:
      s_nama, s_nisn, s_jenjang, s_kelas, s_jk = s_data

      col1, col2 = st.columns(2)

      with col1:
        if st.button("✏️ Edit Siswa Terpilih", use_container_width=True):
          st.session_state["edit_id"] = selected_id
          st.rerun()

      with col2:
        if st.button("🗑️ Hapus Siswa Terpilih", use_container_width=True):
          conn = sqlite3.connect("dian_wacana.db")
          cursor = conn.cursor()
          cursor.execute("DELETE FROM siswa WHERE id = ?", (selected_id,))
          conn.commit()
          conn.close()
          if "edit_id" in st.session_state:
            del st.session_state["edit_id"]
          st.success(f"Data siswa dengan ID {selected_id} berhasil dihapus!")
          st.rerun()
else:
  st.info(
      "Tombol aksi (Edit & Hapus) akan aktif otomatis setelah ada data siswa"
      " yang tersimpan."
  )

# --- 4. FORM EDIT (MUNCUL JIKA TOMBOL EDIT DIKLIK) ---
if st.session_state.get("edit_id"):
  current_edit_id = st.session_state["edit_id"]

  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT nama, nisn, jenjang, kelas, jk FROM siswa WHERE id = ?",
      (current_edit_id,),
  )
  edit_row = cursor.fetchone()
  conn.close()

  if edit_row:
    e_nama, e_nisn, e_jenjang, e_kelas, e_jk = edit_row

    st.markdown("---")
    st.markdown(f"#### 📝 Edit Data Siswa (ID: {current_edit_id})")

    with st.form("form_edit_data"):
      new_nama = st.text_input("Nama Lengkap", value=e_nama)
      new_nisn = st.text_input("NISN", value=e_nisn)
      new_jenjang = st.selectbox(
          "Jenjang",
          ["KB", "TK", "SD"],
          index=["KB", "TK", "SD"].index(e_jenjang),
      )
      new_kelas = st.text_input("Kelas", value=e_kelas)
      new_jk = st.selectbox(
          "Jenis Kelamin",
          ["Laki-laki", "Perempuan"],
          index=["Laki-laki", "Perempuan"].index(e_jk),
      )

      col_a, col_b = st.columns(2)
      update_btn = col_a.form_submit_button(
          "Simpan Perubahan", use_container_width=True
      )
      cancel_btn = col_b.form_submit_button("Batal", use_container_width=True)

      if update_btn:
        conn = sqlite3.connect("dian_wacana.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE siswa SET nama=?, nisn=?, jenjang=?, kelas=?, jk=? WHERE id=?",
            (new_nama, new_nisn, new_jenjang, new_kelas, new_jk, current_edit_id),
        )
        conn.commit()
        conn.close()
        del st.session_state["edit_id"]
        st.success("Data berhasil diperbarui!")
        st.rerun()

      if cancel_btn:
        del st.session_state["edit_id"]
        st.rerun()
