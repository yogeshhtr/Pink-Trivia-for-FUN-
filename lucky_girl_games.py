# -*- coding: utf-8 -*-
"""
app.py — TP Games
Main Streamlit entry point. Run with:  streamlit run app.py
"""
import os
import sys
import streamlit as st

# Make sure sibling modules resolve correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from theme import GLOBAL_CSS, reset_game, init

st.set_page_config(
    page_title="TP Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Game registry ─────────────────────────────────────────────────────────
GAMES = {
    "🎰  Lottery Guess": "lottery",
    "🌸  Pink Trivia":   "trivia",
    "🪢  Hangman":       "hangman",
    "🎲  Dice Duel":     "dice_duel",
    "🐍  Snake":         "snake",
    "🎯  Ludo":          "ludo",
}

# Prefix used by each game for its session-state keys
GAME_PREFIXES = {
    "lottery":  "lot_",
    "trivia":   "tv_",
    "hangman":  "hg_",
    "dice_duel":"dd_",
    "snake":    "",      # no server-side state
    "ludo":     "ld_",
}

TIPS = {
    "lottery":   "Guess the hidden number!\nHot/cold hints & win streaks.",
    "trivia":    "No question repeats until all used.\nFilter by category.",
    "hangman":   "Guess letters before 6 wrong.\nChoose a word category.",
    "dice_duel": "2-4 players, human or CPU.\nHighest roll wins the round.",
    "snake":     "Arrow keys or WASD.\nEat food, avoid the walls!",
    "ludo":      "2-4 players, human or CPU.\nRoll 6 to release pieces.",
}

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / title
    st.markdown(
        '<h1 style="font-family:Orbitron,sans-serif;font-size:22px;color:#FF1493;'
        'text-align:center;text-shadow:0 0 16px rgba(255,20,147,.6);margin:0">🎮 TP Games</h1>',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;color:#8B3060;font-size:12px;margin-top:4px">by Y</p>',
        unsafe_allow_html=True)
    st.markdown("---")

    game_label = st.radio(
        "SELECT GAME",
        list(GAMES.keys()),
        key="game_sel",
        label_visibility="visible",
    )
    game_key = GAMES[game_label]

    st.markdown("---")
    st.markdown(
        f'<p style="color:#C2547A;font-size:12px;line-height:1.6">'
        f'{TIPS.get(game_key,"").replace(chr(10),"<br>")}</p>',
        unsafe_allow_html=True)

    st.markdown("---")

    # Reset current game
    if st.button("Reset Current Game", key="sidebar_reset"):
        prefix = GAME_PREFIXES.get(game_key, "")
        if prefix:
            reset_game(prefix)
        st.rerun()

    # Reset ALL games
    if st.button("Reset ALL Games", key="sidebar_reset_all"):
        for pfx in GAME_PREFIXES.values():
            if pfx:
                reset_game(pfx)
        st.rerun()

    st.markdown("---")
    st.markdown('<p style="color:#3A1830;font-size:11px;text-align:center">TP Games v2.0</p>',
                unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown(
    '<h1 style="font-family:Orbitron,sans-serif;font-size:32px;'
    'text-shadow:0 0 24px rgba(255,20,147,.5)">🎮 TP Games</h1>',
    unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#8B3060;font-size:13px;margin-top:-8px;margin-bottom:16px">'
    'Your personal game hub</p>',
    unsafe_allow_html=True)
st.divider()

# ── Route to game ─────────────────────────────────────────────────────────
if game_key == "lottery":
    import lottery
    lottery.run()

elif game_key == "trivia":
    import trivia
    trivia.run(BASE_DIR)

elif game_key == "hangman":
    import hangman
    hangman.run()

elif game_key == "dice_duel":
    import dice_duel
    dice_duel.run()

elif game_key == "snake":
    import snake
    snake.run()

elif game_key == "ludo":
    import ludo
    ludo.run()
