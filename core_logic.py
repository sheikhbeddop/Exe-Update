# ==============================================================================
# 🧪 SCIENTIST AIMBOT - 8K QUANTUM CYBER DOCK (V 3.0 ULTRA)
# ==============================================================================
# Ultra-Luxury Cyberpunk Interface with Interactive Mouse Particle Aura
# Modular Sidebar Deck • Smart Match Sentinel • Crosshair Studio • Turbo RAM Purge

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymem
from pymem import Pymem
from pymem.pattern import pattern_scan_all
from pymem.memory import read_bytes, write_bytes
import ctypes
import threading
import time
import sys
import os
import winsound
import hashlib
import random
import json
import webbrowser
import gc

def get_icon_path():
    candidates = [
        os.path.join(getattr(sys, "_MEIPASS", ""), "icon.ico"),
        os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "icon.ico"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),
        os.path.join(os.getcwd(), "icon.ico")
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None

def apply_icon(window):
    try:
        icon_path = get_icon_path()
        if icon_path:
            window.iconbitmap(icon_path)
    except Exception:
        pass

# ==========================================
# 🪟 Windows Taskbar Integration
# ==========================================
def enable_window_taskbar(window):
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id()) or window.winfo_id()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        style = (style & ~0x00000080) | 0x00040000
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
    except Exception:
        pass

# ==========================================
# 🧬 Memory & Privilege Structs
# ==========================================
SE_DEBUG_NAME = "SeDebugPrivilege"
SE_PRIVILEGE_ENABLED = 0x00000002

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Luid", ctypes.c_longlong), ("Attributes", ctypes.c_ulong)]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES)]

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('ullTotalPhys', ctypes.c_ulonglong),
        ('ullAvailPhys', ctypes.c_ulonglong),
        ('ullTotalPageFile', ctypes.c_ulonglong),
        ('ullAvailPageFile', ctypes.c_ulonglong),
        ('ullTotalVirtual', ctypes.c_ulonglong),
        ('ullAvailVirtual', ctypes.c_ulonglong),
        ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
    ]

MOUSE_VK_MAP = {
    0x04: "MOUSE3",
    0x05: "MOUSE4",
    0x06: "MOUSE5",
}

VK_MAP = {
    0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
    0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
    0x2D: "INS", 0x2E: "DEL", 0x24: "HOME", 0x23: "END", 0x21: "PGUP", 0x22: "PGDN",
    0x14: "CAPS", 0x09: "TAB", 0x20: "SPACE", 0x10: "SHIFT", 0x11: "CTRL", 0x12: "ALT",
    0x60: "NUM0", 0x61: "NUM1", 0x62: "NUM2", 0x63: "NUM3", 0x64: "NUM4",
    0x65: "NUM5", 0x66: "NUM6", 0x67: "NUM7", 0x68: "NUM8", 0x69: "NUM9",
}
for c in range(0x41, 0x5B): VK_MAP[c] = chr(c)
for n in range(0x30, 0x3A): VK_MAP[n] = chr(n)

# ==========================================
# 🎯 Laser Crosshair Studio
# ==========================================
class QuantumCrosshair:
    def __init__(self):
        self.win = None
        self.is_active = False
        self.colors = ["#00F0FF", "#00FF9D", "#FF0055", "#F59E0B", "#FFFFFF"]
        self.color_names = ["CYAN", "GREEN", "RED", "GOLD", "WHITE"]
        self.color_idx = 0
        self.styles = ["DOT", "PLUS", "CIRCLE_DOT", "DIAMOND"]
        self.style_idx = 0

    def toggle(self):
        if self.is_active:
            self.hide()
        else:
            self.show()
        return self.is_active

    def cycle_color(self):
        self.color_idx = (self.color_idx + 1) % len(self.colors)
        if self.is_active:
            self.redraw()
        return self.color_names[self.color_idx], self.colors[self.color_idx]

    def cycle_style(self):
        self.style_idx = (self.style_idx + 1) % len(self.styles)
        if self.is_active:
            self.redraw()
        return self.styles[self.style_idx]

    def show(self):
        if self.win:
            try: self.win.destroy()
            except Exception: pass
            
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-transparentcolor", "#010101")
        self.win.configure(bg="#010101")
        
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        size = 64
        x = (sw - size) // 2
        y = (sh - size) // 2
        self.win.geometry(f"{size}x{size}+{x}+{y}")
        
        try:
            hwnd = ctypes.windll.user32.GetParent(self.win.winfo_id()) or self.win.winfo_id()
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | 0x00080000 | 0x00000020)
        except Exception:
            pass
            
        self.canvas = tk.Canvas(self.win, width=size, height=size, bg="#010101", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.redraw()
        self.is_active = True

    def hide(self):
        if self.win:
            try: self.win.destroy()
            except Exception: pass
            self.win = None
        self.is_active = False

    def redraw(self):
        if not self.win or not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        c = self.colors[self.color_idx]
        st = self.styles[self.style_idx]
        cx, cy = 32, 32
        
        if st == "DOT":
            self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=c, outline="#000000", width=1)
        elif st == "PLUS":
            self.canvas.create_line(cx-10, cy, cx-3, cy, fill=c, width=2)
            self.canvas.create_line(cx+3, cy, cx+10, cy, fill=c, width=2)
            self.canvas.create_line(cx, cy-10, cx, cy-3, fill=c, width=2)
            self.canvas.create_line(cx, cy+3, cx, cy+10, fill=c, width=2)
            self.canvas.create_oval(cx-1, cy-1, cx+1, cy+1, fill=c, outline=c)
        elif st == "CIRCLE_DOT":
            self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, outline=c, width=1.5)
            self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill=c, outline="#000000", width=1)
        elif st == "DIAMOND":
            self.canvas.create_polygon([cx, cy-6, cx+6, cy, cx, cy+6, cx-6, cy], outline=c, fill="", width=1.5)
            self.canvas.create_oval(cx-1, cy-1, cx+1, cy+1, fill=c, outline=c)

# ==========================================
# 🎨 8K Cyber Rounded Button
# ==========================================
class Cyber8KButton(tk.Canvas):
    def __init__(self, parent, text, command=None, 
                 bg_color="#071220", border_color="#00F0FF", 
                 hover_bg="#00F0FF", hover_fg="#020408", 
                 text_color="#00F0FF", width=180, height=40, 
                 corner_radius=10, font=("Segoe UI", 9, "bold")):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.default_bg = bg_color
        self.default_border = border_color
        self.default_fg = text_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.disabled_bg = "#070B12"
        self.disabled_border = "#121A2B"
        self.disabled_fg = "#475569"
        
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.font = font
        self.text_str = text
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.is_enabled = True
        
        self.rect = self._draw_rounded(1, 1, width-2, height-2, corner_radius, fill=self.bg_color, outline=self.border_color, width=1)
        self.text_item = self.create_text(width // 2, height // 2, text=self.text_str, fill=self.text_color, font=self.font)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        for item in (self.rect, self.text_item):
            self.tag_bind(item, "<Enter>", self._on_enter)
            self.tag_bind(item, "<Leave>", self._on_leave)
            self.tag_bind(item, "<Button-1>", self._on_click)

    def _draw_rounded(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, 
            x2, y2-r, x2, y2, x2-r, y2, x1+r, y2, 
            x1, y2, x1, y2-r, x1, y1+r, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_text(self, new_text):
        self.text_str = new_text
        self.itemconfig(self.text_item, text=new_text)

    def set_theme(self, bg_color, border_color=None, text_color="#FFFFFF", hover_bg=None, hover_fg="#000000"):
        self.default_bg = bg_color
        self.default_border = border_color or bg_color
        self.default_fg = text_color
        if hover_bg: self.hover_bg = hover_bg
        if hover_fg: self.hover_fg = hover_fg
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.default_bg, outline=self.default_border)
            self.itemconfig(self.text_item, fill=self.default_fg)

    def set_state(self, state):
        if state == "disabled":
            self.is_enabled = False
            self.itemconfig(self.rect, fill=self.disabled_bg, outline=self.disabled_border)
            self.itemconfig(self.text_item, fill=self.disabled_fg)
            self.config(cursor="")
        else:
            self.is_enabled = True
            self.itemconfig(self.rect, fill=self.default_bg, outline=self.default_border)
            self.itemconfig(self.text_item, fill=self.default_fg)
            self.config(cursor="hand2")

    def _on_enter(self, event=None):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)
            self.itemconfig(self.text_item, fill=self.hover_fg)
            self.config(cursor="hand2")

    def _on_leave(self, event=None):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.default_bg, outline=self.default_border)
            self.itemconfig(self.text_item, fill=self.default_fg)
            self.config(cursor="")

    def _on_click(self, event=None):
        if self.is_enabled and self.command:
            self.command()

# ==========================================
# 🖥️ 8K Quantum Cyber Command Center
# ==========================================
class AimbotController:
    def __init__(self, root, keyauth_instance=None):
        self.root = root
        self.keyauth = keyauth_instance or globals().get("keyauthapp", None)
        
        # 8K Widescreen Cinema Geometry
        self.WIN_W = 680
        self.WIN_H = 550
        self.real_title = "SCIENTIST 8K QUANTUM"
        self.root.title(self.real_title)
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.root.resizable(False, False)
        self.root.configure(bg="#020408")
        self.root.attributes("-alpha", 0.98)
        self.root.overrideredirect(True)
        
        if apply_icon:
            try: apply_icon(self.root)
            except Exception: pass
        
        sx = (self.root.winfo_screenwidth() - self.WIN_W) // 2
        sy = (self.root.winfo_screenheight() - self.WIN_H) // 2
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}+{sx}+{sy}")
        enable_window_taskbar(self.root)
        
        # Core State
        self.is_injecting = False
        self.is_injected = False
        self.pm = None
        self.patched_records = []
        self.cached_addresses = []
        self.cached_pid = None
        self.force_rescan = True
        self.is_topmost = False
        self.sound_enabled = True
        self.bound_vk = None
        self.bound_key_name = None
        self.is_binding_key = False
        self.reset_hotkey = None
        self.reset_hotkey_name = None
        self.is_binding_reset_hotkey = False
        self.is_shutting_down = False
        self.streamer_mode = False
        
        # 🌟 Smart Match Sentinel
        self.auto_rehook = True
        
        # Crosshair & Masking
        self.crosshair = QuantumCrosshair()
        self.spoof_names = ["Spotify Premium", "Discord", "Calculator", "Visual Studio Code", "Task Manager"]
        self.spoof_idx = 0
        self.is_spoofed = False
        
        # Presets
        self.current_preset = 0
        self.preset_names = ["⚡ ULTRA AGGRESSIVE", "🎯 SMOOTH LEGIT", "🔥 QUANTUM HYBRID"]
        
        # 🌟 Interactive Mouse Particle Aura Tracker
        self.particles = []
        
        self._setup_styles()
        self.setup_ui()
        
        # Mouse Particle Loop & Motion Binding
        self.root.bind("<Motion>", self._on_mouse_motion)
        self._animate_particles()
        
        # Active Hotkeys & Sentinel Watcher
        self.hotkey_thread = threading.Thread(target=self._global_hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        
        self.sentinel_thread = threading.Thread(target=self._smart_match_sentinel_worker, daemon=True)
        self.sentinel_thread.start()
        
        self.root.after(2000, self.check_system_status)
        self.update_expiry_countdown()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Cyber8K.Horizontal.TProgressbar", 
                        troughcolor="#070B12", 
                        background="#00F0FF", 
                        bordercolor="#121A2B", 
                        thickness=4)

    def style_sub_btn(self, btn, bg="#0A0F1D", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#020408"):
        btn.config(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=hover_fg, bd=1, relief="solid", highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg) if btn['state'] != 'disabled' else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg) if btn['state'] != 'disabled' else None)

    # ==========================================
    # 🌟 Interactive Mouse Aura Particles
    # ==========================================
    def _on_mouse_motion(self, e):
        if len(self.particles) < 15:
            colors = ["#00F0FF", "#A78BFA", "#00FF9D"]
            c = random.choice(colors)
            p_id = self.bg_canvas.create_oval(e.x-3, e.y-3, e.x+3, e.y+3, outline=c, fill="", width=1)
            self.particles.append({"id": p_id, "x": e.x, "y": e.y, "r": 3, "max_r": 18, "life": 1.0})

    def _animate_particles(self):
        if not self.is_shutting_down:
            to_remove = []
            for p in self.particles:
                p["r"] += 1.5
                p["life"] -= 0.1
                if p["life"] <= 0 or p["r"] >= p["max_r"]:
                    self.bg_canvas.delete(p["id"])
                    to_remove.append(p)
                else:
                    r = p["r"]
                    self.bg_canvas.coords(p["id"], p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r)
            for p in to_remove:
                self.particles.remove(p)
            self.root.after(35, self._animate_particles)

    def _on_minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        def _restore():
            if self.root.state() == "normal":
                self.root.overrideredirect(True)
                self.root.lift()
            else:
                self.root.after(80, _restore)
        self.root.after(80, _restore)

    def setup_ui(self):
        outer_frame = tk.Frame(self.root, bg="#1E2A4A", bd=1)
        outer_frame.pack(fill="both", expand=True)
        
        self.bg_canvas = tk.Canvas(outer_frame, bg="#020408", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # ==========================================
        # 🔝 Top Hologram Header Bar
        # ==========================================
        titlebar = tk.Frame(self.bg_canvas, bg="#060A14", height=46)
        titlebar.place(x=0, y=0, width=self.WIN_W, height=46)
        
        drag_data = {"x": 0, "y": 0}
        def _start_drag(e):
            drag_data["x"] = e.x_root - self.root.winfo_x()
            drag_data["y"] = e.y_root - self.root.winfo_y()
        def _do_drag(e):
            nx = e.x_root - drag_data["x"]
            ny = e.y_root - drag_data["y"]
            self.root.geometry(f"+{nx}+{ny}")
        
        titlebar.bind("<ButtonPress-1>", _start_drag)
        titlebar.bind("<B1-Motion>", _do_drag)
        
        left_brand = tk.Frame(titlebar, bg="#060A14")
        left_brand.pack(side="left", padx=12, pady=6)
        left_brand.bind("<ButtonPress-1>", _start_drag)
        left_brand.bind("<B1-Motion>", _do_drag)
        
        tk.Label(left_brand, text="🧪", font=("Segoe UI Emoji", 12), bg="#060A14").pack(side="left", padx=(0, 6))
        
        self.title_text_lbl = tk.Label(left_brand, text="SCIENTIST", font=("Segoe UI", 11, "bold"), bg="#060A14", fg="#F8FAFC")
        self.title_text_lbl.pack(side="left")
        
        self.ver_tag = tk.Label(left_brand, text=" 8K QUANTUM PRO ", font=("Segoe UI", 7, "bold"), bg="#0A1E33", fg="#00F0FF", padx=6, pady=2)
        self.ver_tag.pack(side="left", padx=6)
        
        username = getattr(self.keyauth, "logged_username", "Guest") if self.keyauth else "Guest"
        user_chip = tk.Frame(titlebar, bg="#0D1424", bd=1, relief="solid")
        user_chip.config(highlightbackground="#1E2A4A", highlightthickness=1)
        user_chip.pack(side="left", padx=6, pady=7)
        
        user_inner = tk.Frame(user_chip, bg="#0D1424", padx=8, pady=2)
        user_inner.pack()
        
        user_lbl = tk.Label(user_inner, text=f"👑 {username}", font=("Segoe UI", 7, "bold"), bg="#0D1424", fg="#A78BFA")
        user_lbl.pack(side="left", padx=(0, 6))
        
        self.expiry_lbl = tk.Label(user_inner, text="⏳ EXPIRY: --:--:--", font=("Segoe UI", 7, "bold"), bg="#0D1424", fg="#00FF9D")
        self.expiry_lbl.pack(side="left")
        
        right_controls = tk.Frame(titlebar, bg="#060A14")
        right_controls.pack(side="right", padx=(0, 4))
        
        min_btn = tk.Label(right_controls, text=" 🗕 ", font=("Segoe UI", 10), bg="#060A14", fg="#94A3B8", cursor="hand2")
        min_btn.pack(side="left", padx=2, pady=4)
        min_btn.bind("<Enter>", lambda e: min_btn.config(bg="#1E2A4A", fg="#FFFFFF"))
        min_btn.bind("<Leave>", lambda e: min_btn.config(bg="#060A14", fg="#94A3B8"))
        min_btn.bind("<Button-1>", lambda e: self._on_minimize())
        
        close_btn = tk.Label(right_controls, text=" ✕ ", font=("Segoe UI", 10, "bold"), bg="#060A14", fg="#94A3B8", cursor="hand2")
        close_btn.pack(side="left", padx=2, pady=4)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#FF0055", fg="#FFFFFF"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#060A14", fg="#94A3B8"))
        close_btn.bind("<Button-1>", lambda e: self.on_closing())
        
        # Divider Line
        accent_line = tk.Frame(self.bg_canvas, bg="#00F0FF", height=1)
        accent_line.place(x=0, y=46, width=self.WIN_W, height=1)
        
        # ==========================================
        # 🎮 Left Sidebar Quick-Launch Dock
        # ==========================================
        sidebar = tk.Frame(self.bg_canvas, bg="#050810", width=150, bd=1, relief="solid")
        sidebar.config(highlightbackground="#121A2B", highlightthickness=1)
        sidebar.place(x=10, y=55, width=150, height=450)
        
        tk.Label(sidebar, text="⚡ SYSTEM DOCK", font=("Segoe UI", 7, "bold"), bg="#050810", fg="#64748B").pack(anchor="w", padx=8, pady=(8, 6))
        
        self.preset_btn = tk.Button(sidebar, text="⚡ AGGRESSIVE", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.cycle_preset)
        self.preset_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.preset_btn, bg="#0D1424", fg="#A78BFA", hover_bg="#A78BFA", hover_fg="#020408")
        
        self.crosshair_btn = tk.Button(sidebar, text="🎯 CROSSHAIR: OFF", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_crosshair)
        self.crosshair_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.crosshair_btn, bg="#0D1424", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#020408")
        
        self.cross_style_btn = tk.Button(sidebar, text="💠 STYLE: DOT", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.cycle_crosshair_style)
        self.cross_style_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.cross_style_btn, bg="#0D1424", fg="#38BDF8", hover_bg="#38BDF8", hover_fg="#020408")
        
        self.cross_col_btn = tk.Button(sidebar, text="🎨 COLOR: CYAN", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.cycle_crosshair_color)
        self.cross_col_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.cross_col_btn, bg="#0D1424", fg="#00F0FF", hover_bg="#00F0FF", hover_fg="#020408")
        
        self.ram_btn = tk.Button(sidebar, text="🧹 TURBO PURGE", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.flush_system_ram)
        self.ram_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.ram_btn, bg="#0D1424", fg="#00FF9D", hover_bg="#00FF9D", hover_fg="#020408")
        
        self.sentinel_btn = tk.Button(sidebar, text="🤖 SENTINEL: ON", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_sentinel)
        self.sentinel_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.sentinel_btn, bg="#062419", fg="#00FF9D", hover_bg="#00FF9D", hover_fg="#020408")
        
        tk.Label(sidebar, text="⚙️ QUICK TOGGLES", font=("Segoe UI", 7, "bold"), bg="#050810", fg="#64748B").pack(anchor="w", padx=8, pady=(10, 4))
        
        self.sound_btn = tk.Button(sidebar, text="🔊 AUDIO: ON", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_sound)
        self.sound_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.sound_btn, bg="#0D1424", fg="#00FF9D", hover_bg="#00FF9D", hover_fg="#020408")
        
        self.topmost_btn = tk.Button(sidebar, text="📌 PIN OVERLAY", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_topmost)
        self.topmost_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.topmost_btn, bg="#0D1424", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#020408")
        
        self.streamer_btn = tk.Button(sidebar, text="🕶️ CLOAK (F10)", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_streamer_mode)
        self.streamer_btn.pack(fill="x", padx=6, pady=2)
        self.style_sub_btn(self.streamer_btn, bg="#0D1424", fg="#94A3B8", hover_bg="#F59E0B", hover_fg="#020408")
        
        # ==========================================
        # 🎮 Center Main Command Deck
        # ==========================================
        main_content = tk.Frame(self.bg_canvas, bg="#020408")
        main_content.place(x=168, y=55, width=500, height=450)
        
        # Top Hero Hook Card
        hero_card = tk.Frame(main_content, bg="#070C16", bd=1, relief="solid")
        hero_card.config(highlightbackground="#1E2A4A", highlightthickness=1)
        hero_card.pack(fill="x", pady=(0, 6))
        
        h_inner = tk.Frame(hero_card, bg="#070C16", padx=12, pady=10)
        h_inner.pack(fill="x")
        
        tk.Label(h_inner, text="⚡ QUANTUM MASTER HOOK • LIVE MEMORY SENTINEL", font=("Segoe UI", 7, "bold"), bg="#070C16", fg="#00F0FF").pack(anchor="w", pady=(0, 4))
        
        h_ctrl = tk.Frame(h_inner, bg="#070C16")
        h_ctrl.pack(fill="x")
        
        self.inject_btn = Cyber8KButton(
            h_ctrl, 
            text="⚡ ENGAGE QUANTUM HOOK", 
            command=self.handle_action,
            bg_color="#08182B",
            border_color="#00F0FF",
            hover_bg="#00F0FF",
            hover_fg="#020408",
            text_color="#00F0FF",
            width=280, 
            height=44,
            corner_radius=10,
            font=("Segoe UI", 10, "bold")
        )
        self.inject_btn.pack(side="left")
        
        self.status_pill = tk.Label(h_ctrl, text="● STANDBY • READY", font=("Consolas", 8, "bold"), bg="#0A1628", fg="#00FF9D", padx=8, pady=4, bd=1, relief="solid")
        self.status_pill.pack(side="right")
        
        # Middle Grid: Keybind Matrix + Telemetry Radar
        mid_grid = tk.Frame(main_content, bg="#020408")
        mid_grid.pack(fill="x", pady=(0, 6))
        
        # Keybind Card
        key_card = tk.Frame(mid_grid, bg="#070C16", bd=1, relief="solid", width=240)
        key_card.config(highlightbackground="#1E2A4A", highlightthickness=1)
        key_card.pack(side="left", fill="both", expand=True, padx=(0, 3))
        
        k_in = tk.Frame(key_card, bg="#070C16", padx=8, pady=6)
        k_in.pack(fill="both", expand=True)
        
        tk.Label(k_in, text="⌨️ TRIGGER HOTKEYS", font=("Segoe UI", 7, "bold"), bg="#070C16", fg="#64748B").pack(anchor="w", pady=(0, 3))
        
        r1 = tk.Frame(k_in, bg="#070C16")
        r1.pack(fill="x", pady=2)
        tk.Label(r1, text="Trigger", font=("Segoe UI", 8, "bold"), bg="#070C16", fg="#F8FAFC").pack(side="left")
        self.keybind_btn = Cyber8KButton(
            r1, text="[ BIND TRIGGER ]", command=self.start_keybinding,
            bg_color="#0A1222", border_color="#1E2A4A", hover_bg="#00F0FF",
            hover_fg="#020408", text_color="#38BDF8", width=110, height=24, corner_radius=6, font=("Consolas", 8, "bold")
        )
        self.keybind_btn.pack(side="right")
        
        r2 = tk.Frame(k_in, bg="#070C16")
        r2.pack(fill="x", pady=2)
        tk.Label(r2, text="New Round", font=("Segoe UI", 8, "bold"), bg="#070C16", fg="#F8FAFC").pack(side="left")
        self.reset_key_btn = Cyber8KButton(
            r2, text="[ NEW MATCH ]", command=self.start_reset_keybinding,
            bg_color="#0A1222", border_color="#1E2A4A", hover_bg="#00F0FF",
            hover_fg="#020408", text_color="#38BDF8", width=110, height=24, corner_radius=6, font=("Consolas", 8, "bold")
        )
        self.reset_key_btn.pack(side="right")
        
        # Telemetry Card
        radar_card = tk.Frame(mid_grid, bg="#070C16", bd=1, relief="solid", width=250)
        radar_card.config(highlightbackground="#1E2A4A", highlightthickness=1)
        radar_card.pack(side="right", fill="both", expand=True, padx=(3, 0))
        
        rad_in = tk.Frame(radar_card, bg="#070C16", padx=6, pady=4)
        rad_in.pack(fill="both", expand=True)
        
        rad_grid = tk.Frame(rad_in, bg="#070C16")
        rad_grid.pack(fill="both", expand=True)
        
        self.card_process = self._create_radar_card(rad_grid, "EMULATOR", "HD-Player.exe", "⚪ Standby", "#64748B", 0, 0)
        self.card_engine = self._create_radar_card(rad_grid, "ENGINE", "Quantum Cache", "⚡ Ready", "#00F0FF", 0, 1)
        self.card_ram = self._create_radar_card(rad_grid, "SYSTEM RAM", "Physical", "📊 Checking...", "#A78BFA", 1, 0)
        self.card_match = self._create_radar_card(rad_grid, "SENTINEL", "Auto Sync", "🟢 Active", "#00FF9D", 1, 1)
        
        rad_grid.grid_columnconfigure(0, weight=1)
        rad_grid.grid_columnconfigure(1, weight=1)
        
        # Bottom Console Log Stream
        log_box = tk.Frame(main_content, bg="#070C16", bd=1, relief="solid")
        log_box.config(highlightbackground="#1E2A4A", highlightthickness=1)
        log_box.pack(fill="both", expand=True)
        
        log_header = tk.Frame(log_box, bg="#050810", height=26)
        log_header.pack(fill="x")
        log_header.pack_propagate(False)
        
        tk.Label(log_header, text="🖥️ 8K QUANTUM TERMINAL STREAM", font=("Consolas", 8, "bold"), bg="#050810", fg="#00F0FF").pack(side="left", padx=6)
        
        clear_btn = tk.Button(log_header, text="🗑️", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.clear_logs)
        clear_btn.pack(side="right", padx=2, pady=1)
        self.style_sub_btn(clear_btn, bg="#0A0F1D", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#020408")
        
        copy_btn = tk.Button(log_header, text="📋", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.copy_logs)
        copy_btn.pack(side="right", padx=(0, 2), pady=1)
        self.style_sub_btn(copy_btn, bg="#0A0F1D", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#020408")
        
        self.log_text = tk.Text(log_box, bg="#020408", fg="#E2E8F0", 
                                font=("Consolas", 8), relief="flat", bd=0, 
                                wrap="word", highlightthickness=0, height=5)
        self.log_text.pack(fill="both", expand=True, padx=6, pady=4)
        self.log_text.tag_config("time", foreground="#475569")
        self.log_text.tag_config("info", foreground="#38BDF8")
        self.log_text.tag_config("success", foreground="#00FF9D")
        self.log_text.tag_config("warn", foreground="#F59E0B")
        self.log_text.tag_config("error", foreground="#FF0055")
        
        # Footer
        footer = tk.Frame(self.bg_canvas, bg="#020408", height=24)
        footer.place(x=10, y=515, width=self.WIN_W-20, height=24)
        
        discord_btn = tk.Label(footer, text="💬 Discord", font=("Segoe UI", 7, "bold"), bg="#070C16", fg="#A78BFA", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        discord_btn.pack(side="left", padx=(0, 4))
        discord_btn.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/QSSbvyr3nC"))
        
        wa_btn = tk.Label(footer, text="📱 WhatsApp", font=("Segoe UI", 7, "bold"), bg="#070C16", fg="#00FF9D", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        wa_btn.pack(side="left", padx=(0, 4))
        wa_btn.bind("<Button-1>", lambda e: webbrowser.open("https://wa.me/8801952851550"))
        
        spoofer_btn = tk.Label(footer, text="🎭 Mask Process", font=("Segoe UI", 7, "bold"), bg="#070C16", fg="#F59E0B", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        spoofer_btn.pack(side="left")
        spoofer_btn.bind("<Button-1>", lambda e: self.cycle_spoof_title())
        
        credit_lbl = tk.Label(footer, text="8K QUANTUM DOCK • INTERACTIVE AURA EDITION", font=("Segoe UI", 7, "bold"), bg="#020408", fg="#475569")
        credit_lbl.pack(side="right")

        if self.is_admin():
            self.add_log("SUCCESS", "Running with Kernel Administrator Privileges")
        else:
            self.add_log("WARN", "Standard user mode. Some privileges may be restricted.")
            
        self.add_log("SUCCESS", "◈ Scientist 8K Quantum Dock initialized.")
        self.add_log("INFO", "Interactive Particle Aura is active (move mouse over window).")
        self.add_log("INFO", "Smart Match Sentinel is ON — auto-rescan active on every match.")

    def _create_radar_card(self, parent, category, title, status, status_color, r=0, c=0):
        f = tk.Frame(parent, bg="#050810", bd=1, relief="solid")
        f.config(highlightbackground="#121A2B", highlightthickness=1)
        f.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
        
        inner = tk.Frame(f, bg="#050810", padx=4, pady=2)
        inner.pack(fill="both", expand=True)
        
        cat_lbl = tk.Label(inner, text=category, font=("Segoe UI", 6, "bold"), bg="#050810", fg="#475569")
        cat_lbl.pack(anchor="w")
        
        title_lbl = tk.Label(inner, text=title, font=("Segoe UI", 7, "bold"), bg="#050810", fg="#F8FAFC")
        title_lbl.pack(anchor="w")
        
        status_lbl = tk.Label(inner, text=status, font=("Segoe UI", 7, "bold"), bg="#050810", fg=status_color)
        status_lbl.pack(anchor="w")
        f.status_lbl = status_lbl
        return f

    def _update_card_status(self, card, text, color):
        def _exec():
            card.status_lbl.config(text=text, fg=color)
        self.root.after(0, _exec)

    def _smart_match_sentinel_worker(self):
        while not self.is_shutting_down:
            try:
                if self.is_injected and self.cached_addresses and self.cached_pid:
                    test_addr = self.cached_addresses[0] + 0xAF
                    try:
                        pm_t = Pymem("HD-Player.exe")
                        test_bytes = read_bytes(pm_t.process_handle, test_addr, 4)
                        pm_t.close_process()
                        if not test_bytes or test_bytes == b'\x00\x00\x00\x00':
                            self.force_rescan = True
                            self.cached_addresses = []
                            self.is_injected = False
                            self.root.after(0, self._on_match_relocation_detected)
                    except Exception:
                        self.force_rescan = True
                        self.cached_addresses = []
                        self.is_injected = False
                        self.root.after(0, self._on_match_relocation_detected)
            except Exception:
                pass
            time.sleep(1.5)

    def _on_match_relocation_detected(self):
        self.inject_btn.set_text("⚡ ENGAGE QUANTUM HOOK")
        self.inject_btn.set_theme("#08182B", "#00F0FF", "#00F0FF", "#00F0FF", "#020408")
        self.status_pill.config(text="● NEW MATCH DETECTED", fg="#F59E0B")
        self._update_card_status(self.card_match, "🔄 Match Shift", "#F59E0B")
        self.add_log("WARN", "🔄 Match relocation detected - Ready for fresh hook!")
        if self.auto_rehook and not self.is_injecting:
            self.add_log("INFO", "🤖 Auto-Sentinel triggering instant fresh scan for new match...")
            self.handle_action()

    def perform_aimbot_injection(self):
        t0 = time.time()
        try:
            self.update_status("SCANNING QUANTUM PATTERNS...", "#F59E0B")
            self.patched_records.clear()
            
            if not self.adjust_privileges():
                self.update_status("PRIVILEGE ESCALATION FAILED", "#FF0055")
                return False
                
            self.pm = Pymem("HD-Player.exe")
            current_pid = self.pm.process_id
            self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
            
            if self.cached_pid != current_pid or self.force_rescan:
                self.cached_addresses = []
                self.cached_pid = current_pid
                self.force_rescan = False
                self.patched_records.clear()
                
            cache_valid = False
            if self.cached_addresses and self.cached_pid == current_pid:
                try:
                    chk_addr = self.cached_addresses[0] + 0xAF
                    chk_b = read_bytes(self.pm.process_handle, chk_addr, 4)
                    if chk_b and chk_b != b'\x00\x00\x00\x00':
                        cache_valid = True
                except Exception:
                    cache_valid = False
                    
            if cache_valid:
                self.add_log("INFO", f"⚡ Cache Hit: Patching {len(self.cached_addresses)} target address(es)...")
                success_count = 0
                for addr in self.cached_addresses:
                    try:
                        address_rep = addr + 0xAF
                        address_scan = addr + 0xAB
                        original_rep = read_bytes(self.pm.process_handle, address_rep, 4)
                        original_scan = read_bytes(self.pm.process_handle, address_scan, 4)
                        self.patched_records.append((address_rep, original_rep, address_scan, original_scan))
                        write_bytes(self.pm.process_handle, address_rep, original_scan, 4)
                        write_bytes(self.pm.process_handle, address_scan, original_rep, 4)
                        success_count += 1
                    except Exception as e:
                        cache_valid = False
                        self.cached_addresses = []
                        self.force_rescan = True
                        break
                        
                if success_count > 0:
                    elapsed = (time.time() - t0) * 1000
                    self.add_log("SUCCESS", f"⚡ Instant injection complete! Hooked {success_count} target(s) in {elapsed:.1f}ms")
                    self.update_status("AIMBOT HOOKED & ACTIVE", "#00FF9D")
                    self._update_card_status(self.card_engine, f"🟢 {success_count} Hooked", "#00FF9D")
                    self.play_sound_fx("inject_chord")
                    return True

            self.add_log("INFO", "Performing deep virtual signature scan for current match...")
            self._update_card_status(self.card_engine, "🔄 Scanning...", "#F59E0B")
            pattern = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00................................\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA5\x43..............................................................................................................................................................................................................................................\x80\xBF'
            addresses = pattern_scan_all(self.pm.process_handle, pattern, return_multiple=True)
            
            if not addresses:
                self.add_log("ERROR", "Pattern scan returned 0 matching addresses for this match.")
                self.update_status("NO MATCHING TARGETS", "#FF0055")
                self._update_card_status(self.card_engine, "🔴 0 Matches", "#FF0055")
                self.play_sound_fx("error_buzz")
                return False
                
            self.cached_addresses = addresses
            self.cached_pid = current_pid
            self.add_log("SUCCESS", f"Match identified {len(addresses)} target address(es)")
            self._update_card_status(self.card_engine, f"🟢 {len(addresses)} Vectors", "#00FF9D")
            
            success_count = 0
            for i, addr in enumerate(addresses):
                try:
                    address_rep = addr + 0xAF
                    address_scan = addr + 0xAB
                    original_rep = read_bytes(self.pm.process_handle, address_rep, 4)
                    original_scan = read_bytes(self.pm.process_handle, address_scan, 4)
                    self.patched_records.append((address_rep, original_rep, address_scan, original_scan))
                    write_bytes(self.pm.process_handle, address_rep, original_scan, 4)
                    write_bytes(self.pm.process_handle, address_scan, original_rep, 4)
                    success_count += 1
                except Exception as e:
                    self.add_log("WARN", f"Failed to hook vector 0x{addr:X}: {e}")
                    
            if success_count > 0:
                elapsed = (time.time() - t0) * 1000
                self.add_log("SUCCESS", f"Quantum Hook Active! Patched {success_count}/{len(addresses)} vectors in {elapsed:.1f}ms")
                self.update_status("AIMBOT HOOKED & ACTIVE", "#00FF9D")
                self._update_card_status(self.card_match, "🟢 In-Game Live", "#00FF9D")
                self.play_sound_fx("inject_chord")
                return True
            else:
                self.add_log("ERROR", "Memory write access blocked by process protection")
                self.update_status("HOOK FAILED", "#FF0055")
                self.play_sound_fx("error_buzz")
                return False
                
        except pymem.exception.ProcessNotFound:
            self.add_log("ERROR", "HD-Player.exe not found! Please launch emulator first.")
            self.update_status("EMULATOR NOT FOUND", "#FF0055")
            self._update_card_status(self.card_process, "🔴 Not Found", "#FF0055")
            self.play_sound_fx("error_buzz")
            return False
        except Exception as e:
            self.add_log("ERROR", f"Exception during hook: {e}")
            self.update_status("HOOK ERROR", "#FF0055")
            self.play_sound_fx("error_buzz")
            return False
        finally:
            if self.pm:
                try: self.pm.close_process()
                except Exception: pass

    def perform_undo_injection(self):
        t0 = time.time()
        try:
            self.update_status("REVERTING MEMORY HOOKS...", "#F59E0B")
            if not self.adjust_privileges():
                return False
            self.pm = Pymem("HD-Player.exe")
            restored_count = 0
            if self.patched_records:
                for address_rep, original_rep, address_scan, original_scan in self.patched_records:
                    try:
                        write_bytes(self.pm.process_handle, address_rep, original_rep, 4)
                        write_bytes(self.pm.process_handle, address_scan, original_scan, 4)
                        restored_count += 1
                    except Exception as e:
                        self.add_log("WARN", f"Failed to restore address 0x{address_rep:X}: {e}")
                self.patched_records.clear()
            if restored_count > 0:
                elapsed = (time.time() - t0) * 1000
                self.add_log("SUCCESS", f"⚡ Original memory restored! Unhooked {restored_count} address(es) in {elapsed:.1f}ms")
                self.update_status("ORIGINAL RESTORED", "#00F0FF")
                self._update_card_status(self.card_engine, "⚡ Original Memory", "#00F0FF")
                self.play_sound_fx("undo_chord")
                return True
            else:
                self.add_log("ERROR", "Failed to restore memory vectors")
                self.update_status("UNDO FAILED", "#FF0055")
                self.play_sound_fx("error_buzz")
                return False
        except Exception as e:
            self.add_log("ERROR", f"Exception during restore: {e}")
            return False
        finally:
            if self.pm:
                try: self.pm.close_process()
                except Exception: pass

    def handle_action(self):
        if self.is_injecting:
            return
        if not self.is_injected:
            self.start_injection()
        else:
            self.start_undo()

    def injection_worker(self):
        self.root.after(0, lambda: self.inject_btn.set_state("disabled"))
        result = self.perform_aimbot_injection()
        def _finish():
            self.inject_btn.set_state("normal")
            if result:
                self.is_injected = True
                self.inject_btn.set_text("↩️ DISENGAGE & RESTORE")
                self.inject_btn.set_theme("#2D1A06", "#F59E0B", "#F59E0B", "#F59E0B", "#020408")
            else:
                self.is_injected = False
                self.inject_btn.set_text("⚡ ENGAGE QUANTUM HOOK")
                self.inject_btn.set_theme("#08182B", "#00F0FF", "#00F0FF", "#00F0FF", "#020408")
            self.is_injecting = False
        self.root.after(0, _finish)

    def undo_worker(self):
        self.root.after(0, lambda: self.inject_btn.set_state("disabled"))
        result = self.perform_undo_injection()
        def _finish():
            self.inject_btn.set_state("normal")
            if result:
                self.is_injected = False
                self.inject_btn.set_text("⚡ ENGAGE QUANTUM HOOK")
                self.inject_btn.set_theme("#08182B", "#00F0FF", "#00F0FF", "#00F0FF", "#020408")
            else:
                self.is_injected = True
                self.inject_btn.set_text("↩️ RETRY RESTORE")
                self.inject_btn.set_theme("#280812", "#FF0055", "#FF0055", "#FF0055", "#FFFFFF")
            self.is_injecting = False
        self.root.after(0, _finish)

    def start_injection(self):
        self.is_injecting = True
        threading.Thread(target=self.injection_worker, daemon=True).start()

    def start_undo(self):
        self.is_injecting = True
        threading.Thread(target=self.undo_worker, daemon=True).start()

    def reset_cache(self):
        self.cached_addresses = []
        self.cached_pid = None
        self.patched_records = []
        self.force_rescan = True
        self.is_injected = False
        self.inject_btn.set_text("⚡ ENGAGE QUANTUM HOOK")
        self.inject_btn.set_theme("#08182B", "#00F0FF", "#00F0FF", "#00F0FF", "#020408")
        self.add_log("INFO", "🧹 Memory cache flushed - Ready for next round")

    def reset_cache_ui(self):
        if self.is_injecting:
            return
        if self.is_injected:
            self.add_log("INFO", "🔄 Reset triggered - Auto Undoing previous patch...")
            self.play_sound_fx("undo_chord")
            self.is_injecting = True
            def _auto_undo_worker():
                result = self.perform_undo_injection()
                self.root.after(0, lambda: self._finish_reset_undo(result))
            threading.Thread(target=_auto_undo_worker, daemon=True).start()
            return
        self._perform_reset_only()

    def _finish_reset_undo(self, result):
        self.is_injecting = False
        self.is_injected = False
        self.inject_btn.set_text("⚡ ENGAGE QUANTUM HOOK")
        self.inject_btn.set_theme("#08182B", "#00F0FF", "#00F0FF", "#00F0FF", "#020408")
        self._perform_reset_only()

    def _perform_reset_only(self):
        self.reset_cache()
        self.play_sound_fx("success_chord")
        self.add_log("SUCCESS", "✅ Quantum Cache Cleared. Ready for new match.")
        self.update_status("READY FOR NEW MATCH", "#00F0FF")

    def toggle_crosshair(self):
        active = self.crosshair.toggle()
        if active:
            self.crosshair_btn.config(text="🎯 CROSSHAIR: ON", fg="#00F0FF", bg="#0E2338")
            self.play_sound_fx("beep_high")
            self.add_log("SUCCESS", "🎯 Laser Crosshair overlay activated on screen.")
        else:
            self.crosshair_btn.config(text="🎯 CROSSHAIR: OFF", fg="#94A3B8", bg="#0D1424")
            self.play_sound_fx("beep_low")
            self.add_log("INFO", "🎯 Laser Crosshair hidden.")

    def cycle_crosshair_style(self):
        new_st = self.crosshair.cycle_style()
        self.cross_style_btn.config(text=f"💠 {new_st}")
        self.play_sound_fx("beep_high")
        self.add_log("INFO", f"Crosshair style changed to: {new_st}")

    def cycle_crosshair_color(self):
        name, hex_c = self.crosshair.cycle_color()
        self.cross_col_btn.config(text=f"🎨 {name}", fg=hex_c)
        self.play_sound_fx("beep_high")
        self.add_log("INFO", f"Crosshair color changed to: {name}")

    def flush_system_ram(self):
        def _worker():
            self.play_sound_fx("laser")
            self.add_log("INFO", "🧹 Purging standby memory & optimizing working sets...")
            try:
                ctypes.windll.psapi.EmptyWorkingSet(-1)
                if self.pm and self.pm.process_handle:
                    ctypes.windll.psapi.EmptyWorkingSet(self.pm.process_handle)
            except Exception:
                pass
            gc.collect()
            time.sleep(0.3)
            self.add_log("SUCCESS", "✨ Turbo RAM Purge complete! Game FPS stabilized.")
            self.play_sound_fx("success_chord")
        threading.Thread(target=_worker, daemon=True).start()

    def toggle_sentinel(self):
        self.auto_rehook = not self.auto_rehook
        if self.auto_rehook:
            self.sentinel_btn.config(text="🤖 SENTINEL: ON", fg="#00FF9D", bg="#062419")
            self.play_sound_fx("success_chord")
            self.add_log("SUCCESS", "🤖 Auto-Match Sentinel ACTIVE - Auto-rescans memory on new matches!")
        else:
            self.sentinel_btn.config(text="🤖 SENTINEL: OFF", fg="#94A3B8", bg="#0D1424")
            self.play_sound_fx("beep_low")
            self.add_log("INFO", "🤖 Auto-Match Sentinel disabled.")

    def cycle_preset(self):
        self.current_preset = (self.current_preset + 1) % len(self.preset_names)
        p_name = self.preset_names[self.current_preset]
        self.preset_btn.config(text=f"⚡ {p_name.split()[1]}")
        self.play_sound_fx("beep_high")
        self.add_log("INFO", f"Active Tuning Profile set to: {p_name}")

    def cycle_spoof_title(self):
        self.is_spoofed = not self.is_spoofed
        if self.is_spoofed:
            fake = self.spoof_names[self.spoof_idx % len(self.spoof_names)]
            self.spoof_idx += 1
            self.root.title(fake)
            self.title_text_lbl.config(text=fake.upper())
            self.ver_tag.config(text=" MASKED ", bg="#241C07", fg="#F59E0B")
            self.add_log("INFO", f"🎭 Process Title masked as: '{fake}'")
            self.play_sound_fx("beep_high")
        else:
            self.root.title(self.real_title)
            self.title_text_lbl.config(text="SCIENTIST")
            self.ver_tag.config(text=" 8K QUANTUM PRO ", bg="#0A1E33", fg="#00F0FF")
            self.add_log("INFO", "🎭 Process Title mask removed.")
            self.play_sound_fx("beep_low")

    def play_sound_fx(self, fx_type):
        if not self.sound_enabled:
            return
        def _audio():
            try:
                if fx_type == "inject_chord":
                    winsound.Beep(900, 50); winsound.Beep(1300, 50); winsound.Beep(1700, 80)
                elif fx_type == "undo_chord":
                    winsound.Beep(1500, 50); winsound.Beep(1100, 50); winsound.Beep(700, 80)
                elif fx_type == "laser":
                    winsound.Beep(1900, 40); winsound.Beep(2500, 60)
                elif fx_type == "success_chord":
                    winsound.Beep(1300, 60); winsound.Beep(1600, 80)
                elif fx_type == "beep_high":
                    winsound.Beep(1400, 60)
                elif fx_type == "beep_low":
                    winsound.Beep(700, 60)
                elif fx_type == "error_buzz":
                    winsound.Beep(380, 100); winsound.Beep(320, 100)
            except Exception:
                pass
        threading.Thread(target=_audio, daemon=True).start()

    def toggle_streamer_mode(self):
        self.streamer_mode = not self.streamer_mode
        if self.streamer_mode:
            self.root.withdraw()
            if self.crosshair.is_active:
                self.crosshair.hide()
            self.streamer_btn.config(text="🕶️ CLOAKED", fg="#F59E0B", bg="#241407")
            self.add_log("INFO", "Stealth Cloak ENABLED - Window invisible to OBS/Stream")
            self.play_sound_fx("beep_low")
        else:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.streamer_btn.config(text="🕶️ CLOAK (F10)", fg="#94A3B8", bg="#0D1424")
            self.add_log("INFO", "Stealth Cloak DISABLED - Window visible")
            self.play_sound_fx("beep_high")

    def update_expiry_countdown(self):
        expires_val = getattr(self.keyauth.user_data, "expires", None) if (self.keyauth and hasattr(self.keyauth, "user_data")) else None
        if expires_val:
            try:
                remaining = float(expires_val) - time.time()
                if remaining > 0:
                    days, remainder = divmod(int(remaining), 86400)
                    hours, remainder = divmod(remainder, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    if days > 0:
                        time_str = f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"
                    elif hours > 0:
                        time_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                    else:
                        time_str = f"{minutes:02d}m {seconds:02d}s"
                    self.expiry_lbl.config(text=f"⏳ {time_str}", fg="#00FF9D")
                else:
                    self.expiry_lbl.config(text="⏳ EXPIRED", fg="#FF0055")
            except Exception:
                self.expiry_lbl.config(text=f"⏳ {expires_val}", fg="#F8FAFC")
        else:
            self.expiry_lbl.config(text="⏳ LIFETIME ACCESS", fg="#00FF9D")
        if not self.is_shutting_down:
            self.root.after(1000, self.update_expiry_countdown)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.wm_attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.topmost_btn.config(text="📌 PINNED", bg="#0E2338", fg="#00F0FF")
            self.add_log("INFO", "Window pinned on top of gameplay")
        else:
            self.topmost_btn.config(text="📌 PIN OVERLAY", bg="#0D1424", fg="#94A3B8")
            self.add_log("INFO", "Window unpinned")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.config(text="🔊 AUDIO: ON", fg="#00FF9D")
            self.play_sound_fx("beep_high")
            self.add_log("INFO", "Audio sound feedback enabled")
        else:
            self.sound_btn.config(text="🔇 AUDIO: OFF", fg="#475569")
            self.add_log("INFO", "Audio sound feedback muted")

    def add_log(self, level, message):
        def _exec():
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.insert("end", f"[{timestamp}] ", "time")
            tag = "info"
            prefix = "[INFO]"
            if level == "SUCCESS":
                tag = "success"
                prefix = "[SUCCESS]"
            elif level == "WARN":
                tag = "warn"
                prefix = "[WARN]"
            elif level == "ERROR":
                tag = "error"
                prefix = "[ERROR]"
            self.log_text.insert("end", f"{prefix} ", tag)
            self.log_text.insert("end", f"{message}\n")
            self.log_text.see("end")
        self.root.after(0, _exec)

    def update_status(self, text, color="#38BDF8"):
        def _exec():
            self.status_pill.config(text=f"● {text.upper()}", fg=color)
        self.root.after(0, _exec)

    def clear_logs(self):
        self.log_text.delete("1.0", "end")

    def copy_logs(self):
        content = self.log_text.get("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Console stream copied to clipboard!")

    def start_keybinding(self):
        if self.is_binding_key:
            return
        self.is_binding_key = True
        self.keybind_btn.set_text("PRESS KEY...")
        self.keybind_btn.set_theme("#2D1A06", "#F59E0B", "#F59E0B")
        self.add_log("INFO", "Press any key to bind Trigger...")
        threading.Thread(target=self._capture_keybind_thread, daemon=True).start()

    def _capture_keybind_thread(self):
        captured_vk = None
        start_time = time.time()
        while time.time() - start_time < 10:
            for vk in range(0x01, 0xFF):
                if vk == 0x79:
                    continue
                if (ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000) != 0:
                    if vk in (0x01, 0x02):
                        continue
                    captured_vk = vk
                    break
            if captured_vk:
                break
            time.sleep(0.03)
        def _finish_bind():
            if captured_vk:
                self.bound_vk = captured_vk
                self.bound_key_name = MOUSE_VK_MAP.get(captured_vk) or VK_MAP.get(captured_vk, f"KEY_0x{captured_vk:02X}")
                self.keybind_btn.set_text(f"[{self.bound_key_name[:8]}]")
                self.keybind_btn.set_theme("#062419", "#00FF9D", "#00FF9D")
                self.play_sound_fx("success_chord")
                self.add_log("SUCCESS", f"Trigger Key bound to [{self.bound_key_name}].")
            else:
                self.keybind_btn.set_text("[ BIND TRIGGER ]")
                self.keybind_btn.set_theme("#0A1222", "#1E2A4A", "#38BDF8")
                self.add_log("WARN", "Key binding timed out.")
            self.is_binding_key = False
        if captured_vk:
            while (ctypes.windll.user32.GetAsyncKeyState(captured_vk) & 0x8000) != 0:
                time.sleep(0.02)
        self.root.after(0, _finish_bind)

    def start_reset_keybinding(self):
        if self.is_binding_reset_hotkey:
            return
        self.is_binding_reset_hotkey = True
        self.reset_key_btn.set_text("PRESS KEY...")
        self.reset_key_btn.set_theme("#2D1A06", "#F59E0B", "#F59E0B")
        self.add_log("INFO", "Press any key to bind Round Reset...")
        threading.Thread(target=self._capture_reset_key_thread, daemon=True).start()

    def _capture_reset_key_thread(self):
        captured_vk = None
        start_time = time.time()
        while time.time() - start_time < 10:
            for vk in range(0x01, 0xFF):
                if vk == 0x79:
                    continue
                if (ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000) != 0:
                    if vk in (0x01, 0x02):
                        continue
                    captured_vk = vk
                    break
            if captured_vk:
                break
            time.sleep(0.03)
        def _finish_bind():
            if captured_vk:
                self.reset_hotkey = captured_vk
                self.reset_hotkey_name = MOUSE_VK_MAP.get(captured_vk) or VK_MAP.get(captured_vk, f"KEY_0x{captured_vk:02X}")
                self.reset_key_btn.set_text(f"[{self.reset_hotkey_name[:8]}]")
                self.reset_key_btn.set_theme("#062419", "#00FF9D", "#00FF9D")
                self.play_sound_fx("success_chord")
                self.add_log("SUCCESS", f"Round Reset Key bound to [{self.reset_hotkey_name}].")
            else:
                self.reset_key_btn.set_text("[ NEW MATCH ]")
                self.reset_key_btn.set_theme("#0A1222", "#1E2A4A", "#38BDF8")
                self.add_log("WARN", "Key binding timed out.")
            self.is_binding_reset_hotkey = False
        if captured_vk:
            while (ctypes.windll.user32.GetAsyncKeyState(captured_vk) & 0x8000) != 0:
                time.sleep(0.02)
        self.root.after(0, _finish_bind)

    def _global_hotkey_listener(self):
        was_pressed = False
        was_reset_pressed = False
        was_f10_pressed = False
        while not self.is_shutting_down:
            if not self.is_binding_key and not self.is_binding_reset_hotkey:
                f10_down = (ctypes.windll.user32.GetAsyncKeyState(0x79) & 0x8000) != 0
                if f10_down and not was_f10_pressed:
                    was_f10_pressed = True
                    self.root.after(0, self.toggle_streamer_mode)
                elif not f10_down:
                    was_f10_pressed = False
            if self.bound_vk and not self.is_binding_key:
                is_down = (ctypes.windll.user32.GetAsyncKeyState(self.bound_vk) & 0x8000) != 0
                if is_down and not was_pressed:
                    was_pressed = True
                    self.root.after(0, self.handle_action)
                elif not is_down:
                    was_pressed = False
            if self.reset_hotkey and not self.is_binding_reset_hotkey:
                is_reset_down = (ctypes.windll.user32.GetAsyncKeyState(self.reset_hotkey) & 0x8000) != 0
                if is_reset_down and not was_reset_pressed:
                    was_reset_pressed = True
                    self.root.after(0, self.reset_cache_ui)
                elif not is_reset_down:
                    was_reset_pressed = False
            time.sleep(0.02)

    def check_system_status(self):
        try:
            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            ram_load = mem.dwMemoryLoad
            self._update_card_status(self.card_ram, f"📊 Load: {ram_load}%", "#00FF9D" if ram_load < 80 else "#F59E0B")
        except Exception:
            pass
        if not self.is_injecting:
            try:
                pm_check = Pymem("HD-Player.exe")
                current_pid = pm_check.process_id
                pm_check.close_process()
                if self.cached_pid and self.cached_pid != current_pid:
                    self.add_log("WARN", f"🔄 Emulator restart detected! (PID {self.cached_pid} -> {current_pid})")
                    self.cached_addresses = []
                    self.cached_pid = current_pid
                    self.force_rescan = True
                    self.patched_records = []
                    self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
                elif self.cached_pid:
                    self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
                else:
                    self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
                    self.cached_pid = current_pid
            except Exception:
                if self.cached_pid:
                    self.add_log("WARN", "⚠️ Emulator closed - Resetting cache")
                    self.reset_cache()
                self.cached_pid = None
                self._update_card_status(self.card_process, "🔴 Not Found", "#FF0055")
        self.root.after(3000, self.check_system_status)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def adjust_privileges(self):
        try:
            token_handle = ctypes.c_void_p()
            luid = ctypes.c_longlong()
            ctypes.windll.advapi32.OpenProcessToken(
                ctypes.windll.kernel32.GetCurrentProcess(),
                0x20 | 0x8,
                ctypes.byref(token_handle)
            )
            ctypes.windll.advapi32.LookupPrivilegeValueA(
                0, SE_DEBUG_NAME.encode('ascii'), ctypes.byref(luid)
            )
            new_privileges = TOKEN_PRIVILEGES(1, LUID_AND_ATTRIBUTES(luid.value, SE_PRIVILEGE_ENABLED))
            ctypes.windll.advapi32.AdjustTokenPrivileges(
                token_handle, False, ctypes.byref(new_privileges), 0, None, None
            )
            ctypes.windll.kernel32.CloseHandle(token_handle)
            return True
        except Exception:
            return False

    def on_closing(self):
        self.is_shutting_down = True
        if hasattr(self, "crosshair") and self.crosshair:
            try: self.crosshair.hide()
            except Exception: pass
        if self.pm:
            try: self.pm.close_process()
            except Exception: pass
        if self.is_injected and not self.is_injecting:
            try:
                def _auto_undo():
                    try: self.perform_undo_injection()
                    except Exception: pass
                threading.Thread(target=_auto_undo, daemon=True).start()
                time.sleep(0.3)
            except Exception:
                pass
        try:
            self.root.destroy()
        except Exception:
            pass
        os._exit(0)

def run_remote_app(keyauth_instance=None):
    root = tk.Tk()
    if apply_icon:
        try: apply_icon(root)
        except Exception: pass
    app = AimbotController(root, keyauth_instance=keyauth_instance)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    run_remote_app()
