# -*- coding: utf-8 -*-
"""games/lottery.py — TP Games: Lucky Number Lottery"""
import random
import streamlit as st
from theme import init, reset_game, dice_svg, PINK, PINK2, CARD, BORDER, TEXT, TEXT2, GREEN, RED

def run():
    init({"lot_secret":0,"lot_tries":0,"lot_max_tries":5,"lot_max_num":50,
          "lot_done":False,"lot_history":[],"lot_wins":0,"lot_losses":0,
          "lot_started":False,"lot_streak":0,"lot_best":0})
    s = st.session_state

    st.markdown("## 🎰 Lucky Number Lottery")
    st.caption("Guess the secret number hiding in the vault!")

    col_d, col_r = st.columns([3,1])
    with col_d:
        diff = st.selectbox("Difficulty", [
            "Easy   — 1 to 30, 7 tries",
            "Medium — 1 to 50, 5 tries",
            "Hard   — 1 to 99, 4 tries",
        ], key="lot_diff")
    with col_r:
        if st.button("Reset Stats", key="lot_rst"):
            reset_game("lot_"); st.rerun()

    cfg = {
        "Easy   — 1 to 30, 7 tries":  (30, 7),
        "Medium — 1 to 50, 5 tries":  (50, 5),
        "Hard   — 1 to 99, 4 tries":  (99, 4),
    }
    max_num, max_tries = cfg[diff]

    if st.button("New Game", key="lot_new"):
        s.lot_secret    = random.randint(1, max_num)
        s.lot_tries     = 0
        s.lot_max_tries = max_tries
        s.lot_max_num   = max_num
        s.lot_done      = False
        s.lot_history   = []
        s.lot_started   = True
        st.rerun()

    if not s.lot_started:
        st.info("Press **New Game** to start!"); return

    rem = s.lot_max_tries - s.lot_tries
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Guesses",     s.lot_tries)
    c2.metric("Remaining",   rem)
    c3.metric("Wins",        s.lot_wins)
    c4.metric("Best Streak", s.lot_best)
    st.progress(max(0., rem / s.lot_max_tries))

    # Ball row
    balls = ""
    for i in range(s.lot_max_tries):
        if i < len(s.lot_history):
            g, k = s.lot_history[i]
            bg  = "#0A2A10" if k=="win" else "#2A0A10"
            bdr = "#4CAF50" if k=="win" else "#E91E63"
            clr = "#A5D6A7" if k=="win" else "#F48FB1"
            balls += (f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                      f'width:42px;height:42px;border-radius:50%;background:{bg};'
                      f'border:2px solid {bdr};font-weight:700;color:{clr};margin:3px;font-size:13px">{g}</span>')
        else:
            balls += ('<span style="display:inline-flex;align-items:center;justify-content:center;'
                      'width:42px;height:42px;border-radius:50%;background:#2D1224;'
                      'border:2px solid #8B2050;color:#8B3060;margin:3px;font-size:13px">?</span>')
    st.markdown(f'<div style="text-align:center;margin:12px 0">{balls}</div>', unsafe_allow_html=True)

    # History chips
    if s.lot_history:
        parts = []
        for g, k in s.lot_history:
            cls    = "win" if k=="win" else ("low" if k=="low" else "high")
            symbol = "OK" if k=="win" else ("UP" if k=="low" else "DN")
            parts.append(f'<span class="tp-chip tp-chip-{cls}">{symbol} {g}</span>')
        st.markdown('<div style="margin:8px 0">' + "".join(parts) + '</div>', unsafe_allow_html=True)

    if not s.lot_done:
        guess = st.number_input(f"Enter a number between 1 and {s.lot_max_num}",
                                1, s.lot_max_num, step=1, key="lot_inp")
        if st.button("Submit Guess", key="lot_sub"):
            g = int(guess); s.lot_tries += 1
            if g == s.lot_secret:
                s.lot_history.append((g, "win"))
                s.lot_wins   += 1
                s.lot_streak += 1
                s.lot_best    = max(s.lot_best, s.lot_streak)
                s.lot_done    = True
                st.success(f"Correct! {s.lot_secret} was the number! Won in {s.lot_tries} tries!")
            elif s.lot_tries >= s.lot_max_tries:
                s.lot_history.append((g, "high" if g > s.lot_secret else "low"))
                s.lot_losses += 1; s.lot_streak = 0; s.lot_done = True
                st.error(f"Out of tries! The number was {s.lot_secret}.")
            else:
                d = abs(g - s.lot_secret); r = s.lot_max_num
                direction = "higher" if g < s.lot_secret else "lower"
                k = "low" if g < s.lot_secret else "high"
                s.lot_history.append((g, k))
                if d <= r*.05:   hint = f"Burning hot! Just a tiny bit **{direction}**!"
                elif d <= r*.15: hint = f"Warm! Go a bit **{direction}**."
                else:            hint = f"Cold! Go much **{direction}**. ({rem-1} tries left)"
                st.info(hint)
            st.rerun()
    else:
        if st.button("Play Again", key="lot_again"):
            s.lot_secret    = random.randint(1, max_num)
            s.lot_tries     = 0
            s.lot_max_tries = max_tries
            s.lot_max_num   = max_num
            s.lot_done      = False
            s.lot_history   = []
            st.rerun()
