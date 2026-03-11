"""
LMU Clock Overlay - Transparent system clock overlay for Le Mans Ultimate
Author: cento789
"""

import tkinter as tk
from tkinter import colorchooser, ttk
from datetime import datetime
import sys
import os
import json
import threading
import subprocess

from PIL import Image, ImageDraw
import pystray
import keyboard

APP_NAME = "LMU Clock Overlay"
APP_VERSION = "1.4.0"

# Process names to detect Le Mans Ultimate
LMU_PROCESS_NAMES = ["Le Mans Ultimate.exe", "LMU.exe"]
AUTHOR = "cento789"

DEFAULT_SIZE = 18
DEFAULT_COLOR = "#00FF00"
DEFAULT_OPACITY = 0.9
DEFAULT_SHOW_DATE = False
DEFAULT_POS = (50, 50)
DEFAULT_FONT = "Consolas"
DEFAULT_FORMAT_24H = True
DEFAULT_SHADOW = True
HOTKEY = "ctrl+shift+h"
SHADOW_COLOR = "#000000"
SHADOW_OFFSET = 2

FONT_CHOICES = [
    "Consolas", "Arial", "Segoe UI", "Verdana", "Tahoma",
    "Courier New", "Lucida Console", "Calibri", "Impact",
]

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", "."), "LMUClockOverlay")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")


def _load_config():
    defaults = {
        "font_size": DEFAULT_SIZE,
        "color": DEFAULT_COLOR,
        "opacity": DEFAULT_OPACITY,
        "show_date": DEFAULT_SHOW_DATE,
        "pos_x": DEFAULT_POS[0],
        "pos_y": DEFAULT_POS[1],
        "font_family": DEFAULT_FONT,
        "format_24h": DEFAULT_FORMAT_24H,
        "shadow": DEFAULT_SHADOW,
    }
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
        for k, v in defaults.items():
            saved.setdefault(k, v)
        return saved
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults


def _save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def _create_tray_icon_image(color):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], outline=color, width=4)
    draw.line([32, 32, 32, 14], fill=color, width=3)
    draw.line([32, 32, 48, 32], fill=color, width=3)
    return img


def _time_str(format_24h):
    return datetime.now().strftime("%H:%M:%S") if format_24h else datetime.now().strftime("%I:%M:%S %p")


def _is_lmu_running():
    """Check if Le Mans Ultimate process is running."""
    try:
        output = subprocess.check_output(
            ["tasklist", "/FO", "CSV", "/NH"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True, timeout=5,
        )
        output_lower = output.lower()
        return any(name.lower() in output_lower for name in LMU_PROCESS_NAMES)
    except (subprocess.SubprocessError, OSError):
        return False


class SettingsWindow:
    def __init__(self, cfg):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.font_size = cfg["font_size"]
        self.color = cfg["color"]
        self.opacity = cfg["opacity"]
        self.show_date = cfg["show_date"]
        self.font_family = cfg["font_family"]
        self.format_24h = cfg["format_24h"]
        self.shadow = cfg["shadow"]
        self.started = False

        # --- Header ---
        tk.Label(
            self.root, text=APP_NAME,
            font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#1e1e1e",
        ).pack(pady=(12, 0))
        tk.Label(
            self.root, text=f"v{APP_VERSION} by {AUTHOR}",
            font=("Segoe UI", 9), fg="#888888", bg="#1e1e1e",
        ).pack(pady=(0, 12))

        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(padx=20, pady=4)

        row = 0

        # --- Font family ---
        tk.Label(
            frame, text="Font:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.font_var = tk.StringVar(value=self.font_family)
        font_frame = tk.Frame(frame, bg="#1e1e1e")
        font_frame.grid(row=row, column=1, padx=(10, 0), pady=4, sticky="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
                        fieldbackground="#333333", background="#333333",
                        foreground="#CCCCCC", selectbackground="#555555",
                        selectforeground="#FFFFFF")
        self.font_combo = ttk.Combobox(
            font_frame, textvariable=self.font_var,
            values=FONT_CHOICES, state="readonly", width=18,
            style="Dark.TCombobox",
        )
        self.font_combo.pack()
        self.font_combo.bind("<<ComboboxSelected>>", self._on_font_change)

        row += 1

        # --- Font size ---
        tk.Label(
            frame, text="Font size (px):", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.size_var = tk.IntVar(value=self.font_size)
        size_frame = tk.Frame(frame, bg="#1e1e1e")
        size_frame.grid(row=row, column=1, padx=(10, 0), pady=4)
        tk.Scale(
            size_frame, from_=10, to=60, orient="horizontal",
            variable=self.size_var, length=180,
            bg="#1e1e1e", fg="#CCCCCC", highlightthickness=0,
            troughcolor="#333333", command=self._on_size_change,
        ).pack()

        row += 1

        # --- Color ---
        tk.Label(
            frame, text="Color:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        color_frame = tk.Frame(frame, bg="#1e1e1e")
        color_frame.grid(row=row, column=1, padx=(10, 0), pady=4)
        self.color_btn = tk.Button(
            color_frame, text="  Pick Color  ", bg=self.color, fg="#000000",
            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
            command=self._pick_color,
        )
        self.color_btn.pack()

        row += 1

        # --- Opacity ---
        tk.Label(
            frame, text="Opacity:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.opacity_var = tk.DoubleVar(value=self.opacity)
        opacity_frame = tk.Frame(frame, bg="#1e1e1e")
        opacity_frame.grid(row=row, column=1, padx=(10, 0), pady=4)
        tk.Scale(
            opacity_frame, from_=0.2, to=1.0, resolution=0.05,
            orient="horizontal", variable=self.opacity_var, length=180,
            bg="#1e1e1e", fg="#CCCCCC", highlightthickness=0,
            troughcolor="#333333", command=self._on_opacity_change,
        ).pack()

        row += 1

        # --- Time format ---
        tk.Label(
            frame, text="Format:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.format_var = tk.BooleanVar(value=self.format_24h)
        format_frame = tk.Frame(frame, bg="#1e1e1e")
        format_frame.grid(row=row, column=1, padx=(10, 0), pady=4, sticky="w")
        tk.Radiobutton(
            format_frame, text="24h", variable=self.format_var, value=True,
            bg="#1e1e1e", fg="#CCCCCC", activebackground="#1e1e1e",
            activeforeground="#CCCCCC", selectcolor="#333333",
            command=self._on_format_change,
        ).pack(side="left")
        tk.Radiobutton(
            format_frame, text="12h (AM/PM)", variable=self.format_var, value=False,
            bg="#1e1e1e", fg="#CCCCCC", activebackground="#1e1e1e",
            activeforeground="#CCCCCC", selectcolor="#333333",
            command=self._on_format_change,
        ).pack(side="left", padx=(8, 0))

        row += 1

        # --- Show date ---
        tk.Label(
            frame, text="Show date:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.date_var = tk.BooleanVar(value=self.show_date)
        date_frame = tk.Frame(frame, bg="#1e1e1e")
        date_frame.grid(row=row, column=1, padx=(10, 0), pady=4, sticky="w")
        tk.Checkbutton(
            date_frame, variable=self.date_var,
            bg="#1e1e1e", activebackground="#1e1e1e",
            selectcolor="#333333", command=self._on_date_toggle,
        ).pack()

        row += 1

        # --- Text shadow ---
        tk.Label(
            frame, text="Text shadow:", font=("Segoe UI", 10),
            fg="#CCCCCC", bg="#1e1e1e",
        ).grid(row=row, column=0, sticky="w", pady=4)

        self.shadow_var = tk.BooleanVar(value=self.shadow)
        shadow_frame = tk.Frame(frame, bg="#1e1e1e")
        shadow_frame.grid(row=row, column=1, padx=(10, 0), pady=4, sticky="w")
        tk.Checkbutton(
            shadow_frame, variable=self.shadow_var,
            bg="#1e1e1e", activebackground="#1e1e1e",
            selectcolor="#333333", command=self._on_shadow_toggle,
        ).pack()

        # --- Preview ---
        self.preview_canvas = tk.Canvas(
            self.root, bg="#000000", highlightthickness=0, height=60,
        )
        self.preview_canvas.pack(padx=20, pady=12, fill="x")
        self._draw_preview()

        # --- Hotkey hint ---
        tk.Label(
            self.root,
            text=f"In-game: drag to move | right-click to close | {HOTKEY.upper()} hide/show",
            font=("Segoe UI", 8), fg="#666666", bg="#1e1e1e",
        ).pack(pady=(0, 4))

        # --- Start button ---
        self.start_btn = tk.Button(
            self.root, text="  \u25b6  START  ",
            font=("Segoe UI", 12, "bold"),
            bg="#00AA00", fg="#FFFFFF",
            activebackground="#008800", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2",
            command=self._on_start,
        )
        self.start_btn.pack(pady=(4, 16))

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._update_preview()

    def _draw_preview(self):
        """Redraw the preview canvas with current settings."""
        c = self.preview_canvas
        c.delete("all")
        time_text = _time_str(self.format_var.get())
        date_text = datetime.now().strftime("%d/%m/%Y")
        font_t = (self.font_var.get(), self.size_var.get(), "bold")
        font_d = (self.font_var.get(), max(10, self.size_var.get() // 2), "bold")

        # Calculate required height
        h = self.size_var.get() + 16
        if self.date_var.get():
            h += max(10, self.size_var.get() // 2) + 4
        c.config(height=h)

        cx = c.winfo_reqwidth() // 2 or 150
        ty = 8

        if self.shadow_var.get():
            c.create_text(cx + SHADOW_OFFSET, ty + SHADOW_OFFSET,
                          text=time_text, font=font_t, fill="#222222", anchor="n")
        c.create_text(cx, ty, text=time_text, font=font_t, fill=self.color, anchor="n")

        if self.date_var.get():
            dy = ty + self.size_var.get() + 4
            if self.shadow_var.get():
                c.create_text(cx + SHADOW_OFFSET, dy + SHADOW_OFFSET,
                              text=date_text, font=font_d, fill="#222222", anchor="n")
            c.create_text(cx, dy, text=date_text, font=font_d, fill=self.color, anchor="n")

    def _on_font_change(self, _event=None):
        self.font_family = self.font_var.get()
        self._draw_preview()

    def _on_size_change(self, _val):
        self.font_size = self.size_var.get()
        self._draw_preview()

    def _pick_color(self):
        result = colorchooser.askcolor(color=self.color, title="Scegli colore orologio")
        if result and result[1]:
            self.color = result[1]
            self.color_btn.config(bg=self.color)
            self._draw_preview()

    def _on_opacity_change(self, _val):
        self.opacity = self.opacity_var.get()

    def _on_format_change(self):
        self.format_24h = self.format_var.get()
        self._draw_preview()

    def _on_date_toggle(self):
        self.show_date = self.date_var.get()
        self._draw_preview()

    def _on_shadow_toggle(self):
        self.shadow = self.shadow_var.get()
        self._draw_preview()

    def _update_preview(self):
        self._draw_preview()
        self.root.after(500, self._update_preview)

    def _on_start(self):
        self.started = True
        self.root.destroy()

    def _on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        if self.started:
            return {
                "font_size": self.size_var.get(),
                "color": self.color,
                "opacity": self.opacity_var.get(),
                "show_date": self.date_var.get(),
                "font_family": self.font_var.get(),
                "format_24h": self.format_var.get(),
                "shadow": self.shadow_var.get(),
            }
        return None


class ShadowLabel(tk.Canvas):
    """A Canvas-based label that renders text with an optional drop shadow."""

    def __init__(self, parent, font_family, font_size, color, shadow=True, **kw):
        super().__init__(parent, bg="#000000", highlightthickness=0, **kw)
        self._font_family = font_family
        self._font_size = font_size
        self._color = color
        self._shadow = shadow
        self._text = ""

    def set_text(self, text):
        self._text = text
        self._redraw()

    def _redraw(self):
        self.delete("all")
        fnt = (self._font_family, self._font_size, "bold")
        x, y = 4, 2
        if self._shadow:
            self.create_text(x + SHADOW_OFFSET, y + SHADOW_OFFSET,
                             text=self._text, font=fnt, fill="#222222", anchor="nw")
        self.create_text(x, y, text=self._text, font=fnt, fill=self._color, anchor="nw")
        # Resize canvas to fit
        self.update_idletasks()
        bbox = self.bbox("all")
        if bbox:
            self.config(width=bbox[2] + 4, height=bbox[3] + 2)


class ClockOverlay:
    def __init__(self, cfg):
        self.cfg = cfg
        self.font_size = cfg["font_size"]
        self.color = cfg["color"]
        self.opacity = cfg["opacity"]
        self.show_date = cfg["show_date"]
        self.font_family = cfg["font_family"]
        self.format_24h = cfg["format_24h"]
        self.shadow = cfg["shadow"]
        self.pos_x = cfg["pos_x"]
        self.pos_y = cfg["pos_y"]
        self.tray_icon = None
        self.visible = False  # start hidden, wait for LMU
        self.lmu_running = False
        self.user_hidden = False  # tracks manual hide via hotkey

        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#000000")
        self.root.attributes("-alpha", self.opacity)
        self.root.configure(bg="#000000")
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")
        self.root.withdraw()  # start hidden

        self._drag_data = {"x": 0, "y": 0}

        self.time_label = ShadowLabel(
            self.root, self.font_family, self.font_size, self.color, self.shadow,
        )
        self.time_label.pack()

        self.date_label = ShadowLabel(
            self.root, self.font_family, max(10, self.font_size // 2),
            self.color, self.shadow,
        )
        if self.show_date:
            self.date_label.pack()

        self._bind_all()
        self._update_clock()
        self._check_lmu()

        keyboard.add_hotkey(HOTKEY, self._toggle_visibility)

    def _bind_all(self):
        for w in [self.root, self.time_label, self.date_label]:
            w.bind("<ButtonPress-1>", self._on_drag_start)
            w.bind("<B1-Motion>", self._on_drag_motion)
            w.bind("<ButtonRelease-1>", self._on_drag_end)
            w.bind("<ButtonPress-3>", lambda e: self._quit())

    def _on_drag_start(self, event):
        self._drag_data["x"] = event.x_root - self.root.winfo_x()
        self._drag_data["y"] = event.y_root - self.root.winfo_y()

    def _on_drag_motion(self, event):
        x = event.x_root - self._drag_data["x"]
        y = event.y_root - self._drag_data["y"]
        self.root.geometry(f"+{x}+{y}")

    def _on_drag_end(self, _event):
        self.pos_x = self.root.winfo_x()
        self.pos_y = self.root.winfo_y()

    def _toggle_visibility(self):
        self.root.after(0, self._do_toggle)

    def _do_toggle(self):
        if self.visible:
            self.root.withdraw()
            self.visible = False
            self.user_hidden = True
        else:
            if self.lmu_running:
                self.root.deiconify()
                self.visible = True
            self.user_hidden = False

    def _check_lmu(self):
        """Periodically check if LMU is running and show/hide overlay."""
        def _poll():
            was_running = self.lmu_running
            self.lmu_running = _is_lmu_running()

            if self.lmu_running and not was_running:
                if not self.user_hidden:
                    self.root.after(0, self._show_overlay)
                self._update_tray_tooltip("LMU detected - overlay active")
            elif not self.lmu_running and was_running:
                self.root.after(0, self._hide_overlay)
                self._update_tray_tooltip("Waiting for Le Mans Ultimate...")

            self.root.after(3000, _poll)

        self._update_tray_tooltip("Waiting for Le Mans Ultimate...")
        self.root.after(1000, _poll)

    def _show_overlay(self):
        if not self.visible:
            self.root.deiconify()
            self.visible = True

    def _hide_overlay(self):
        if self.visible:
            self.root.withdraw()
            self.visible = False

    def _update_tray_tooltip(self, text):
        if self.tray_icon:
            self.tray_icon.title = text

    def _update_clock(self):
        self.time_label.set_text(_time_str(self.format_24h))
        if self.show_date:
            self.date_label.set_text(datetime.now().strftime("%d/%m/%Y"))
        self.root.after(200, self._update_clock)

    def _quit(self):
        self.cfg["pos_x"] = self.pos_x
        self.cfg["pos_y"] = self.pos_y
        _save_config(self.cfg)
        keyboard.unhook_all()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()

    def _setup_tray(self):
        icon_image = _create_tray_icon_image(self.color)
        menu = pystray.Menu(
            pystray.MenuItem(f"{APP_NAME} v{APP_VERSION}", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Show/Hide  (Ctrl+Shift+H)", lambda: self._toggle_visibility()),
            pystray.MenuItem("Quit", lambda: self.root.after(0, self._quit)),
        )
        self.tray_icon = pystray.Icon(
            APP_NAME, icon_image, "Waiting for Le Mans Ultimate...", menu
        )
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def run(self):
        self._setup_tray()
        self.root.mainloop()


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"{APP_NAME} v{APP_VERSION} by {AUTHOR}")
        sys.exit(0)

    cfg = _load_config()
    settings = SettingsWindow(cfg)
    result = settings.run()

    if result:
        cfg.update(result)
        _save_config(cfg)
        overlay = ClockOverlay(cfg)
        overlay.run()
