import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from tkcalendar import DateEntry

try:
    from tkcalendar import Calendar
    HAS_CALENDAR = True

except ImportError:
    HAS_CALENDAR = False

# ─── Light palette ────────────────────────────────────────────────────────────
C = {"bg": "#F4F7FB", "panel": "#FFFFFF", "card": "#FFFFFF", "card_alt": "#F0F5FB", "input": "#FFFFFF",
     "input_bd": "#ADC0D4", "accent1": "#1A6FC4", "accent2": "#D05A10", "accent3": "#2A8C3F", "accent4": "#B07800",
     "text": "#1C2B3A", "subtext": "#6B7F94", "border": "#D0DCE8", "ok": "#2A8C3F",
     "warn": "#D05A10", "err": "#C0253A", "hdr_bg": "#1A3A5C", "hdr_fg": "#E8F4FF", "hover": "#e6f0ff", }

MODE_COLOR = {"flight": C["accent1"], "car": C["accent2"], "train": C["accent3"]}
MODE_ICON = {"flight": "✈", "car": "🚗", "train": "🚆"}

CITY_SUGGESTIONS = sorted([ "Amsterdam", "Athens", "Barcelona", "Berlin", "Brașov", "Bucharest",
    "Budapest", "Cluj-Napoca", "Copenhagen", "Dublin", "Frankfurt",
    "Geneva", "Hamburg", "Helsinki", "Iași", "Istanbul", "Lisbon",
    "London", "Luxembourg", "Lyon", "Madrid", "Milan", "Munich",
    "Nice", "Oslo", "Paris", "Prague", "Rome", "Rotterdam",
    "Sofia", "Stockholm", "Timișoara", "Vienna", "Warsaw", "Zurich", ])

FT = ("Segoe UI", 18, "bold")
FH = ("Segoe UI", 11, "bold")
FB = ("Segoe UI", 10)
FS = ("Segoe UI", 9)
FSB = ("Segoe UI", 9, "bold")

def lbl(parent, text, font=None, fg=None, bg=None, **kw):
    return tk.Label(parent, text=text, font=font or FB, fg=fg or C["text"], bg=bg or C["panel"], **kw)

def hsep(parent, padx=10, pady=4):
    tk.Frame(parent, height=1, bg=C["border"]).pack(fill="x", padx=padx, pady=pady)

def vsep(parent):
    return tk.Frame(parent, width=1, bg=C["border"])

def action_btn(parent, text, command, color=None, fg="white", width=None):
    b = tk.Button(parent, text=text, command=command, font=FSB, fg=fg, bg=color or C["accent1"],
                  activebackground="#0F4A8A", activeforeground="white", relief="flat", bd=0, padx=14, pady=7, cursor="hand2")
    if width:
        b.config(width=width)
    return b

def styled_combo(parent, values, textvariable=None, width=14):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("L.TCombobox", fieldbackground=C["input"], background=C["input"],
                    foreground=C["text"], arrowcolor=C["accent1"], bordercolor=C["input_bd"], lightcolor=C["input_bd"],
                    darkcolor=C["input_bd"], selectbackground=C["accent1"], selectforeground="white")
    return ttk.Combobox(parent, values=values, textvariable=textvariable, width=width, font=FB, state="readonly", style="L.TCombobox")

def outlined_date(parent, textvariable=None, width=14):
    wrap = tk.Frame(parent, bg=C["input_bd"], padx=1, pady=1)

    if HAS_CALENDAR:
        from datetime import date
        d = DateEntry(wrap, textvariable=textvariable, font=FB, background=C["accent1"], foreground="white",
                      normalbackground=C["input"], normalforeground=C["text"], borderwidth=0,
                      date_pattern="yyyy-mm-dd", mindate=date.today(), width=width, showweeknumbers=False)
        d.pack(fill="x", padx=2, pady=2)
        return wrap, d
    else:
        e = tk.Entry( wrap, textvariable=textvariable, width=width, font=FB, fg=C["text"], bg=C["input"],
            insertbackground=C["accent1"], relief="flat", bd=4, highlightthickness=0 )
        e.pack(fill="x")
        return wrap, e

def fmt_time(minutes):
    h, m = divmod(int(minutes), 60)
    return f"{h}h {m:02d}m" if h else f"{m}m"
