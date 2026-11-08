import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Pendaftaran Kegiatan Mahasiswa"

ACTIVITIES = ["Seminar", "Workshop", "Lomba", "Pelatihan", "Bakti Sosial"]
STUDY_PROGRAMS = ["Informatika", "Sistem Informasi", "Teknik Elektro", "Manajemen", "Akuntansi"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("760x620")
        self.resizable(True, True)

        self._about_window = None
        self.name_var = tk.StringVar()
        self.prodi_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="")
        self.activity_vars = {act: tk.BooleanVar(value=False) for act in ACTIVITIES}

        self._build_menu()
        self._build_ui()
        self.bind("<Return>", self._on_enter)
    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit / Keluar", command=self.destroy, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.open_about)
        menubar.add_cascade(label="Bantuan", menu=help_menu)

        self.config(menu=menubar)
        self.bind_all("<Control-q>", lambda e: self.destroy())
    def _build_ui(self):
        container = ttk.Frame(self, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        title_lbl = ttk.Label(container, text=APP_TITLE, font=("Helvetica", 16, "bold"))
        title_lbl.pack(pady=(0, 10))

        form = ttk.LabelFrame(container, text="Data Mahasiswa", padding=10)
        form.pack(fill=tk.X, pady=5)

        ttk.Label(form, text="Nama:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(form, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(form, text="Program Studi:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        prodi_cb = ttk.Combobox(form, textvariable=self.prodi_var, values=STUDY_PROGRAMS, state="readonly", width=37)
        prodi_cb.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        if STUDY_PROGRAMS:
            prodi_cb.current(0)

        ttk.Label(form, text="Jenis Kelamin:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        gender_frame = ttk.Frame(form)
        gender_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(gender_frame, text="Laki-laki", variable=self.gender_var, value="Laki-laki").pack(side=tk.LEFT, padx=(0, 12))
        ttk.Radiobutton(gender_frame, text="Perempuan", variable=self.gender_var, value="Perempuan").pack(side=tk.LEFT)
        ttk.Label(form, text="Kegiatan:").grid(row=3, column=0, sticky=tk.NW, padx=5, pady=5)
        act_container = ttk.Frame(form)
        act_container.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        cb_frame = ttk.Frame(act_container)
        cb_frame.pack(side=tk.LEFT, anchor=tk.N)
        for act in ACTIVITIES:
            ttk.Checkbutton(cb_frame, text=act, variable=self.activity_vars[act]).pack(anchor=tk.W)

        self.activity_listbox = tk.Listbox(act_container, height=6, width=22, selectmode=tk.MULTIPLE, exportselection=False)
        self.activity_listbox.pack(side=tk.LEFT, padx=(15, 0))
        for act in ACTIVITIES:
            self.activity_listbox.insert(tk.END, act)
        ttk.Label(act_container, text="Pilihan kegiatan (Listbox)").pack(side=tk.LEFT, padx=(5, 0))
        ttk.Label(form, text="Alasan mengikuti:").grid(row=4, column=0, sticky=tk.NW, padx=5, pady=5)
        self.reason_text = tk.Text(form, height=4, width=42)
        self.reason_text.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=8)
        ttk.Button(btn_frame, text="Submit", command=self.submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.LabelFrame(container, text="Ringkasan Pendaftaran", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.info_text = tk.Text(info_frame, height=12, state=tk.DISABLED, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
    def _on_enter(self, event):
        if isinstance(event.widget, tk.Text):
            return
        self.submit()

    def _selected_activities(self):
        selected = [act for act in ACTIVITIES if self.activity_vars[act].get()]
        for idx in self.activity_listbox.curselection():
            act = self.activity_listbox.get(idx)
            if act not in selected:
                selected.append(act)
        return selected

    def submit(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Validasi", "Nama tidak boleh kosong.")
            return

        prodi = self.prodi_var.get()
        gender = self.gender_var.get()
        activities = self._selected_activities()
        reason = self.reason_text.get("1.0", tk.END).strip()

        if not gender:
            messagebox.showwarning("Validasi", "Pilih jenis kelamin.")
            return
        if not activities:
            messagebox.showwarning("Validasi", "Pilih minimal satu kegiatan.")
            return

        summary = (
            "=== RINGKASAN PENDAFTARAN ===\n"
            f"Nama           : {name}\n"
            f"Program Studi  : {prodi}\n"
            f"Jenis Kelamin  : {gender}\n"
            f"Kegiatan       : {', '.join(activities)}\n"
            f"Alasan         : {reason if reason else '-'}\n"
            "=============================\n"
        )

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, summary)
        self.info_text.config(state=tk.DISABLED)

        messagebox.showinfo("Sukses", "Pendaftaran berhasil disimpan.")
    def reset(self):
        self.name_var.set("")
        self.prodi_var.set(STUDY_PROGRAMS[0] if STUDY_PROGRAMS else "")
        self.gender_var.set("")
        for v in self.activity_vars.values():
            v.set(False)
        self.activity_listbox.selection_clear(0, tk.END)
        self.reason_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.DISABLED)
        messagebox.showinfo("Reset", "Form telah direset.")

    def open_about(self):
        if self._about_window is not None and self._about_window.winfo_exists():
            self._about_window.lift()
            return
        win = tk.Toplevel(self)
        win.title("About")
        win.geometry("360x220")
        win.transient(self)
        ttk.Label(win, text=APP_TITLE, font=("Helvetica", 14, "bold")).pack(pady=(15, 5))
        ttk.Label(win, text="Aplikasi Pendaftaran Kegiatan Mahasiswa").pack()
        ttk.Label(win, text="Dibuat dengan Python Tkinter").pack()
        ttk.Label(win, text="Praktikum Sesi 11 - Advanced Widgets & Event Handling").pack(pady=5)
        ttk.Button(win, text="Tutup", command=win.destroy).pack(pady=15)
        self._about_window = win


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
