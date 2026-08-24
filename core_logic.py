# ==========================================
# 🧪 SCIENTIST AIMBOT - REMOTE CORE LOGIC
# ==========================================
# This file is loaded dynamically from GitHub / Cloud
# Any updates made here instantly take effect on all client EXEs!

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
import math

def enable_window_taskbar(window):
    """Ensures a borderless Tkinter window appears in the Windows taskbar and Alt-Tab."""
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if not hwnd:
            hwnd = window.winfo_id()
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
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

# ==========================================
# ⌨️ Virtual Key Mapping
# ==========================================
MOUSE_VK_MAP = {
    0x04: "MOUSE3 (Middle)",
    0x05: "MOUSE4 (Side Back)",
    0x06: "MOUSE5 (Side Forward)",
}

VK_MAP = {
    0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
    0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
    0x2D: "INSERT", 0x2E: "DELETE", 0x24: "HOME", 0x23: "END", 0x21: "PAGEUP", 0x22: "PAGEDOWN",
    0x14: "CAPSLOCK", 0x09: "TAB", 0x20: "SPACE",
    0x60: "NUM0", 0x61: "NUM1", 0x62: "NUM2", 0x63: "NUM3", 0x64: "NUM4",
    0x65: "NUM5", 0x66: "NUM6", 0x67: "NUM7", 0x68: "NUM8", 0x69: "NUM9",
}
for c in range(0x41, 0x5B): VK_MAP[c] = chr(c)
for n in range(0x30, 0x3A): VK_MAP[n] = chr(n)

# ==========================================
# 🎨 CyberButton Component
# ==========================================
class CyberButton(tk.Canvas):
    def __init__(self, parent, text, command=None, bg_color="#0D111A", border_color="#1E293B", 
                 hover_bg="#6366F1", hover_fg="#FFFFFF", text_color="#FFFFFF", 
                 width=180, height=42, corner_radius=8, font=("Segoe UI", 9, "bold")):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.default_bg = bg_color
        self.default_border = border_color
        self.default_fg = text_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.disabled_bg = "#0F131D"
        self.disabled_border = "#1B2234"
        self.disabled_fg = "#475569"
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.font = font
        self.text_str = text
        self.is_enabled = True
        self.rect = self._draw_rounded_rect(1, 1, width-2, height-2, corner_radius, fill=self.bg_color, outline=self.border_color, width=1)
        self.text = self.create_text(width // 2, height // 2, text=self.text_str, fill=self.text_color, font=self.font)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        for item in (self.rect, self.text):
            self.tag_bind(item, "<Enter>", self._on_enter)
            self.tag_bind(item, "<Leave>", self._on_leave)
            self.tag_bind(item, "<Button-1>", self._on_click)

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_text(self, new_text):
        self.text_str = new_text
        self.itemconfig(self.text, text=new_text)

    def set_color(self, bg_color, hover_color=None):
        color_mappings = {
            "#ED8936": ("#241407", "#F59E0B", "#F59E0B", "#000000"),
            "#C05621": ("#241407", "#F59E0B", "#F59E0B", "#000000"),
            "#E53E3E": ("#260C14", "#EF4444", "#EF4444", "#FFFFFF"),
            "#C53030": ("#260C14", "#EF4444", "#EF4444", "#FFFFFF"),
            "#FF3366": ("#052414", "#00FF66", "#00FF66", "#000000"),
            "#E6004C": ("#052414", "#00FF66", "#00FF66", "#000000"),
            "#1E2638": ("#0D111A", "#1E293B", "#FFFFFF", "#FFFFFF"),
            "#2D3952": ("#0D111A", "#1E293B", "#FFFFFF", "#FFFFFF"),
            "#2D3748": ("#0D111A", "#1E293B", "#FFFFFF", "#FFFFFF"),
            "#4A5568": ("#0D111A", "#1E293B", "#FFFFFF", "#FFFFFF"),
            "#F6AD55": ("#241C07", "#FBBF24", "#FBBF24", "#000000"),
            "#DD6B20": ("#241C07", "#FBBF24", "#FBBF24", "#000000"),
            "#48BB78": ("#052414", "#00FF66", "#00FF66", "#000000"),
            "#38A169": ("#052414", "#00FF66", "#00FF66", "#000000"),
        }
        if bg_color in color_mappings:
            bg, border, text, hover_fg = color_mappings[bg_color]
            self.default_bg = bg
            self.default_border = border
            self.default_fg = text
            self.hover_bg = border
            self.hover_fg = hover_fg
        else:
            self.default_bg = bg_color
            self.default_border = hover_color if hover_color else bg_color
            self.default_fg = "#FFFFFF"
            self.hover_bg = hover_color if hover_color else bg_color
            self.hover_fg = "#000000"
        if self.is_enabled:
            self.bg_color = self.default_bg
            self.border_color = self.default_border
            self.text_color = self.default_fg
            self.itemconfig(self.rect, fill=self.bg_color, outline=self.border_color)
            self.itemconfig(self.text, fill=self.text_color)

    def set_state(self, state):
        if state == "disabled":
            self.is_enabled = False
            self.bg_color = self.disabled_bg
            self.border_color = self.disabled_border
            self.text_color = self.disabled_fg
            self.itemconfig(self.rect, fill=self.bg_color, outline=self.border_color)
            self.itemconfig(self.text, fill=self.text_color)
            self.config(cursor="")
        else:
            self.is_enabled = True
            self.bg_color = self.default_bg
            self.border_color = self.default_border
            self.text_color = self.default_fg
            self.itemconfig(self.rect, fill=self.bg_color, outline=self.border_color)
            self.itemconfig(self.text, fill=self.text_color)
            self.config(cursor="hand2")

    def _on_enter(self, event=None):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)
            self.itemconfig(self.text, fill=self.hover_fg)
            self.config(cursor="hand2")

    def _on_leave(self, event=None):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.default_bg, outline=self.default_border)
            self.itemconfig(self.text, fill=self.default_fg)
            self.config(cursor="")

    def _on_click(self, event=None):
        if self.is_enabled and self.command:
            self.command()

# ==========================================
# 🖥️ Main Dashboard (Cyber-Glass Luxury Theme)
# ==========================================
class AimbotController:
    def __init__(self, root, keyauth_instance=None):
        self.root = root
        self.keyauth = keyauth_instance or globals().get("keyauthapp", None)
        self.WIN_W = 590
        self.WIN_H = 505
        self.root.title("Scientists Aimbot")
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.root.resizable(False, False)
        self.root.configure(bg="#0A0D14")
        self.root.attributes("-alpha", 0.96)
        self.root.overrideredirect(True)
        
        if "apply_icon" in globals():
            try:
                apply_icon(self.root)
            except Exception:
                pass
        
        # Center window on screen
        sx = (self.root.winfo_screenwidth() - self.WIN_W) // 2
        sy = (self.root.winfo_screenheight() - self.WIN_H) // 2
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}+{sx}+{sy}")
        
        enable_window_taskbar(self.root)
        
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
        self._setup_styles()
        self.setup_ui()
        self.hotkey_thread = threading.Thread(target=self._global_hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        self.root.after(2000, self.check_system_status)
        self.update_expiry_countdown()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Cyber.Horizontal.TProgressbar", 
                        troughcolor="#0A0D14", 
                        background="#00FF66", 
                        bordercolor="#1E293B", 
                        thickness=4)

    def style_raw_btn(self, btn, bg="#111622", fg="#94A3B8", hover_bg="#1E293B", hover_fg="#FFFFFF"):
        btn.config(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=hover_fg, bd=1, relief="solid", highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg) if btn['state'] != 'disabled' else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg) if btn['state'] != 'disabled' else None)

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
        # 1px border stroke around entire main window
        outer_frame = tk.Frame(self.root, bg="#1E293B", bd=1)
        outer_frame.pack(fill="both", expand=True)
        
        inner_container = tk.Frame(outer_frame, bg="#0A0D14")
        inner_container.pack(fill="both", expand=True)
        
        # ==========================================
        # 🔝 Top Navigation & Title Bar
        # ==========================================
        titlebar = tk.Frame(inner_container, bg="#0A0D14", height=42)
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)
        
        # Drag handling
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
        
        # Left brand info
        left_brand = tk.Frame(titlebar, bg="#0A0D14")
        left_brand.pack(side="left", padx=12, pady=6)
        left_brand.bind("<ButtonPress-1>", _start_drag)
        left_brand.bind("<B1-Motion>", _do_drag)
        
        icon_lbl = tk.Label(left_brand, text="🧪", font=("Segoe UI Emoji", 11), bg="#0A0D14")
        icon_lbl.pack(side="left", padx=(0, 6))
        icon_lbl.bind("<ButtonPress-1>", _start_drag)
        icon_lbl.bind("<B1-Motion>", _do_drag)
        
        title_text = tk.Label(left_brand, text="SCIENTIST [🔥 CLOUD V3.0]", font=("Segoe UI", 10, "bold"), bg="#0A0D14", fg="#F59E0B")
        title_text.pack(side="left")
        title_text.bind("<ButtonPress-1>", _start_drag)
        title_text.bind("<B1-Motion>", _do_drag)
        
        ver_tag = tk.Label(left_brand, text=" 🚀 AUTO-UPDATED V 3.0 ", font=("Segoe UI", 7, "bold"), bg="#241C07", fg="#00FF66", padx=6, pady=2)
        ver_tag.pack(side="left", padx=6)
        ver_tag.bind("<ButtonPress-1>", _start_drag)
        ver_tag.bind("<B1-Motion>", _do_drag)
        
        # Middle User/Expiry Chip
        username = getattr(self.keyauth, "logged_username", "Guest") if self.keyauth else "Guest"
        user_chip = tk.Frame(titlebar, bg="#111622", bd=1, relief="solid")
        user_chip.config(highlightbackground="#1E293B", highlightthickness=1)
        user_chip.pack(side="left", padx=10, pady=7)
        user_chip.bind("<ButtonPress-1>", _start_drag)
        user_chip.bind("<B1-Motion>", _do_drag)
        
        user_inner = tk.Frame(user_chip, bg="#111622", padx=8, pady=2)
        user_inner.pack()
        user_inner.bind("<ButtonPress-1>", _start_drag)
        user_inner.bind("<B1-Motion>", _do_drag)
        
        user_lbl = tk.Label(user_inner, text=f"👤 {username}", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#38BDF8")
        user_lbl.pack(side="left", padx=(0, 6))
        user_lbl.bind("<ButtonPress-1>", _start_drag)
        user_lbl.bind("<B1-Motion>", _do_drag)
        
        self.expiry_lbl = tk.Label(user_inner, text="⏳ EXPIRY: --:--:--", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#00FF66")
        self.expiry_lbl.pack(side="left")
        self.expiry_lbl.bind("<ButtonPress-1>", _start_drag)
        self.expiry_lbl.bind("<B1-Motion>", _do_drag)
        
        # Right window controls (Minimize & Close)
        right_controls = tk.Frame(titlebar, bg="#0A0D14")
        right_controls.pack(side="right")
        
        min_btn = tk.Label(right_controls, text="  🗕  ", font=("Segoe UI", 10), bg="#0A0D14", fg="#94A3B8", cursor="hand2")
        min_btn.pack(side="left", fill="y", ipadx=6)
        min_btn.bind("<Enter>", lambda e: min_btn.config(bg="#1E293B", fg="#FFFFFF"))
        min_btn.bind("<Leave>", lambda e: min_btn.config(bg="#0A0D14", fg="#94A3B8"))
        min_btn.bind("<Button-1>", lambda e: self._on_minimize())
        
        close_btn = tk.Label(right_controls, text="  ✕  ", font=("Segoe UI", 10, "bold"), bg="#0A0D14", fg="#94A3B8", cursor="hand2")
        close_btn.pack(side="left", fill="y", ipadx=6)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#E11D48", fg="#FFFFFF"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#0A0D14", fg="#94A3B8"))
        close_btn.bind("<Button-1>", lambda e: self.on_closing())
        
        # Top Accent Line
        accent_line = tk.Frame(inner_container, bg="#6366F1", height=1)
        accent_line.pack(fill="x")
        
        # ==========================================
        # 🎛️ 2-Column Bento Grid Core
        # ==========================================
        bento_grid = tk.Frame(inner_container, bg="#0A0D14")
        bento_grid.pack(fill="both", expand=True, padx=12, pady=10)
        
        # ------------------------------------------
        # 🚀 LEFT COLUMN: Execution & Controls Core
        # ------------------------------------------
        left_col = tk.Frame(bento_grid, bg="#0A0D14", width=275)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 6))
        
        # 1. Hero Injector Card
        hero_card = tk.Frame(left_col, bg="#111622", bd=1, relief="solid")
        hero_card.config(highlightbackground="#1E293B", highlightthickness=1)
        hero_card.pack(fill="x", pady=(0, 8))
        
        hero_inner = tk.Frame(hero_card, bg="#111622", padx=12, pady=10)
        hero_inner.pack(fill="x")
        
        hero_header = tk.Label(hero_inner, text="⚡ CORE INJECTION ENGINE", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#64748B")
        hero_header.pack(anchor="w", pady=(0, 6))
        
        self.inject_btn = CyberButton(
            hero_inner, 
            text="⚡ INJECT AIMBOT [CLOUD V3.0]", 
            command=self.handle_action,
            bg_color="#052414",
            border_color="#00FF66",
            hover_bg="#00FF66",
            hover_fg="#000000",
            text_color="#00FF66",
            width=250, 
            height=46
        )
        self.inject_btn.pack(fill="x", pady=(0, 6))
        
        self.status_lbl = tk.Label(hero_inner, text="[ STANDBY - READY TO INJECT ]", font=("Consolas", 7, "bold"), bg="#111622", fg="#38BDF8")
        self.status_lbl.pack(anchor="center", pady=(0, 4))
        
        self.progress = ttk.Progressbar(hero_inner, style="Cyber.Horizontal.TProgressbar", mode='indeterminate')
        self.progress.pack(fill="x")
        self.progress.pack_forget()
        
        # 2. Hotkey Assignment Card
        key_card = tk.Frame(left_col, bg="#111622", bd=1, relief="solid")
        key_card.config(highlightbackground="#1E293B", highlightthickness=1)
        key_card.pack(fill="x", pady=(0, 8))
        
        key_inner = tk.Frame(key_card, bg="#111622", padx=12, pady=8)
        key_inner.pack(fill="x")
        
        key_header = tk.Label(key_inner, text="⌨️ HOTKEY ASSIGNMENTS", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#64748B")
        key_header.pack(anchor="w", pady=(0, 6))
        
        # Row 1 (Aimbot Trigger)
        row1 = tk.Frame(key_inner, bg="#111622")
        row1.pack(fill="x", pady=(0, 4))
        r1_lbl = tk.Label(row1, text="Aimbot Trigger", font=("Segoe UI", 8, "bold"), bg="#111622", fg="#FFFFFF")
        r1_lbl.pack(side="left")
        self.keybind_btn = CyberButton(
            row1,
            text="[ KEY BIND ]",
            command=self.start_keybinding,
            bg_color="#0D111A",
            border_color="#1E293B",
            hover_bg="#6366F1",
            hover_fg="#FFFFFF",
            text_color="#38BDF8",
            width=110,
            height=26,
            corner_radius=6,
            font=("Consolas", 8, "bold")
        )
        self.keybind_btn.pack(side="right")
        
        # Row 2 (New Match Reset)
        row2 = tk.Frame(key_inner, bg="#111622")
        row2.pack(fill="x")
        r2_lbl = tk.Label(row2, text="New Match Reset", font=("Segoe UI", 8, "bold"), bg="#111622", fg="#FFFFFF")
        r2_lbl.pack(side="left")
        self.reset_key_btn = CyberButton(
            row2,
            text="[ NEW MATCH ]",
            command=self.start_reset_keybinding,
            bg_color="#0D111A",
            border_color="#1E293B",
            hover_bg="#6366F1",
            hover_fg="#FFFFFF",
            text_color="#38BDF8",
            width=110,
            height=26,
            corner_radius=6,
            font=("Consolas", 8, "bold")
        )
        self.reset_key_btn.pack(side="right")
        
        # 3. Quick Feature Toggles Bar
        toggle_bar = tk.Frame(left_col, bg="#0A0D14")
        toggle_bar.pack(fill="x")
        
        self.sound_btn = tk.Button(toggle_bar, text="🔊 AUDIO", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_sound)
        self.sound_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.style_raw_btn(self.sound_btn, bg="#111622", fg="#00FF66", hover_bg="#00FF66", hover_fg="#000000")
        
        self.topmost_btn = tk.Button(toggle_bar, text="📌 PIN TOP", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_topmost)
        self.topmost_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.style_raw_btn(self.topmost_btn, bg="#111622", fg="#94A3B8", hover_bg="#6366F1", hover_fg="#FFFFFF")
        
        self.streamer_btn = tk.Button(toggle_bar, text="🕶️ STREAM", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_streamer_mode)
        self.streamer_btn.pack(side="left", fill="x", expand=True)
        self.style_raw_btn(self.streamer_btn, bg="#111622", fg="#94A3B8", hover_bg="#F59E0B", hover_fg="#000000")
        
        # ------------------------------------------
        # 📡 RIGHT COLUMN: Telemetry HUD & Log Stream
        # ------------------------------------------
        right_col = tk.Frame(bento_grid, bg="#0A0D14", width=275)
        right_col.pack(side="right", fill="both", expand=True, padx=(6, 0))
        
        # 1. Telemetry HUD
        hud_card = tk.Frame(right_col, bg="#111622", bd=1, relief="solid")
        hud_card.config(highlightbackground="#1E293B", highlightthickness=1)
        hud_card.pack(fill="x", pady=(0, 8))
        
        hud_inner = tk.Frame(hud_card, bg="#111622", padx=10, pady=8)
        hud_inner.pack(fill="x")
        
        hud_header = tk.Label(hud_inner, text="📊 SYSTEM TELEMETRY HUD", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#64748B")
        hud_header.pack(anchor="w", pady=(0, 6))
        
        hud_grid = tk.Frame(hud_inner, bg="#111622")
        hud_grid.pack(fill="x")
        
        self.card_process = self._create_card(hud_grid, "PROCESS", "HD-Player.exe", "⚪ Standby", "#64748B", 0, 0)
        self.card_engine = self._create_card(hud_grid, "ENGINE", "Ultra Cache", "⚡ Ready", "#38BDF8", 0, 1)
        self.card_ram = self._create_card(hud_grid, "RAM LOAD", "Physical", "📊 Checking...", "#38BDF8", 1, 0)
        self.card_priv = self._create_card(hud_grid, "PRIVILEGE", "SeDebugToken", "🔒 Checking", "#FBBF24", 1, 1)
        
        hud_grid.grid_columnconfigure(0, weight=1)
        hud_grid.grid_columnconfigure(1, weight=1)
        
        # 2. Compact Live Log Stream
        log_card = tk.Frame(right_col, bg="#111622", bd=1, relief="solid")
        log_card.config(highlightbackground="#1E293B", highlightthickness=1)
        log_card.pack(fill="both", expand=True)
        
        log_header = tk.Frame(log_card, bg="#0D111A", height=28)
        log_header.pack(fill="x")
        log_header.pack_propagate(False)
        
        log_title = tk.Label(log_header, text="🖥️ LIVE LOG STREAM", font=("Consolas", 8, "bold"), bg="#0D111A", fg="#00FF66")
        log_title.pack(side="left", padx=8)
        
        copy_btn = tk.Button(log_header, text="📋", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.copy_logs)
        copy_btn.pack(side="right", padx=(0, 4), pady=2)
        self.style_raw_btn(copy_btn, bg="#111622", fg="#94A3B8", hover_bg="#00FF66", hover_fg="#000000")
        
        save_btn = tk.Button(log_header, text="💾", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.save_log_file)
        save_btn.pack(side="right", padx=2, pady=2)
        self.style_raw_btn(save_btn, bg="#111622", fg="#8E8E93", hover_bg="#00FF66", hover_fg="#000000")
        
        clear_btn = tk.Button(log_header, text="🗑️", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.clear_logs)
        clear_btn.pack(side="right", padx=2, pady=2)
        self.style_raw_btn(clear_btn, bg="#111622", fg="#8E8E93", hover_bg="#00FF66", hover_fg="#000000")
        
        self.log_text = tk.Text(log_card, bg="#080A0F", fg="#E2E8F0", 
                                font=("Consolas", 8), relief="flat", bd=0, 
                                wrap="word", highlightthickness=0, height=7)
        self.log_text.pack(fill="both", expand=True, padx=6, pady=6)
        self.log_text.tag_config("time", foreground="#64748B")
        self.log_text.tag_config("info", foreground="#38BDF8")
        self.log_text.tag_config("success", foreground="#00FF66")
        self.log_text.tag_config("warn", foreground="#FBBF24")
        self.log_text.tag_config("error", foreground="#EF4444")
        
        # ==========================================
        # 🔻 Bottom Quick Bar
        # ==========================================
        footer = tk.Frame(inner_container, bg="#0A0D14", height=28)
        footer.pack(side="bottom", fill="x", padx=12, pady=(0, 6))
        
        discord_btn = tk.Label(footer, text="💬 Discord", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#38BDF8", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        discord_btn.pack(side="left", padx=(0, 6))
        discord_btn.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/QSSbvyr3nC"))
        
        wa_btn = tk.Label(footer, text="📱 WhatsApp", font=("Segoe UI", 7, "bold"), bg="#111622", fg="#00FF66", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        wa_btn.pack(side="left")
        wa_btn.bind("<Button-1>", lambda e: webbrowser.open("https://wa.me/8801952851550"))
        
        credit_lbl = tk.Label(footer, text="DEVELOPED BY GOMON // V 1.0", font=("Segoe UI", 7, "bold"), bg="#0A0D14", fg="#475569")
        credit_lbl.pack(side="right")

        if self.is_admin():
            self._update_card_status(self.card_priv, "🟢 Granted", "#00FF66")
            self.add_log("SUCCESS", "Application running with Administrator Privileges")
        else:
            self._update_card_status(self.card_priv, "⚠️ Limited", "#FBBF24")
            self.add_log("WARN", "Not running as Administrator. Privileges may be limited.")
            
        self.add_log("SUCCESS", "🔥 [CLOUD LIVE AUTO-UPDATE] V3.0 ACTIVE & SYNCED WITH GITHUB!")
        self.add_log("SUCCESS", "⚡ Cloud V3.0 remote payload loaded successfully!")
        self.add_log("INFO", "Click 'KEY BIND' to set Aimbot Hotkey")
        self.add_log("INFO", "Click 'NEW MATCH KEY' to set Reset Cache Hotkey")
        self.add_log("INFO", "Press F10 to toggle Streamer Mode")

    def toggle_streamer_mode(self):
        self.streamer_mode = not self.streamer_mode
        if self.streamer_mode:
            self.root.withdraw()
            self.streamer_btn.config(text="🕶️ HIDDEN", fg="#F59E0B", bg="#241407")
            self.add_log("INFO", "Streamer Mode ENABLED - Window hidden")
            self.play_sound(1000, 80)
        else:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.streamer_btn.config(text="🕶️ STREAM", fg="#94A3B8", bg="#111622")
            self.add_log("INFO", "Streamer Mode DISABLED - Window visible")
            self.play_sound(800, 80)

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
                        time_str = f"{days}d {hours:02d}h {minutes:02d}m"
                    else:
                        time_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                    self.expiry_lbl.config(text=f"⏳ {time_str}", fg="#00FF66")
                else:
                    self.expiry_lbl.config(text="⏳ EXPIRED", fg="#EF4444")
            except Exception:
                self.expiry_lbl.config(text=f"⏳ {expires_val}", fg="#FFFFFF")
        else:
            self.expiry_lbl.config(text="⏳ LIFETIME", fg="#00FF66")
        if not self.is_shutting_down:
            self.root.after(1000, self.update_expiry_countdown)

    def _create_card(self, parent, category, title, status, status_color, r=0, c=0):
        f = tk.Frame(parent, bg="#0D111A", bd=1, relief="solid")
        f.config(highlightbackground="#1E293B", highlightthickness=1)
        f.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
        
        inner = tk.Frame(f, bg="#0D111A", padx=6, pady=4)
        inner.pack(fill="both", expand=True)
        
        cat_lbl = tk.Label(inner, text=category, font=("Segoe UI", 6, "bold"), bg="#0D111A", fg="#64748B")
        cat_lbl.pack(anchor="w")
        
        title_lbl = tk.Label(inner, text=title, font=("Segoe UI", 7, "bold"), bg="#0D111A", fg="#FFFFFF")
        title_lbl.pack(anchor="w")
        
        color_map = {
            "#48BB78": "#00FF66",
            "#38BDF8": "#00F0FF",
            "#F56565": "#EF4444",
            "#F6AD55": "#F59E0B",
            "#718096": "#64748B"
        }
        mapped_color = color_map.get(status_color, status_color)
        status_lbl = tk.Label(inner, text=status, font=("Segoe UI", 7, "bold"), bg="#0D111A", fg=mapped_color)
        status_lbl.pack(anchor="w")
        f.status_lbl = status_lbl
        return f

    def _update_card_status(self, card, text, color):
        color_map = {
            "#48BB78": "#00FF66",
            "#38BDF8": "#00F0FF",
            "#F56565": "#EF4444",
            "#F6AD55": "#F59E0B",
            "#718096": "#64748B"
        }
        mapped_color = color_map.get(color, color)
        def _exec():
            card.status_lbl.config(text=text, fg=mapped_color)
        self.root.after(0, _exec)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.wm_attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.topmost_btn.config(text="📌 PINNED", bg="#062419", fg="#00FF66")
            self.add_log("INFO", "Window set to Always On Top")
        else:
            self.topmost_btn.config(text="📌 PIN TOP", bg="#111622", fg="#94A3B8")
            self.add_log("INFO", "Always On Top unpinned")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.config(text="🔊 AUDIO", fg="#00FF66")
            self.play_sound(1000, 80)
            self.add_log("INFO", "Audio sound feedback enabled")
        else:
            self.sound_btn.config(text="🔇 AUDIO", fg="#64748B")
            self.add_log("INFO", "Audio sound feedback disabled")

    def play_sound(self, freq, duration):
        if self.sound_enabled:
            def _beep():
                try:
                    winsound.Beep(freq, duration)
                except Exception:
                    pass
            threading.Thread(target=_beep, daemon=True).start()

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
            self.status_lbl.config(text=f"[ {text.upper()} ]", fg=color)
        self.root.after(0, _exec)

    def clear_logs(self):
        self.log_text.delete("1.0", "end")

    def copy_logs(self):
        content = self.log_text.get("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Terminal logs copied to clipboard!")

    def save_log_file(self):
        content = self.log_text.get("1.0", "end")
        default_name = f"Scientists_Log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                initialfile=default_name,
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                self.add_log("SUCCESS", f"Logs exported to {os.path.basename(filepath)}")
                self.play_sound(1000, 100)
            except Exception as e:
                self.add_log("ERROR", f"Failed to save log file: {e}")

    def start_keybinding(self):
        if self.is_binding_key:
            return
        self.is_binding_key = True
        self.keybind_btn.set_text("PRESS KEY...")
        self.keybind_btn.set_color("#F6AD55", "#DD6B20")
        self.add_log("INFO", "Press any key to bind Aimbot Hotkey...")
        thread = threading.Thread(target=self._capture_keybind_thread, daemon=True)
        thread.start()

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
                self.keybind_btn.set_color("#48BB78", "#38A169")
                self.play_sound(1200, 100)
                self.add_log("SUCCESS", f"Aimbot Hotkey bound to [{self.bound_key_name}].")
            else:
                self.keybind_btn.set_text("[ KEY BIND ]")
                self.keybind_btn.set_color("#1E2638", "#2D3952")
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
        self.reset_key_btn.set_color("#F6AD55", "#DD6B20")
        self.add_log("INFO", "Press any key to bind New Match Hotkey...")
        thread = threading.Thread(target=self._capture_reset_key_thread, daemon=True)
        thread.start()

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
                self.reset_key_btn.set_color("#48BB78", "#38A169")
                self.play_sound(1200, 100)
                self.add_log("SUCCESS", f"New Match Hotkey bound to [{self.reset_hotkey_name}].")
            else:
                self.reset_key_btn.set_text("[ NEW MATCH ]")
                self.reset_key_btn.set_color("#2D3748", "#4A5568")
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
            self._update_card_status(self.card_ram, f"📊 Load: {ram_load}%", "#34D399" if ram_load < 80 else "#F6AD55")
        except Exception:
            pass
        if not self.is_injected and not self.is_injecting:
            try:
                pm_check = Pymem("HD-Player.exe")
                current_pid = pm_check.process_id
                pm_check.close_process()
                if self.cached_pid and self.cached_pid != current_pid:
                    self.add_log("WARN", f"🔄 Process PID changed! Old: {self.cached_pid}, New: {current_pid}")
                    self.cached_addresses = []
                    self.cached_pid = current_pid
                    self.force_rescan = True
                    self.patched_records = []
                    self._update_card_status(self.card_process, f"🟢 New Match (PID {current_pid})", "#00FF66")
                elif self.cached_pid:
                    self._update_card_status(self.card_process, f"🟢 Active (PID {current_pid})", "#00FF66")
                else:
                    self._update_card_status(self.card_process, "🟢 Process Active", "#00FF66")
                    self.cached_pid = current_pid
            except Exception:
                if self.cached_pid:
                    self.add_log("WARN", "⚠️ Process disappeared - Reset state")
                    self.reset_cache()
                self.cached_pid = None
                self._update_card_status(self.card_process, "🔴 Not Found", "#FF3B30")
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
            self._update_card_status(self.card_priv, "🟢 Granted", "#00FF66")
            return True
        except Exception as e:
            self.add_log("ERROR", f"Failed to adjust privileges: {e}")
            self._update_card_status(self.card_priv, "🔴 Failed", "#EF4444")
            return False

    def reset_cache(self):
        self.cached_addresses = []
        self.cached_pid = None
        self.patched_records = []
        self.force_rescan = True
        self.is_injected = False
        self.inject_btn.set_text("⚡ INJECT AIMBOT")
        self.inject_btn.set_color("#FF3366", "#E6004C")
        self.add_log("INFO", "🧹 Cache and state reset - Ready for new match")

    def reset_cache_ui(self):
        if self.is_injecting:
            return
        if self.is_injected:
            self.add_log("INFO", "🔄 Reset triggered - Auto Undoing first...")
            self.play_sound(800, 100)
            self.is_injecting = True
            def _auto_undo_worker():
                result = self.perform_undo_injection()
                self.root.after(0, lambda: self._finish_reset_undo(result))
            threading.Thread(target=_auto_undo_worker, daemon=True).start()
            return
        self._perform_reset_only()

    def _finish_reset_undo(self, result):
        self.is_injecting = False
        if result:
            self.is_injected = False
            self.inject_btn.set_text("⚡ INJECT AIMBOT")
            self.inject_btn.set_color("#FF3366", "#E6004C")
            self._perform_reset_only()
        else:
            self.add_log("ERROR", "Auto Undo failed! Try manual Undo first.")
            self.update_status("UNDO FAILED", "#EF4444")

    def _perform_reset_only(self):
        self.reset_cache()
        self.play_sound(1000, 80)
        self.add_log("SUCCESS", "✅ Cache cleared. Ready for new match.")
        self.update_status("READY FOR NEW MATCH", "#00F0FF")

    def perform_aimbot_injection(self):
        t0 = time.time()
        try:
            self.update_status("INJECTING PATTERN...", "#FFCC00")
            self.patched_records.clear()
            if not self.adjust_privileges():
                self.update_status("PRIVILEGE ADJUSTMENT FAILED", "#FF3B30")
                return False
            self.pm = Pymem("HD-Player.exe")
            current_pid = self.pm.process_id
            self._update_card_status(self.card_process, f"🟢 Attached (PID {current_pid})", "#00FF66")
            if self.cached_pid != current_pid or self.force_rescan:
                self.add_log("INFO", f"🔄 New process detected (PID: {current_pid}) - Forcing full scan")
                self.cached_addresses = []
                self.cached_pid = current_pid
                self.force_rescan = False
                self.patched_records.clear()
            if self.cached_addresses and self.cached_pid == current_pid:
                self.add_log("INFO", f"⚡ Instant patch using {len(self.cached_addresses)} cached target address(es)...")
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
                        self.add_log("WARN", f"Cache hit failed at 0x{addr:X}: {e}")
                        self.cached_addresses = []
                        self.force_rescan = True
                        break
                if success_count > 0:
                    elapsed = (time.time() - t0) * 1000
                    self.add_log("SUCCESS", f"⚡ Instant injection complete! Patched {success_count} address(es) in {elapsed:.1f}ms")
                    self.update_status("AIMBOT ACTIVATED & RUNNING", "#00FF66")
                    self._update_card_status(self.card_engine, f"🟢 {success_count} Cached", "#00FF66")
                    self.play_sound(1200, 120)
                    return True
            self.add_log("INFO", "Scanning virtual memory for target signature pattern...")
            self._update_card_status(self.card_engine, "🔄 Scanning...", "#FFCC00")
            pattern = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00................................\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA5\x43..............................................................................................................................................................................................................................................\x80\xBF'
            addresses = pattern_scan_all(self.pm.process_handle, pattern, return_multiple=True)
            if not addresses:
                self.add_log("ERROR", "Pattern scan returned 0 matching memory addresses")
                self.update_status("NO MATCHING ADDRESSES FOUND", "#FF3B30")
                self._update_card_status(self.card_engine, "🔴 0 Matches", "#FF3B30")
                self.play_sound(400, 180)
                return False
            self.cached_addresses = addresses
            self.cached_pid = current_pid
            self.add_log("SUCCESS", f"Signature scan identified {len(addresses)} target address(es)")
            self._update_card_status(self.card_engine, f"🟢 {len(addresses)} Matched", "#00FF66")
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
                    self.add_log("WARN", f"Failed to patch address 0x{addr:X}: {e}")
            if success_count > 0:
                elapsed = (time.time() - t0) * 1000
                self.add_log("SUCCESS", f"Initial injection complete! Patched {success_count}/{len(addresses)} addresses in {elapsed:.1f}ms")
                self.update_status("AIMBOT ACTIVATED & RUNNING", "#00FF66")
                self.play_sound(1200, 120)
                return True
            else:
                self.add_log("ERROR", "Zero memory addresses were successfully patched")
                self.update_status("INJECTION PATCH FAILED", "#FF3B30")
                self.play_sound(400, 180)
                return False
        except pymem.exception.ProcessNotFound:
            self.add_log("ERROR", "HD-Player.exe not found! Please launch the emulator first.")
            self.update_status("PROCESS NOT FOUND", "#FF3B30")
            self._update_card_status(self.card_process, "🔴 Not Found", "#FF3B30")
            self.play_sound(400, 180)
            return False
        except Exception as e:
            self.add_log("ERROR", f"Unexpected error during injection: {e}")
            self.update_status("INJECTION ERROR OCCURRED", "#FF3B30")
            self.play_sound(400, 180)
            return False
        finally:
            if self.pm:
                try:
                    self.pm.close_process()
                except Exception:
                    pass

    def perform_undo_injection(self):
        t0 = time.time()
        try:
            self.update_status("REVERTING PATCH...", "#FFCC00")
            if not self.adjust_privileges():
                self.update_status("PRIVILEGE ADJUSTMENT FAILED", "#FF3B30")
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
                self.add_log("SUCCESS", f"⚡ Instant undo complete! Restored {restored_count} address(es) in {elapsed:.1f}ms")
                self.update_status("PATCH UNDONE / ORIGINAL RESTORED", "#00F0FF")
                self._update_card_status(self.card_engine, "⚡ Original Code", "#00F0FF")
                self.play_sound(800, 100)
                return True
            else:
                self.add_log("ERROR", "Failed to restore memory addresses")
                self.update_status("UNDO FAILED", "#FF3B30")
                self.play_sound(400, 180)
                return False
        except pymem.exception.ProcessNotFound:
            self.add_log("ERROR", "HD-Player.exe not found! Please launch the emulator first.")
            self.update_status("PROCESS NOT FOUND", "#FF3B30")
            self._update_card_status(self.card_process, "🔴 Not Found", "#FF3B30")
            self.play_sound(400, 180)
            return False
        except Exception as e:
            self.add_log("ERROR", f"Unexpected error during undo: {e}")
            self.update_status("UNDO ERROR OCCURRED", "#FF3B30")
            self.play_sound(400, 180)
            return False
        finally:
            if self.pm:
                try:
                    self.pm.close_process()
                except Exception:
                    pass

    def handle_action(self):
        if self.is_injecting:
            return
        if not self.is_injected:
            try:
                pm_check = Pymem("HD-Player.exe")
                current_pid = pm_check.process_id
                pm_check.close_process()
                if self.cached_pid != current_pid:
                    self.add_log("INFO", "🔄 New match detected - Resetting cache")
                    self.reset_cache()
            except:
                pass
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
                self.inject_btn.set_text("↩️ UNDO INJECTION")
                self.inject_btn.set_color("#ED8936", "#C05621")
            else:
                self.is_injected = False
                self.inject_btn.set_text("⚡ INJECT AIMBOT")
                self.inject_btn.set_color("#FF3366", "#E6004C")
            self.is_injecting = False
        self.root.after(0, _finish)

    def undo_worker(self):
        self.root.after(0, lambda: self.inject_btn.set_state("disabled"))
        result = self.perform_undo_injection()
        def _finish():
            self.inject_btn.set_state("normal")
            if result:
                self.is_injected = False
                self.inject_btn.set_text("⚡ INJECT AIMBOT")
                self.inject_btn.set_color("#FF3366", "#E6004C")
            else:
                self.is_injected = True
                self.inject_btn.set_text("↩️ RETRY UNDO")
                self.inject_btn.set_color("#E53E3E", "#C53030")
            self.is_injecting = False
        self.root.after(0, _finish)

    def start_injection(self):
        self.is_injecting = True
        thread = threading.Thread(target=self.injection_worker, daemon=True)
        thread.start()

    def start_undo(self):
        self.is_injecting = True
        thread = threading.Thread(target=self.undo_worker, daemon=True)
        thread.start()

    def on_closing(self):
        self.is_shutting_down = True
        if self.pm:
            try:
                self.pm.close_process()
            except Exception:
                pass
        if self.is_injected and not self.is_injecting:
            try:
                self.add_log("INFO", "🛑 Closing EXE - Auto Undo initiated...")
                def _auto_undo():
                    try:
                        self.perform_undo_injection()
                    except Exception:
                        pass
                threading.Thread(target=_auto_undo, daemon=True).start()
                time.sleep(0.5)
            except Exception:
                pass
        self.root.destroy()

def run_remote_app(keyauth_instance=None):
    """Entry point called when loaded remotely."""
    root = tk.Tk()
    if "apply_icon" in globals():
        try:
            apply_icon(root)
        except Exception:
            pass
    app = AimbotController(root, keyauth_instance=keyauth_instance)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    run_remote_app()
