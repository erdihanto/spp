from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

# --- Inisialisasi Database ---
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


# --- Fungsi-Fungsi Aplikasi ---
def muat_data():
  for row in tree.get_children():
    tree.delete(row)
  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM siswa")
  for row in cursor.fetchall():
    tree.insert("", END, values=row)
  conn.close()


def tambah_data():
  if not e_nama.get() or not e_nisn.get() or not e_kelas.get():
    messagebox.showerror("Peringatan", "Semua kolom harus diisi!")
    return

  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO siswa (nama, nisn, jenjang, kelas, jk) VALUES (?, ?, ?, ?,"
      " ?)",
      (
          e_nama.get(),
          e_nisn.get(),
          combo_jenjang.get(),
          e_kelas.get(),
          combo_jk.get(),
      ),
  )
  conn.commit()
  conn.close()
  muat_data()
  bersihkan_form()
  messagebox.showinfo("Sukses", "Data siswa berhasil ditambahkan!")


def hapus_data():
  selected_item = tree.selection()
  if not selected_item:
    messagebox.showerror("Peringatan", "Pilih data yang ingin dihapus!")
    return

  item_id = tree.item(selected_item)["values"][0]
  conn = sqlite3.connect("dian_wacana.db")
  cursor = conn.cursor()
  cursor.execute("DELETE FROM siswa WHERE id=?", (item_id,))
  conn.commit()
  conn.close()
  muat_data()
  messagebox.showinfo("Sukses", "Data berhasil dihapus!")


def bersihkan_form():
  e_nama.delete(0, END)
  e_nisn.delete(0, END)
  e_kelas.delete(0, END)


# --- Desain Tampilan (GUI) ---
root = Tk()
root.title("Aplikasi Pendataan Siswa TK-KB-SD Dian Wacana")
root.geometry("750x450")

# Label Judul
Label(
    root,
    text="Data Siswa TK - KB - SD Dian Wacana",
    font=("Arial", 14, "bold"),
).pack(pady=10)

# Frame Input
frame_input = Frame(root)
frame_input.pack(pady=5)

Label(frame_input, text="Nama Lengkap:").grid(
    row=0, column=0, sticky=W, padx=5, pady=2
)
e_nama = Entry(frame_input, width=25)
e_nama.grid(row=0, column=1, padx=5, pady=2)

Label(frame_input, text="NISN/No. Induk:").grid(
    row=1, column=0, sticky=W, padx=5, pady=2
)
e_nisn = Entry(frame_input, width=25)
e_nisn.grid(row=1, column=1, padx=5, pady=2)

Label(frame_input, text="Jenjang:").grid(
    row=2, column=0, sticky=W, padx=5, pady=2
)
combo_jenjang = ttk.Combobox(
    frame_input, values=["KB", "TK", "SD"], width=23, state="readonly"
)
combo_jenjang.grid(row=2, column=1, padx=5, pady=2)
combo_jenjang.current(2)

Label(frame_input, text="Kelas:").grid(
    row=0, column=2, sticky=W, padx=5, pady=2
)
e_kelas = Entry(frame_input, width=25)
e_kelas.grid(row=0, column=3, padx=5, pady=2)

Label(frame_input, text="Jenis Kelamin:").grid(
    row=1, column=2, sticky=W, padx=5, pady=2
)
combo_jk = ttk.Combobox(
    frame_input, values=["Laki-laki", "Perempuan"], width=23, state="readonly"
)
combo_jk.grid(row=1, column=3, padx=5, pady=2)
combo_jk.current(0)

# Tombol Aksi
frame_btn = Frame(root)
frame_btn.pack(pady=10)

Button(
    frame_btn,
    text="Tambah Data",
    bg="green",
    fg="white",
    width=15,
    command=tambah_data,
).grid(row=0, column=0, padx=5)
Button(
    frame_btn,
    text="Hapus Terpilih",
    bg="red",
    fg="white",
    width=15,
    command=hapus_data,
).grid(row=0, column=1, padx=5)

# Tabel Data (Treeview)
columns = ("ID", "Nama", "NISN", "Jenjang", "Kelas", "L/P")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
  tree.heading(col, text=col)
  tree.column(col, width=100)

tree.pack(pady=10, fill=BOTH, expand=True)

# Muat data awal saat aplikasi dibuka
muat_data()

root.mainloop()
