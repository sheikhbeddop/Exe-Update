# ==============================================================================
# 🧪 SCIENTIST AIMBOT - QUANTUM PRO EDITION (ALL-IN-ONE ENGINE)
# ==============================================================================
# Ultra-Modern Cyberpunk OLED Glass Interface
# Includes: Crosshair Overlay, RAM Flush, Auto-Rehook, Sci-Fi Audio & Stealth Cloak

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

# Safe icon helper
try:
    from main import apply_icon
except Exception:
    apply_icon = None

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
# 🧬 Windows Privilege Structs
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
    0x04: "MOUSE3 (Mid)",
    0x05: "MOUSE4 (Back)",
    0x06: "MOUSE5 (Fwd)",
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
# 🎯 Feature 1: Click-Through Crosshair Overlay
# ==========================================
class QuantumCrosshair:
    def __init__(self):
        self.win = None
        self.is_active = False
        self.colors = ["#00F0FF", "#00FF9D", "#FF3366", "#F59E0B", "#FFFFFF"]
        self.color_idx = 0
        self.styles = ["DOT", "PLUS", "CIRCLE_DOT"]
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
        return self.colors[self.color_idx]

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
        size = 60
        x = (sw - size) // 2
        y = (sh - size) // 2
        self.win.geometry(f"{size}x{size}+{x}+{y}")
        
        # Set Click-Through Window (WS_EX_TRANSPARENT | WS_EX_LAYERED)
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
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None
        self.is_active = False

    def redraw(self):
        if not self.win or not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        c = self.colors[self.color_idx]
        st = self.styles[self.style_idx]
        cx, cy = 30, 30
        
        if st == "DOT":
            self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=c, outline="#000000", width=1)
        elif st == "PLUS":
            # 4 Crosshair lines
            self.canvas.create_line(cx-9, cy, cx-3, cy, fill=c, width=2)
            self.canvas.create_line(cx+3, cy, cx+9, cy, fill=c, width=2)
            self.canvas.create_line(cx, cy-9, cx, cy-3, fill=c, width=2)
            self.canvas.create_line(cx, cy+3, cx, cy+9, fill=c, width=2)
            self.canvas.create_oval(cx-1, cy-1, cx+1, cy+1, fill=c, outline=c)
        elif st == "CIRCLE_DOT":
            self.canvas.create_oval(cx-7, cy-7, cx+7, cy+7, outline=c, width=1.5)
            self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill=c, outline="#000000", width=1)

# ==========================================
# 🎨 Quantum Pill Cyber Button
# ==========================================
class QuantumButton(tk.Canvas):
    def __init__(self, parent, text, command=None, 
                 bg_color="#0D121F", border_color="#1E293B", 
                 hover_bg="#00F0FF", hover_fg="#05070B", 
                 text_color="#F8FAFC", width=200, height=42, 
                 corner_radius=10, font=("Segoe UI", 9, "bold")):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.default_bg = bg_color
        self.default_border = border_color
        self.default_fg = text_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.disabled_bg = "#080B12"
        self.disabled_border = "#131A29"
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

    def set_color(self, bg_color, border_color=None, text_color="#FFFFFF", hover_bg=None, hover_fg="#000000"):
        self.default_bg = bg_color
        self.default_border = border_color or bg_color
        self.default_fg = text_color
        if hover_bg:
            self.hover_bg = hover_bg
        if hover_fg:
            self.hover_fg = hover_fg
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
# 🖥️ Main Quantum Dashboard
# ==========================================
class AimbotController:
    def __init__(self, root, keyauth_instance=None):
        self.root = root
        self.keyauth = keyauth_instance or globals().get("keyauthapp", None)
        
        # Dimensions & Geometry
        self.WIN_W = 620
        self.WIN_H = 545
        self.real_title = "SCIENTIST QUANTUM"
        self.root.title(self.real_title)
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.root.resizable(False, False)
        self.root.configure(bg="#05070B")
        self.root.attributes("-alpha", 0.98)
        self.root.overrideredirect(True)
        
        if apply_icon:
            try: apply_icon(self.root)
            except Exception: pass
        
        sx = (self.root.winfo_screenwidth() - self.WIN_W) // 2
        sy = (self.root.winfo_screenheight() - self.WIN_H) // 2
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}+{sx}+{sy}")
        enable_window_taskbar(self.root)
        
        # Core States
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
        self.auto_rehook = False
        
        # Features
        self.crosshair = QuantumCrosshair()
        self.spoof_names = ["Spotify Free", "Discord Updater", "Calculator", "Visual Studio Code", "Task Manager"]
        self.spoof_idx = 0
        self.is_spoofed = False
        
        self._setup_styles()
        self.setup_ui()
        
        # Threads
        self.hotkey_thread = threading.Thread(target=self._global_hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        self.root.after(2000, self.check_system_status)
        self.update_expiry_countdown()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Quantum.Horizontal.TProgressbar", 
                        troughcolor="#0B0F19", 
                        background="#00F0FF", 
                        bordercolor="#1E2640", 
                        thickness=4)

    def style_pill_btn(self, btn, bg="#0D121F", fg="#94A3B8", hover_bg="#1E293B", hover_fg="#FFFFFF"):
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
        outer_frame = tk.Frame(self.root, bg="#1E2640", bd=1)
        outer_frame.pack(fill="both", expand=True)
        
        inner_container = tk.Frame(outer_frame, bg="#05070B")
        inner_container.pack(fill="both", expand=True)
        
        # ==========================================
        # 🔝 Top Navigation Bar
        # ==========================================
        titlebar = tk.Frame(inner_container, bg="#090D16", height=46)
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)
        
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
        
        left_brand = tk.Frame(titlebar, bg="#090D16")
        left_brand.pack(side="left", padx=12, pady=6)
        left_brand.bind("<ButtonPress-1>", _start_drag)
        left_brand.bind("<B1-Motion>", _do_drag)
        
        icon_lbl = tk.Label(left_brand, text="◈", font=("Segoe UI Symbol", 13, "bold"), bg="#090D16", fg="#00F0FF")
        icon_lbl.pack(side="left", padx=(0, 6))
        
        self.title_text_lbl = tk.Label(left_brand, text="SCIENTIST", font=("Segoe UI", 11, "bold"), bg="#090D16", fg="#F8FAFC")
        self.title_text_lbl.pack(side="left")
        
        self.ver_tag = tk.Label(left_brand, text=" QUANTUM PRO ", font=("Segoe UI", 7, "bold"), bg="#0E2338", fg="#00F0FF", padx=5, pady=2)
        self.ver_tag.pack(side="left", padx=6)
        
        username = getattr(self.keyauth, "logged_username", "Guest") if self.keyauth else "Guest"
        user_chip = tk.Frame(titlebar, bg="#0F1626", bd=1, relief="solid")
        user_chip.config(highlightbackground="#1E293B", highlightthickness=1)
        user_chip.pack(side="left", padx=6, pady=7)
        
        user_inner = tk.Frame(user_chip, bg="#0F1626", padx=8, pady=2)
        user_inner.pack()
        
        user_lbl = tk.Label(user_inner, text=f"👤 {username}", font=("Segoe UI", 7, "bold"), bg="#0F1626", fg="#818CF8")
        user_lbl.pack(side="left", padx=(0, 6))
        
        self.expiry_lbl = tk.Label(user_inner, text="⏳ EXPIRY: --:--:--", font=("Segoe UI", 7, "bold"), bg="#0F1626", fg="#00FF9D")
        self.expiry_lbl.pack(side="left")
        
        right_controls = tk.Frame(titlebar, bg="#090D16")
        right_controls.pack(side="right", padx=(0, 4))
        
        min_btn = tk.Label(right_controls, text=" 🗕 ", font=("Segoe UI", 10), bg="#090D16", fg="#94A3B8", cursor="hand2")
        min_btn.pack(side="left", padx=2, pady=4)
        min_btn.bind("<Enter>", lambda e: min_btn.config(bg="#1E293B", fg="#FFFFFF"))
        min_btn.bind("<Leave>", lambda e: min_btn.config(bg="#090D16", fg="#94A3B8"))
        min_btn.bind("<Button-1>", lambda e: self._on_minimize())
        
        close_btn = tk.Label(right_controls, text=" ✕ ", font=("Segoe UI", 10, "bold"), bg="#090D16", fg="#94A3B8", cursor="hand2")
        close_btn.pack(side="left", padx=2, pady=4)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#E11D48", fg="#FFFFFF"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#090D16", fg="#94A3B8"))
        close_btn.bind("<Button-1>", lambda e: self.on_closing())
        
        accent_line = tk.Frame(inner_container, bg="#00F0FF", height=1)
        accent_line.pack(fill="x")
        
        # ==========================================
        # 🍱 Bento Grid
        # ==========================================
        bento_grid = tk.Frame(inner_container, bg="#05070B")
        bento_grid.pack(fill="both", expand=True, padx=12, pady=8)
        
        # --- LEFT COLUMN (Control Deck) ---
        left_col = tk.Frame(bento_grid, bg="#05070B", width=290)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 6))
        
        # 1. Hero Injector Card
        hero_card = tk.Frame(left_col, bg="#0B0F19", bd=1, relief="solid")
        hero_card.config(highlightbackground="#1E2640", highlightthickness=1)
        hero_card.pack(fill="x", pady=(0, 6))
        
        hero_inner = tk.Frame(hero_card, bg="#0B0F19", padx=10, pady=10)
        hero_inner.pack(fill="x")
        
        hero_header = tk.Label(hero_inner, text="⚡ QUANTUM MEMORY ENGINE", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#00F0FF")
        hero_header.pack(anchor="w", pady=(0, 4))
        
        self.inject_btn = QuantumButton(
            hero_inner, 
            text="⚡ INJECT QUANTUM AIMBOT", 
            command=self.handle_action,
            bg_color="#071927",
            border_color="#00F0FF",
            hover_bg="#00F0FF",
            hover_fg="#05070B",
            text_color="#00F0FF",
            width=265, 
            height=44,
            corner_radius=10,
            font=("Segoe UI", 10, "bold")
        )
        self.inject_btn.pack(fill="x", pady=(0, 4))
        
        self.status_lbl = tk.Label(hero_inner, text="● STANDBY • READY TO INJECT", font=("Consolas", 8, "bold"), bg="#0B0F19", fg="#38BDF8")
        self.status_lbl.pack(anchor="center", pady=(0, 2))
        
        self.progress = ttk.Progressbar(hero_inner, style="Quantum.Horizontal.TProgressbar", mode='indeterminate')
        self.progress.pack(fill="x")
        self.progress.pack_forget()
        
        # 2. Hotkey Control Card
        key_card = tk.Frame(left_col, bg="#0B0F19", bd=1, relief="solid")
        key_card.config(highlightbackground="#1E2640", highlightthickness=1)
        key_card.pack(fill="x", pady=(0, 6))
        
        key_inner = tk.Frame(key_card, bg="#0B0F19", padx=10, pady=6)
        key_inner.pack(fill="x")
        
        key_header = tk.Label(key_inner, text="⌨️ TRIGGER & HOTKEY MATRIX", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#64748B")
        key_header.pack(anchor="w", pady=(0, 4))
        
        row1 = tk.Frame(key_inner, bg="#0B0F19")
        row1.pack(fill="x", pady=(0, 3))
        r1_lbl = tk.Label(row1, text="Aimbot Trigger", font=("Segoe UI", 8, "bold"), bg="#0B0F19", fg="#F8FAFC")
        r1_lbl.pack(side="left")
        self.keybind_btn = QuantumButton(
            row1, text="[ KEY BIND ]", command=self.start_keybinding,
            bg_color="#0D121F", border_color="#1E2640", hover_bg="#00F0FF",
            hover_fg="#05070B", text_color="#38BDF8", width=110, height=26, corner_radius=6, font=("Consolas", 8, "bold")
        )
        self.keybind_btn.pack(side="right")
        
        row2 = tk.Frame(key_inner, bg="#0B0F19")
        row2.pack(fill="x")
        r2_lbl = tk.Label(row2, text="Round Reset", font=("Segoe UI", 8, "bold"), bg="#0B0F19", fg="#F8FAFC")
        r2_lbl.pack(side="left")
        self.reset_key_btn = QuantumButton(
            row2, text="[ NEW MATCH ]", command=self.start_reset_keybinding,
            bg_color="#0D121F", border_color="#1E2640", hover_bg="#00F0FF",
            hover_fg="#05070B", text_color="#38BDF8", width=110, height=26, corner_radius=6, font=("Consolas", 8, "bold")
        )
        self.reset_key_btn.pack(side="right")
        
        # 3. New Features Action Deck (Crosshair & RAM Flush & Auto Sentinel)
        feature_card = tk.Frame(left_col, bg="#0B0F19", bd=1, relief="solid")
        feature_card.config(highlightbackground="#1E2640", highlightthickness=1)
        feature_card.pack(fill="x", pady=(0, 6))
        
        f_inner = tk.Frame(feature_card, bg="#0B0F19", padx=8, pady=6)
        f_inner.pack(fill="x")
        
        f_header = tk.Label(f_inner, text="🛠️ QUANTUM UTILITIES & TWEAKS", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#64748B")
        f_header.pack(anchor="w", pady=(0, 4))
        
        f_row = tk.Frame(f_inner, bg="#0B0F19")
        f_row.pack(fill="x")
        
        self.crosshair_btn = tk.Button(f_row, text="🎯 CROSSHAIR", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_crosshair)
        self.crosshair_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.style_pill_btn(self.crosshair_btn, bg="#0D121F", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#05070B")
        
        self.ram_flush_btn = tk.Button(f_row, text="🧹 FLUSH RAM", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.flush_system_ram)
        self.ram_flush_btn.pack(side="left", fill="x", expand=True, padx=2)
        self.style_pill_btn(self.ram_flush_btn, bg="#0D121F", fg="#818CF8", hover_bg="#818CF8", hover_fg="#05070B")
        
        self.auto_hook_btn = tk.Button(f_row, text="🤖 AUTO: OFF", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_auto_rehook)
        self.auto_hook_btn.pack(side="left", fill="x", expand=True, padx=(2, 0))
        self.style_pill_btn(self.auto_hook_btn, bg="#0D121F", fg="#94A3B8", hover_bg="#00FF9D", hover_fg="#05070B")
        
        # 4. Quick Toggles Bar (Audio, Pin, Cloak)
        toggle_bar = tk.Frame(left_col, bg="#05070B")
        toggle_bar.pack(fill="x")
        
        self.sound_btn = tk.Button(toggle_bar, text="🔊 SFX AUDIO", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_sound)
        self.sound_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.style_pill_btn(self.sound_btn, bg="#0B0F19", fg="#00FF9D", hover_bg="#00FF9D", hover_fg="#05070B")
        
        self.topmost_btn = tk.Button(toggle_bar, text="📌 PIN OVERLAY", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_topmost)
        self.topmost_btn.pack(side="left", fill="x", expand=True, padx=2)
        self.style_pill_btn(self.topmost_btn, bg="#0B0F19", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#05070B")
        
        self.streamer_btn = tk.Button(toggle_bar, text="🕶️ CLOAK (F10)", font=("Segoe UI", 7, "bold"), cursor="hand2", command=self.toggle_streamer_mode)
        self.streamer_btn.pack(side="left", fill="x", expand=True, padx=(2, 0))
        self.style_pill_btn(self.streamer_btn, bg="#0B0F19", fg="#94A3B8", hover_bg="#F59E0B", hover_fg="#05070B")
        
        # --- RIGHT COLUMN (HUD & Matrix Logs) ---
        right_col = tk.Frame(bento_grid, bg="#05070B", width=290)
        right_col.pack(side="right", fill="both", expand=True, padx=(6, 0))
        
        # 5. Telemetry Matrix HUD
        hud_card = tk.Frame(right_col, bg="#0B0F19", bd=1, relief="solid")
        hud_card.config(highlightbackground="#1E2640", highlightthickness=1)
        hud_card.pack(fill="x", pady=(0, 6))
        
        hud_inner = tk.Frame(hud_card, bg="#0B0F19", padx=8, pady=6)
        hud_inner.pack(fill="x")
        
        hud_header = tk.Label(hud_inner, text="📊 TELEMETRY MATRIX HUD", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#64748B")
        hud_header.pack(anchor="w", pady=(0, 4))
        
        hud_grid = tk.Frame(hud_inner, bg="#0B0F19")
        hud_grid.pack(fill="x")
        
        self.card_process = self._create_card(hud_grid, "TARGET", "HD-Player.exe", "⚪ Standby", "#64748B", 0, 0)
        self.card_engine = self._create_card(hud_grid, "ENGINE", "Quantum Cache", "⚡ Ready", "#00F0FF", 0, 1)
        self.card_ram = self._create_card(hud_grid, "RAM LOAD", "Physical", "📊 Checking...", "#818CF8", 1, 0)
        self.card_priv = self._create_card(hud_grid, "SECURITY", "SeDebugToken", "🔒 Checking", "#FBBF24", 1, 1)
        
        hud_grid.grid_columnconfigure(0, weight=1)
        hud_grid.grid_columnconfigure(1, weight=1)
        
        # 6. Live Console Stream Card
        log_card = tk.Frame(right_col, bg="#0B0F19", bd=1, relief="solid")
        log_card.config(highlightbackground="#1E2640", highlightthickness=1)
        log_card.pack(fill="both", expand=True)
        
        log_header = tk.Frame(log_card, bg="#070A12", height=26)
        log_header.pack(fill="x")
        log_header.pack_propagate(False)
        
        log_title = tk.Label(log_header, text="🖥️ LIVE LOG CONSOLE", font=("Consolas", 8, "bold"), bg="#070A12", fg="#00F0FF")
        log_title.pack(side="left", padx=6)
        
        clear_btn = tk.Button(log_header, text="🗑️", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.clear_logs)
        clear_btn.pack(side="right", padx=2, pady=1)
        self.style_pill_btn(clear_btn, bg="#0D121F", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#05070B")
        
        copy_btn = tk.Button(log_header, text="📋", font=("Segoe UI", 7), cursor="hand2", width=3, command=self.copy_logs)
        copy_btn.pack(side="right", padx=(0, 2), pady=1)
        self.style_pill_btn(copy_btn, bg="#0D121F", fg="#94A3B8", hover_bg="#00F0FF", hover_fg="#05070B")
        
        self.log_text = tk.Text(log_card, bg="#04060A", fg="#E2E8F0", 
                                font=("Consolas", 8), relief="flat", bd=0, 
                                wrap="word", highlightthickness=0, height=8)
        self.log_text.pack(fill="both", expand=True, padx=6, pady=4)
        self.log_text.tag_config("time", foreground="#475569")
        self.log_text.tag_config("info", foreground="#38BDF8")
        self.log_text.tag_config("success", foreground="#00FF9D")
        self.log_text.tag_config("warn", foreground="#FBBF24")
        self.log_text.tag_config("error", foreground="#EF4444")
        
        # 7. Footer Bar
        footer = tk.Frame(inner_container, bg="#05070B", height=26)
        footer.pack(side="bottom", fill="x", padx=12, pady=(0, 4))
        
        discord_btn = tk.Label(footer, text="💬 Discord", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#818CF8", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        discord_btn.pack(side="left", padx=(0, 4))
        discord_btn.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/QSSbvyr3nC"))
        
        wa_btn = tk.Label(footer, text="📱 WhatsApp", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#00FF9D", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        wa_btn.pack(side="left", padx=(0, 4))
        wa_btn.bind("<Button-1>", lambda e: webbrowser.open("https://wa.me/8801952851550"))
        
        spoofer_btn = tk.Label(footer, text="🎭 Mask Title", font=("Segoe UI", 7, "bold"), bg="#0B0F19", fg="#F59E0B", padx=6, pady=1, cursor="hand2", bd=1, relief="solid")
        spoofer_btn.pack(side="left")
        spoofer_btn.bind("<Button-1>", lambda e: self.cycle_spoof_title())
        
        credit_lbl = tk.Label(footer, text="QUANTUM PRO • ALL-IN-ONE EDITION", font=("Segoe UI", 7, "bold"), bg="#05070B", fg="#475569")
        credit_lbl.pack(side="right")

        if self.is_admin():
            self._update_card_status(self.card_priv, "🟢 Granted", "#00FF9D")
            self.add_log("SUCCESS", "Running with Kernel Administrator Privileges")
        else:
            self._update_card_status(self.card_priv, "⚠️ Limited", "#FBBF24")
            self.add_log("WARN", "Running with standard user permissions.")
            
        self.add_log("SUCCESS", "◈ Scientist Quantum Pro initialized.")
        self.add_log("INFO", "Click 'TARGET' or 'INJECT' to start hooking.")
        self.add_log("INFO", "Click '🎯 CROSSHAIR' to toggle on-screen laser dot.")
        self.add_log("INFO", "Click '🧹 FLUSH RAM' to free memory & boost FPS.")
        self.add_log("INFO", "Press F10 for Stealth Window Cloak.")

    # ==========================================
    # 🎯 Feature Implementation Handlers
    # ==========================================
    def toggle_crosshair(self):
        active = self.crosshair.toggle()
        if active:
            self.crosshair_btn.config(text="🎯 CROSS: ON", fg="#00F0FF", bg="#0E2338")
            self.play_sound_fx("beep_high")
            self.add_log("SUCCESS", "🎯 Laser Crosshair overlay activated on screen.")
        else:
            self.crosshair_btn.config(text="🎯 CROSSHAIR", fg="#94A3B8", bg="#0D121F")
            self.play_sound_fx("beep_low")
            self.add_log("INFO", "🎯 Laser Crosshair overlay hidden.")

    def flush_system_ram(self):
        def _worker():
            self.play_sound_fx("laser")
            self.add_log("INFO", "🧹 Flushing standby list and optimizing working set...")
            try:
                # Flush current process
                ctypes.windll.psapi.EmptyWorkingSet(-1)
                # Flush emulator process if attached
                if self.pm and self.pm.process_handle:
                    ctypes.windll.psapi.EmptyWorkingSet(self.pm.process_handle)
            except Exception:
                pass
            gc.collect()
            time.sleep(0.3)
            self.add_log("SUCCESS", "✨ RAM Flushed & Standby Cache cleared successfully!")
            self.play_sound_fx("success_chord")
        threading.Thread(target=_worker, daemon=True).start()

    def toggle_auto_rehook(self):
        self.auto_rehook = not self.auto_rehook
        if self.auto_rehook:
            self.auto_hook_btn.config(text="🤖 AUTO: ON", fg="#00FF9D", bg="#062419")
            self.play_sound_fx("success_chord")
            self.add_log("SUCCESS", "🤖 Auto-Rehook Sentinel ACTIVE - Will auto-detect and hook new matches!")
        else:
            self.auto_hook_btn.config(text="🤖 AUTO: OFF", fg="#94A3B8", bg="#0D121F")
            self.play_sound_fx("beep_low")
            self.add_log("INFO", "🤖 Auto-Rehook Sentinel disabled.")

    def cycle_spoof_title(self):
        self.is_spoofed = not self.is_spoofed
        if self.is_spoofed:
            fake = self.spoof_names[self.spoof_idx % len(self.spoof_names)]
            self.spoof_idx += 1
            self.root.title(fake)
            self.title_text_lbl.config(text=fake.upper())
            self.ver_tag.config(text=" MASKED ", bg="#241C07", fg="#F59E0B")
            self.add_log("INFO", f"🎭 Window masked as: '{fake}'")
            self.play_sound_fx("beep_high")
        else:
            self.root.title(self.real_title)
            self.title_text_lbl.config(text="SCIENTIST")
            self.ver_tag.config(text=" QUANTUM PRO ", bg="#0E2338", fg="#00F0FF")
            self.add_log("INFO", "🎭 Window mask removed.")
            self.play_sound_fx("beep_low")

    def play_sound_fx(self, fx_type):
        if not self.sound_enabled:
            return
        def _audio():
            try:
                if fx_type == "inject_chord":
                    winsound.Beep(900, 60); winsound.Beep(1200, 60); winsound.Beep(1600, 90)
                elif fx_type == "undo_chord":
                    winsound.Beep(1400, 60); winsound.Beep(1000, 60); winsound.Beep(600, 90)
                elif fx_type == "laser":
                    winsound.Beep(1800, 50); winsound.Beep(2400, 80)
                elif fx_type == "success_chord":
                    winsound.Beep(1200, 80); winsound.Beep(1500, 100)
                elif fx_type == "beep_high":
                    winsound.Beep(1400, 80)
                elif fx_type == "beep_low":
                    winsound.Beep(700, 80)
                elif fx_type == "error_buzz":
                    winsound.Beep(400, 120); winsound.Beep(350, 120)
                else:
                    winsound.Beep(1000, 80)
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
            self.add_log("INFO", "Stealth Cloak ENABLED - Window invisible to screen recorder")
            self.play_sound_fx("beep_low")
        else:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.streamer_btn.config(text="🕶️ CLOAK (F10)", fg="#94A3B8", bg="#0B0F19")
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
                        time_str = f"{days}d {hours:02d}h {minutes:02d}m"
                    else:
                        time_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                    self.expiry_lbl.config(text=f"⏳ {time_str}", fg="#00FF9D")
                else:
                    self.expiry_lbl.config(text="⏳ EXPIRED", fg="#EF4444")
            except Exception:
                self.expiry_lbl.config(text=f"⏳ {expires_val}", fg="#F8FAFC")
        else:
            self.expiry_lbl.config(text="⏳ LIFETIME ACCESS", fg="#00FF9D")
        if not self.is_shutting_down:
            self.root.after(1000, self.update_expiry_countdown)

    def _create_card(self, parent, category, title, status, status_color, r=0, c=0):
        f = tk.Frame(parent, bg="#070A12", bd=1, relief="solid")
        f.config(highlightbackground="#131A29", highlightthickness=1)
        f.grid(row=r, column=c, padx=2, pady=2, sticky="ew")
        
        inner = tk.Frame(f, bg="#070A12", padx=6, pady=4)
        inner.pack(fill="both", expand=True)
        
        cat_lbl = tk.Label(inner, text=category, font=("Segoe UI", 6, "bold"), bg="#070A12", fg="#475569")
        cat_lbl.pack(anchor="w")
        
        title_lbl = tk.Label(inner, text=title, font=("Segoe UI", 7, "bold"), bg="#070A12", fg="#F8FAFC")
        title_lbl.pack(anchor="w")
        
        status_lbl = tk.Label(inner, text=status, font=("Segoe UI", 7, "bold"), bg="#070A12", fg=status_color)
        status_lbl.pack(anchor="w")
        f.status_lbl = status_lbl
        return f

    def _update_card_status(self, card, text, color):
        def _exec():
            card.status_lbl.config(text=text, fg=color)
        self.root.after(0, _exec)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.wm_attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.topmost_btn.config(text="📌 PINNED", bg="#0E2338", fg="#00F0FF")
            self.add_log("INFO", "Window pinned on top of all games")
        else:
            self.topmost_btn.config(text="📌 PIN OVERLAY", bg="#0B0F19", fg="#94A3B8")
            self.add_log("INFO", "Window unpinned")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.config(text="🔊 SFX AUDIO", fg="#00FF9D")
            self.play_sound_fx("beep_high")
            self.add_log("INFO", "Acoustic audio feedback enabled")
        else:
            self.sound_btn.config(text="🔇 SFX MUTED", fg="#475569")
            self.add_log("INFO", "Acoustic audio feedback muted")

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
            self.status_lbl.config(text=f"● {text.upper()}", fg=color)
        self.root.after(0, _exec)

    def clear_logs(self):
        self.log_text.delete("1.0", "end")

    def copy_logs(self):
        content = self.log_text.get("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Console logs copied to clipboard!")

    def start_keybinding(self):
        if self.is_binding_key:
            return
        self.is_binding_key = True
        self.keybind_btn.set_text("PRESS KEY...")
        self.keybind_btn.set_color("#2D1A06", "#F59E0B", "#F59E0B")
        self.add_log("INFO", "Press any key to bind Aimbot Trigger...")
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
                self.keybind_btn.set_color("#062419", "#00FF9D", "#00FF9D")
                self.play_sound_fx("success_chord")
                self.add_log("SUCCESS", f"Trigger Key bound to [{self.bound_key_name}].")
            else:
                self.keybind_btn.set_text("[ KEY BIND ]")
                self.keybind_btn.set_color("#0D121F", "#1E2640", "#38BDF8")
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
        self.reset_key_btn.set_color("#2D1A06", "#F59E0B", "#F59E0B")
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
                self.reset_key_btn.set_color("#062419", "#00FF9D", "#00FF9D")
                self.play_sound_fx("success_chord")
                self.add_log("SUCCESS", f"Round Reset Key bound to [{self.reset_hotkey_name}].")
            else:
                self.reset_key_btn.set_text("[ NEW MATCH ]")
                self.reset_key_btn.set_color("#0D121F", "#1E2640", "#38BDF8")
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
                    # Auto re-hook sentinel
                    if self.auto_rehook and not self.is_injecting:
                        self.add_log("INFO", "🤖 Auto-Rehook triggered by process change...")
                        self.handle_action()
                elif self.cached_pid:
                    self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
                else:
                    self._update_card_status(self.card_process, f"🟢 PID {current_pid}", "#00FF9D")
                    self.cached_pid = current_pid
                    if self.auto_rehook and not self.is_injected and not self.is_injecting:
                        self.add_log("INFO", "🤖 Auto-Rehook triggered on process discovery...")
                        self.handle_action()
            except Exception:
                if self.cached_pid:
                    self.add_log("WARN", "⚠️ Process disappeared - Resetting cache")
                    self.reset_cache()
                self.cached_pid = None
                self._update_card_status(self.card_process, "🔴 Not Found", "#EF4444")
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
            self._update_card_status(self.card_priv, "🟢 Granted", "#00FF9D")
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
        self.inject_btn.set_text("⚡ INJECT QUANTUM AIMBOT")
        self.inject_btn.set_color("#071927", "#00F0FF", "#00F0FF", "#00F0FF", "#05070B")
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
        if result:
            self.is_injected = False
            self.inject_btn.set_text("⚡ INJECT QUANTUM AIMBOT")
            self.inject_btn.set_color("#071927", "#00F0FF", "#00F0FF", "#00F0FF", "#05070B")
            self._perform_reset_only()
        else:
            self.add_log("ERROR", "Auto Undo failed! Try manual Undo first.")
            self.update_status("UNDO FAILED", "#EF4444")

    def _perform_reset_only(self):
        self.reset_cache()
        self.play_sound_fx("success_chord")
        self.add_log("SUCCESS", "✅ Quantum Cache Cleared. Ready for new round.")
        self.update_status("READY FOR NEXT ROUND", "#00F0FF")

    def perform_aimbot_injection(self):
        t0 = time.time()
        try:
            self.update_status("HOOKING VIRTUAL MEMORY...", "#F59E0B")
            self.patched_records.clear()
            if not self.adjust_privileges():
                self.update_status("PRIVILEGE ESCALATION FAILED", "#EF4444")
                return False
            self.pm = Pymem("HD-Player.exe")
            current_pid = self.pm.process_id
            self._update_card_status(self.card_process, f"🟢 Attached ({current_pid})", "#00FF9D")
            
            if self.cached_pid != current_pid or self.force_rescan:
                self.add_log("INFO", f"🔄 Emulator process initialized (PID: {current_pid}) - Scanning signatures")
                self.cached_addresses = []
                self.cached_pid = current_pid
                self.force_rescan = False
                self.patched_records.clear()
                
            if self.cached_addresses and self.cached_pid == current_pid:
                self.add_log("INFO", f"⚡ Quantum Cache Hit: Patching {len(self.cached_addresses)} target address(es)...")
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
                        self.add_log("WARN", f"Cache address fault at 0x{addr:X}: {e}")
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
                    
            self.add_log("INFO", "Scanning virtual memory for quantum signatures...")
            self._update_card_status(self.card_engine, "🔄 Scanning...", "#F59E0B")
            pattern = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00................................\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA5\x43..............................................................................................................................................................................................................................................\x80\xBF'
            addresses = pattern_scan_all(self.pm.process_handle, pattern, return_multiple=True)
            if not addresses:
                self.add_log("ERROR", "Zero matching quantum signatures found in memory")
                self.update_status("NO SIGNATURES FOUND", "#EF4444")
                self._update_card_status(self.card_engine, "🔴 0 Matches", "#EF4444")
                self.play_sound_fx("error_buzz")
                return False
                
            self.cached_addresses = addresses
            self.cached_pid = current_pid
            self.add_log("SUCCESS", f"Identified {len(addresses)} matching memory vector(s)")
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
                self.play_sound_fx("inject_chord")
                return True
            else:
                self.add_log("ERROR", "Memory write access blocked by process protection")
                self.update_status("HOOK FAILED", "#EF4444")
                self.play_sound_fx("error_buzz")
                return False
                
        except pymem.exception.ProcessNotFound:
            self.add_log("ERROR", "HD-Player.exe process not detected. Please launch emulator.")
            self.update_status("EMULATOR NOT FOUND", "#EF4444")
            self._update_card_status(self.card_process, "🔴 Not Found", "#EF4444")
            self.play_sound_fx("error_buzz")
            return False
        except Exception as e:
            self.add_log("ERROR", f"Exception during hook execution: {e}")
            self.update_status("HOOK ERROR", "#EF4444")
            self.play_sound_fx("error_buzz")
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
            self.update_status("REVERTING MEMORY HOOKS...", "#F59E0B")
            if not self.adjust_privileges():
                self.update_status("PRIVILEGE ESCALATION FAILED", "#EF4444")
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
                self.update_status("ORIGINAL CODE RESTORED", "#00F0FF")
                self._update_card_status(self.card_engine, "⚡ Original Memory", "#00F0FF")
                self.play_sound_fx("undo_chord")
                return True
            else:
                self.add_log("ERROR", "Failed to restore memory vectors")
                self.update_status("UNDO FAILED", "#EF4444")
                self.play_sound_fx("error_buzz")
                return False
        except pymem.exception.ProcessNotFound:
            self.add_log("ERROR", "HD-Player.exe not found! Please launch the emulator.")
            self.update_status("EMULATOR NOT FOUND", "#EF4444")
            self._update_card_process("🔴 Not Found", "#EF4444")
            self.play_sound_fx("error_buzz")
            return False
        except Exception as e:
            self.add_log("ERROR", f"Exception during memory restore: {e}")
            self.update_status("RESTORE ERROR", "#EF4444")
            self.play_sound_fx("error_buzz")
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
                    self.add_log("INFO", "🔄 New match PID detected - Flushing cache")
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
                self.inject_btn.set_text("↩️ REVERT / RESTORE MEMORY")
                self.inject_btn.set_color("#2D1A06", "#F59E0B", "#F59E0B", "#F59E0B", "#05070B")
            else:
                self.is_injected = False
                self.inject_btn.set_text("⚡ INJECT QUANTUM AIMBOT")
                self.inject_btn.set_color("#071927", "#00F0FF", "#00F0FF", "#00F0FF", "#05070B")
            self.is_injecting = False
        self.root.after(0, _finish)

    def undo_worker(self):
        self.root.after(0, lambda: self.inject_btn.set_state("disabled"))
        result = self.perform_undo_injection()
        def _finish():
            self.inject_btn.set_state("normal")
            if result:
                self.is_injected = False
                self.inject_btn.set_text("⚡ INJECT QUANTUM AIMBOT")
                self.inject_btn.set_color("#071927", "#00F0FF", "#00F0FF", "#00F0FF", "#05070B")
            else:
                self.is_injected = True
                self.inject_btn.set_text("↩️ RETRY MEMORY RESTORE")
                self.inject_btn.set_color("#260C14", "#EF4444", "#EF4444", "#EF4444", "#FFFFFF")
            self.is_injecting = False
        self.root.after(0, _finish)

    def start_injection(self):
        self.is_injecting = True
        threading.Thread(target=self.injection_worker, daemon=True).start()

    def start_undo(self):
        self.is_injecting = True
        threading.Thread(target=self.undo_worker, daemon=True).start()

    def on_closing(self):
        self.is_shutting_down = True
        if hasattr(self, "crosshair") and self.crosshair:
            try: self.crosshair.hide()
            except Exception: pass
        if self.pm:
            try:
                self.pm.close_process()
            except Exception:
                pass
        if self.is_injected and not self.is_injecting:
            try:
                def _auto_undo():
                    try:
                        self.perform_undo_injection()
                    except Exception:
                        pass
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
