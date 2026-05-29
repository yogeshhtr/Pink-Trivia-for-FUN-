# -*- coding: utf-8 -*-
"""
theme.py — TP Games
Shared dark-pink theme CSS, colour palette, and session-state helpers.
"""

DARK  = "#1A0A12"
DARK2 = "#2A1020"
DARK3 = "#3A1830"
CARD  = "#2D1224"
CARD2 = "#3D1E34"
BORDER= "#8B2050"
PINK  = "#FF1493"
PINK2 = "#FF69B4"
PINK3 = "#FFB6C1"
TEXT  = "#F8D7E8"
TEXT2 = "#C2547A"
TEXT3 = "#8B3060"
GREEN = "#4CAF50"
RED   = "#E91E63"
GOLD  = "#FFD700"

LUDO_HEX   = {"Red":"#E91E63","Green":"#4CAF50","Yellow":"#FFC107","Blue":"#2196F3"}
LUDO_DARK  = {"Red":"#880E4F","Green":"#1B5E20","Yellow":"#795548","Blue":"#0D47A1"}
LUDO_LIGHT = {"Red":"#4A0020","Green":"#0A2A10","Yellow":"#2A1E00","Blue":"#0A1A3A"}

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background-color: #1A0A12 !important;
    color: #F8D7E8 !important;
}
.stApp {
    background: linear-gradient(135deg, #1A0A12 0%, #2A1020 60%, #1A0A12 100%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2D1224 0%, #1A0A12 100%) !important;
    border-right: 1px solid #8B2050 !important;
}
[data-testid="stSidebar"] * { color: #F8D7E8 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important; font-weight: 700 !important;
    padding: 6px 0 !important;
}
[data-testid="stSidebar"] hr { border-color: #8B2050 !important; }

/* ── Headings ── */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #FF1493 !important; text-align: center;
    text-shadow: 0 0 20px rgba(255,20,147,.5);
}
h2 { font-family: 'Orbitron', sans-serif !important; color: #FF69B4 !important; }
h3 { color: #FFB6C1 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #8B2050, #FF1493) !important;
    color: white !important; border: 1px solid #FF69B4 !important;
    border-radius: 8px !important; font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important; padding: 10px 26px !important;
    box-shadow: 0 0 12px rgba(255,20,147,.35) !important;
    transition: all .2s !important; text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.stButton > button:hover {
    box-shadow: 0 0 22px rgba(255,20,147,.65) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: #2D1224 !important; color: #F8D7E8 !important;
    border: 1px solid #8B2050 !important; border-radius: 8px !important;
    font-family: 'Nunito', sans-serif !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #FF1493 !important;
    box-shadow: 0 0 8px rgba(255,20,147,.4) !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: #2D1224 !important; border-color: #8B2050 !important;
    color: #F8D7E8 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #2D1224 !important; border-radius: 10px !important;
    border: 1px solid #8B2050 !important;
    box-shadow: 0 0 10px rgba(255,20,147,.1) !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: #C2547A !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: #FF69B4 !important; font-weight: 800 !important; }

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #8B2050, #FF1493) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: #3D1E34 !important; border-radius: 99px !important;
}

/* ── Alerts ── */
.stSuccess { background: #0A2A10 !important; border-left: 3px solid #4CAF50 !important; border-radius: 8px !important; color: #A5D6A7 !important; }
.stError   { background: #2A0A10 !important; border-left: 3px solid #E91E63 !important; border-radius: 8px !important; color: #F48FB1 !important; }
.stWarning { background: #2A1A00 !important; border-left: 3px solid #FFC107 !important; border-radius: 8px !important; color: #FFE082 !important; }
.stInfo    { background: #0A1A3A !important; border-left: 3px solid #2196F3 !important; border-radius: 8px !important; color: #90CAF9 !important; }

/* ── Divider ── */
hr { border-color: #8B2050 !important; opacity: .4 !important; }

/* ── Shared card ── */
.tp-card {
    background: #2D1224; border-radius: 12px; padding: 18px 22px;
    border: 1px solid #8B2050; box-shadow: 0 0 18px rgba(255,20,147,.12);
    margin-bottom: 12px;
}
.tp-chip {
    display: inline-block; border-radius: 6px; padding: 3px 12px;
    font-size: 12px; font-weight: 700; margin: 2px;
}
.tp-chip-low  { background: #0A1A3A; color: #90CAF9; border: 1px solid #2196F3; }
.tp-chip-high { background: #2A0A10; color: #F48FB1; border: 1px solid #E91E63; }
.tp-chip-win  { background: #0A2A10; color: #A5D6A7; border: 1px solid #4CAF50; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1A0A12; }
::-webkit-scrollbar-thumb { background: #8B2050; border-radius: 3px; }
</style>
"""

def init(keys: dict):
    """Initialise session-state keys only if they are not already set."""
    import streamlit as st
    for k, v in keys.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_game(prefix: str):
    """Delete all session-state keys that start with *prefix*."""
    import streamlit as st
    to_del = [k for k in st.session_state.keys() if k.startswith(prefix)]
    for k in to_del:
        del st.session_state[k]


def dice_svg(val: int, size: int = 60) -> str:
    """Return an SVG die face with dark theme dots."""
    dots = {
        1: '<circle cx="25" cy="25" r="5" fill="#FF1493"/>',
        2: '<circle cx="13" cy="13" r="4" fill="#FF69B4"/><circle cx="37" cy="37" r="4" fill="#FF69B4"/>',
        3: '<circle cx="13" cy="13" r="4" fill="#FF69B4"/><circle cx="25" cy="25" r="4" fill="#FF69B4"/><circle cx="37" cy="37" r="4" fill="#FF69B4"/>',
        4: '<circle cx="13" cy="13" r="4" fill="#FF1493"/><circle cx="37" cy="13" r="4" fill="#FF1493"/><circle cx="13" cy="37" r="4" fill="#FF1493"/><circle cx="37" cy="37" r="4" fill="#FF1493"/>',
        5: '<circle cx="13" cy="13" r="4" fill="#FF1493"/><circle cx="37" cy="13" r="4" fill="#FF1493"/><circle cx="25" cy="25" r="4" fill="#FF1493"/><circle cx="13" cy="37" r="4" fill="#FF1493"/><circle cx="37" cy="37" r="4" fill="#FF1493"/>',
        6: '<circle cx="13" cy="10" r="4" fill="#FF1493"/><circle cx="37" cy="10" r="4" fill="#FF1493"/><circle cx="13" cy="25" r="4" fill="#FF1493"/><circle cx="37" cy="25" r="4" fill="#FF1493"/><circle cx="13" cy="40" r="4" fill="#FF1493"/><circle cx="37" cy="40" r="4" fill="#FF1493"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="50" height="50" rx="10" fill="#2D1224" stroke="#FF1493" stroke-width="2"/>'
            + dots.get(val, "") + '</svg>')
