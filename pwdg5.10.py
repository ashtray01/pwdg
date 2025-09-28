import tkinter as tk
from tkinter import ttk, messagebox
import string, random

EXCLUDED_CHARS = "Il0oO"
DEFAULT_SPECIAL_CHARS = "!@#$%^&*()_+-"

THEMES = {
    "Dark": {
        'background': '#2d2d2d', 'foreground': '#ffffff',
        'button_bg': '#3d3d3d', 'button_fg': '#ffffff',
        'entry_bg': '#404040', 'entry_fg': '#ffffff',
        'slider_bg': '#404040', 'slider_trough': '#505050',
        'success': '#4CAF50'
    },
    "Light": {
        'background': '#ffffff',
        'foreground': '#000000',
        'button_bg': '#e0e0e0',
        'button_fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'slider_bg': '#d0d0d0',
        'slider_trough': '#b0b0b0',
        'success': '#2e7d32'
    },
    "Pink": {
        'background': '#ffe6f0', 'foreground': '#402030',
        'button_bg': '#ffb6c1', 'button_fg': '#402030',
        'entry_bg': '#fff0f5', 'entry_fg': '#402030',
        'slider_bg': '#ffd6e6', 'slider_trough': '#ff99cc',
        'success': '#ff69b4'
    },
    "Green": {
        'background': '#e6ffe6', 'foreground': '#204020',
        'button_bg': '#b6ffb6', 'button_fg': '#204020',
        'entry_bg': '#f0fff0', 'entry_fg': '#204020',
        'slider_bg': '#c8facc', 'slider_trough': '#80e080',
        'success': '#32cd32'
    },
    "Red": {
        'background': '#ffe6e6', 'foreground': '#401010',
        'button_bg': '#ffb6b6', 'button_fg': '#401010',
        'entry_bg': '#fff0f0', 'entry_fg': '#401010',
        'slider_bg': '#ffc0c0', 'slider_trough': '#ff8080',
        'success': '#ff3030'
    },
    "Blue": {
        'background': '#e6f2ff', 'foreground': '#103050',
        'button_bg': '#add8e6', 'button_fg': '#103050',
        'entry_bg': '#f0f8ff', 'entry_fg': '#103050',
        'slider_bg': '#b0e0e6', 'slider_trough': '#87ceeb',
        'success': '#1e90ff'
    },
    "Purple": {
        'background': '#f5e6ff', 'foreground': '#301040',
        'button_bg': '#d8b6ff', 'button_fg': '#301040',
        'entry_bg': '#f8f0ff', 'entry_fg': '#301040',
        'slider_bg': '#e0ccff', 'slider_trough': '#c080ff',
        'success': '#9370db'
    },
    "Orange": {
        'background': '#fff2e6', 'foreground': '#502010',
        'button_bg': '#ffd8b6', 'button_fg': '#502010',
        'entry_bg': '#fff8f0', 'entry_fg': '#502010',
        'slider_bg': '#ffe0cc', 'slider_trough': '#ffb080',
        'success': '#ff8c00'
    },
    "Cyber": {
        'background': '#0f0f1b', 'foreground': '#00ffcc',
        'button_bg': '#1a1a2e', 'button_fg': '#00ffcc',
        'entry_bg': '#16213e', 'entry_fg': '#00ffcc',
        'slider_bg': '#0f3460', 'slider_trough': '#1a5fb4',
        'success': '#00ff41'
    },
    "Terminal": {
        'background': '#000000', 'foreground': '#00ff00',
        'button_bg': '#111111', 'button_fg': '#00ff00',
        'entry_bg': '#001100', 'entry_fg': '#00ff00',
        'slider_bg': '#002200', 'slider_trough': '#004400',
        'success': '#33ff33'
    }
}

class PwdgApp:
    def __init__(self, master):
        self.master = master
        self.current_theme = "Dark"
        self.theme_popup = None
        self._in_taskbar_mode = False
        self._taskbar_var = tk.BooleanVar(value=False)
        self.master.geometry("185x280+200+200")
        self.master.minsize(185, 250)
        self.master.maxsize(185,500)
        self.master.overrideredirect(True)
        self.create_title_bar(self.master, "pwdg", self.quit_app)
        self.setup_style()
        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.master.bind("<Button-3>", self.show_context_menu)

    # ===== Выход =====
    def quit_app(self):
        self.master.quit()

    # ===== Переключение режима панели задач =====
    def toggle_taskbar_visibility(self):
       current_x = self.master.winfo_x()
       current_y = self.master.winfo_y()
       current_height = self.master.winfo_height()
       geom = f"185x{current_height}+{current_x}+{current_y}"

       self.master.withdraw()
       new_mode = not self._in_taskbar_mode
       self.master.overrideredirect(not new_mode)
       self.master.geometry(geom)
       self.master.deiconify()
       self._in_taskbar_mode = new_mode
       self._taskbar_var.set(new_mode)

    # ===== Контекстное меню по ПКМ =====
    def show_context_menu(self, event):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Exit", command=self.quit_app)
        menu.add_command(label="Settings", command=self.open_settings)
        menu.add_checkbutton(
            label="Show in Taskbar",
            variable=self._taskbar_var,
            command=self.toggle_taskbar_visibility
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_settings(self):
        messagebox.showinfo("Settings", "Settings panel (not implemented yet)")

    # ===== Кастомный заголовок с перетаскиванием =====
    def create_title_bar(self, window, title, close_cmd):
        bar = tk.Frame(window, bg="#333333")
        bar.pack(fill=tk.X)
        lbl = tk.Label(bar, text=title, bg="#333333", fg="white",
                       font=("Segoe UI", 10, "bold"), padx=8, pady=3)
        lbl.pack(side=tk.LEFT)

        close = tk.Label(bar, text="✖", bg="#333333", fg="white",
                         padx=5, pady=3, cursor="hand2")
        close.pack(side=tk.RIGHT)

        def start_move(e):
            window.x = e.x
            window.y = e.y
        def do_move(e):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")

        bar.bind("<ButtonPress-1>", start_move)
        bar.bind("<B1-Motion>", do_move)
        close.bind("<Button-1>", lambda e: close_cmd())

    # ===== Стиль =====
    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

    def apply_theme(self, name):
        t = THEMES[name]
        self.master.configure(bg=t['background'])
        self.style.configure('.', background=t['background'], foreground=t['foreground'])
        self.style.configure('TFrame', background=t['background'])
        self.style.configure('TLabel', background=t['background'], foreground=t['foreground'])
        self.style.configure('TButton', background=t['button_bg'], foreground=t['button_fg'])
        self.style.configure('TEntry', fieldbackground=t['entry_bg'], foreground=t['entry_fg'],
                             insertcolor=t['foreground'])
        self.style.configure('Horizontal.TScale', background=t['slider_bg'], troughcolor=t['slider_trough'])
        # Обновляем tk.Label вручную
        self.password_label.config(bg=t['background'], fg=t['foreground'])

        if self.theme_popup and tk.Toplevel.winfo_exists(self.theme_popup):
            self.theme_popup.configure(bg=t['background'])

    # ===== UI =====
    def update_length_display(self, value=None):
        current_length = int(round(float(self.length_scale.get())))
        self.length_label.config(text=f"Length: {current_length}")

    def setup_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        lf = ttk.Frame(frame)
        lf.pack(fill=tk.X, pady=5)
        self.length_label = ttk.Label(lf, text="Length: 12")
        self.length_label.pack(side=tk.TOP)
        self.length_scale = ttk.Scale(lf, from_=8, to=64, orient=tk.HORIZONTAL,
                                      command=self.update_length_display)
        self.length_scale.set(12)
        self.length_scale.pack(fill=tk.X)

        cf = ttk.Frame(frame)
        cf.pack(fill=tk.X, pady=5)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_num = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        ttk.Checkbutton(cf, text="A-Z", variable=self.use_upper).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(cf, text="a-z", variable=self.use_lower).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(cf, text="0-9", variable=self.use_num).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(cf, text="Special", variable=self.use_special,
                        command=self.toggle_special_entry).grid(row=1, column=1, sticky="w")

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill=tk.X, pady=(3, 5))
        self.special_entry = ttk.Entry(entry_frame, width=20)  # Ограничение ширины
        self.special_entry.insert(0, DEFAULT_SPECIAL_CHARS)
        self.special_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.theme_btn = ttk.Button(entry_frame, text="+", width=2, command=self.open_theme_popup)
        self.theme_btn.pack(side=tk.RIGHT, padx=(5, 0))
        self.toggle_special_entry()

        bf = ttk.Frame(frame)
        bf.pack(fill=tk.X, pady=5)
        ttk.Button(bf, text="Generate", command=self.generate_password).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(bf, text="Copy", command=self.copy_password).pack(side=tk.LEFT)

        self.password_label = tk.Label(
            frame,
            text="",
            font=("Consolas", 10, "bold"),
            wraplength=160,  # для учета отступов пароля
            justify=tk.CENTER,
            bg=THEMES[self.current_theme]['background'],
            fg=THEMES[self.current_theme]['foreground']
        )
        self.password_label.pack(fill=tk.X, pady=(10, 0))

    def toggle_special_entry(self):
        state = "normal" if self.use_special.get() else "disabled"
        self.special_entry.config(state=state)

    def validate_inputs(self):
        if not any([self.use_upper.get(), self.use_lower.get(),
                    self.use_num.get(), self.use_special.get()]):
            messagebox.showwarning("Warning", "Select at least one character type!")
            return False
        if self.use_special.get() and not self.special_entry.get().strip():
            messagebox.showwarning("Warning", "Enter special characters!")
            return False
        return True

    # ===== Password =====
    def generate_password(self):
        if not self.validate_inputs():
            return
        length = int(self.length_scale.get())
        char_sets = []
        if self.use_upper.get():
            char_sets.append([c for c in string.ascii_uppercase if c not in EXCLUDED_CHARS])
        if self.use_lower.get():
            char_sets.append([c for c in string.ascii_lowercase if c not in EXCLUDED_CHARS])
        if self.use_num.get():
            char_sets.append([c for c in string.digits if c not in EXCLUDED_CHARS])
        if self.use_special.get():
            sp = [c for c in self.special_entry.get().strip() if c not in EXCLUDED_CHARS]
            if not sp:
                messagebox.showwarning("Warning", "No valid special characters")
                return
            char_sets.append(sp)
        if length < len(char_sets):
            messagebox.showwarning("Warning", f"Minimum length: {len(char_sets)}")
            return

        pwd = [random.choice(s) for s in char_sets]
        remaining = length - len(pwd)
        all_chars = [c for s in char_sets for c in s]
        pwd.extend(random.choices(all_chars, k=remaining))
        random.shuffle(pwd)
        pwd_str = "".join(pwd)
        self.password_label.config(text=pwd_str)

    def copy_password(self):
        pwd = self.password_label.cget("text")
        if not pwd:
            messagebox.showwarning("Warning", "No password to copy!")
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(pwd)
        t = THEMES[self.current_theme]
        self.password_label.config(fg=t['success'])
        self.master.after(300, lambda: self.password_label.config(fg=t['foreground']))

    # ===== Theme popup =====
    def open_theme_popup(self):
        if self.theme_popup and tk.Toplevel.winfo_exists(self.theme_popup):
            self.position_theme_popup()
            self.theme_popup.deiconify()
            self.theme_popup.lift()
            return

        self.theme_popup = tk.Toplevel(self.master)
        self.theme_popup.overrideredirect(True)
        self.create_title_bar(self.theme_popup, "Theme", self.theme_popup.withdraw)

        body = tk.Frame(self.theme_popup)
        body.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for name in THEMES:
            b = ttk.Button(body, text=name, command=lambda n=name: self.change_theme(n))
            b.pack(fill=tk.X, pady=2)

        self.position_theme_popup()
        self.apply_theme(self.current_theme)

    def position_theme_popup(self):
        self.master.update_idletasks()
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_w = self.master.winfo_width()
        root_h = self.master.winfo_height()
        screen_w = self.master.winfo_screenwidth()
        self.theme_popup.update_idletasks()
        w = self.theme_popup.winfo_reqwidth()
        h = self.theme_popup.winfo_reqheight()
        if root_x + root_w / 2 < screen_w / 2:
            x = root_x + root_w + 5
        else:
            x = root_x - w - 5
        y = root_y + (root_h - h) // 2
        self.theme_popup.geometry(f"+{x}+{y}")

    def change_theme(self, name):
        self.current_theme = name
        self.apply_theme(name)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("pwdg")
    app = PwdgApp(root)
    root.mainloop()