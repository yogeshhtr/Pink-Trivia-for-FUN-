# -*- coding: utf-8 -*-
"""games/hangman.py — TP Games: Hangman"""
import random
import streamlit as st
from theme import init, reset_game

HANG_WORDS = [
    ("BUTTERFLY","Nature"),("BLOSSOM","Nature"),("RAINBOW","Nature"),
    ("LAVENDER","Nature"),("MAGNOLIA","Nature"),("JASMINE","Nature"),
    ("PRINCESS","Royalty"),("TIARA","Royalty"),("CROWN","Royalty"),
    ("DIAMOND","Gems"),("SAPPHIRE","Gems"),("AMETHYST","Gems"),("CRYSTAL","Gems"),
    ("GLITTER","Fashion"),("SPARKLE","Fashion"),("RIBBON","Fashion"),
    ("VELVET","Fashion"),("STILETTO","Fashion"),("HAIRPIN","Fashion"),
    ("LIPSTICK","Beauty"),("MASCARA","Beauty"),("PERFUME","Beauty"),
    ("EYELINER","Beauty"),("BLUSH","Beauty"),
    ("BRACELET","Jewelry"),("NECKLACE","Jewelry"),("EARRINGS","Jewelry"),
    ("CUPCAKE","Food"),("MACARON","Food"),("STRAWBERRY","Food"),
    ("CHEESECAKE","Food"),("LEMONADE","Food"),
    ("UNICORN","Fantasy"),("ENCHANTED","Fantasy"),("FANTASY","Fantasy"),
    ("ELEGANCE","Words"),("ROMANCE","Words"),("GORGEOUS","Words"),("RADIANCE","Words"),
]

def _svg(wrong: int) -> str:
    parts = [
        '<circle cx="200" cy="90" r="28" stroke="#FF1493" stroke-width="3" fill="#2A0A18"/>',
        '<line x1="200" y1="118" x2="200" y2="205" stroke="#FF69B4" stroke-width="3"/>',
        '<line x1="200" y1="145" x2="158" y2="175" stroke="#FF69B4" stroke-width="3"/>',
        '<line x1="200" y1="145" x2="242" y2="175" stroke="#FF69B4" stroke-width="3"/>',
        '<line x1="200" y1="205" x2="162" y2="248" stroke="#FF69B4" stroke-width="3"/>',
        '<line x1="200" y1="205" x2="238" y2="248" stroke="#FF69B4" stroke-width="3"/>',
    ]
    body = "".join(parts[:wrong])
    eyes = ""
    if wrong >= 6:
        eyes = ('<text x="192" y="96" font-size="14" fill="#FF1493">X</text>'
                '<text x="204" y="96" font-size="14" fill="#FF1493">X</text>')
    elif wrong >= 1:
        eyes = ('<circle cx="192" cy="88" r="4" fill="#FF1493"/>'
                '<circle cx="208" cy="88" r="4" fill="#FF1493"/>')
    return (
        '<svg width="320" height="290" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="320" height="290" fill="#1A0A12" rx="14"/>'
        '<line x1="50" y1="268" x2="270" y2="268" stroke="#8B2050" stroke-width="4"/>'
        '<line x1="110" y1="268" x2="110" y2="28" stroke="#8B2050" stroke-width="4"/>'
        '<line x1="110" y1="28" x2="200" y2="28" stroke="#8B2050" stroke-width="4"/>'
        '<line x1="200" y1="28" x2="200" y2="62" stroke="#8B2050" stroke-width="4"/>'
        + body + eyes + '</svg>'
    )

def run():
    init({"hg_word":"","hg_category":"","hg_guessed":[],"hg_wrong":0,
          "hg_done":False,"hg_won":False,"hg_started":False,
          "hg_wins":0,"hg_losses":0,"hg_streak":0})
    s = st.session_state

    st.markdown("## 🪢 Hangman")
    st.caption("Guess the hidden word letter by letter before it's too late!")

    col_cat, col_rst = st.columns([3,1])
    with col_cat:
        cats = ["All"] + sorted(set(c for _,c in HANG_WORDS))
        hcat = st.selectbox("Word category", cats, key="hg_cat")
    with col_rst:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Stats", key="hg_rst"):
            reset_game("hg_"); st.rerun()

    c1,c2,c3 = st.columns(3)
    c1.metric("Wins", s.hg_wins)
    c2.metric("Losses", s.hg_losses)
    c3.metric("Streak", s.hg_streak)

    def new_game():
        pool = [(w,c) for w,c in HANG_WORDS if hcat=="All" or c==hcat]
        word, cat = random.choice(pool)
        s.hg_word=word; s.hg_category=cat
        s.hg_guessed=[]; s.hg_wrong=0
        s.hg_done=False; s.hg_won=False; s.hg_started=True

    if st.button("New Game", key="hg_new") or not s.hg_started:
        new_game(); st.rerun()

    if not s.hg_started: return

    left, right = st.columns([1, 1])

    with left:
        st.markdown(_svg(s.hg_wrong), unsafe_allow_html=True)
        # Lives bar
        filled = 6 - s.hg_wrong
        bar    = "♥ " * filled + "♡ " * s.hg_wrong
        color  = "#4CAF50" if filled>3 else ("#FFC107" if filled>1 else "#E91E63")
        st.markdown(
            f'<p style="text-align:center;font-size:18px;color:{color};letter-spacing:2px">{bar}</p>',
            unsafe_allow_html=True)

    with right:
        # Word display
        display = "  ".join("_" if c not in s.hg_guessed else c for c in s.hg_word)
        st.markdown(
            f'<div style="text-align:center;margin:24px 0">'
            f'<div style="font-size:30px;font-weight:800;letter-spacing:10px;color:#FF69B4;'
            f'font-family:Orbitron,sans-serif">{display}</div>'
            f'<div style="color:#8B3060;font-size:12px;margin-top:10px;letter-spacing:2px;text-transform:uppercase">'
            f'Category: {s.hg_category} &nbsp;|&nbsp; {len(s.hg_word)} letters</div>'
            f'</div>', unsafe_allow_html=True)

        wrong_letters   = [l for l in s.hg_guessed if l not in s.hg_word]
        correct_letters = [l for l in s.hg_guessed if l in s.hg_word]
        if wrong_letters:
            wl = " ".join(wrong_letters)
            st.markdown(f'<p style="color:#E91E63;font-size:13px">Wrong: <b>{wl}</b></p>', unsafe_allow_html=True)
        if correct_letters:
            cl = " ".join(correct_letters)
            st.markdown(f'<p style="color:#4CAF50;font-size:13px">Correct: <b>{cl}</b></p>', unsafe_allow_html=True)

        won  = all(c in s.hg_guessed for c in s.hg_word)
        lost = s.hg_wrong >= 6
        if won and not s.hg_done:
            s.hg_done=True; s.hg_won=True; s.hg_wins+=1; s.hg_streak+=1
        if lost and not s.hg_done:
            s.hg_done=True; s.hg_won=False; s.hg_losses+=1; s.hg_streak=0

        if not s.hg_done:
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for row_str in [alphabet[:13], alphabet[13:]]:
                cols = st.columns(len(row_str))
                for i, letter in enumerate(row_str):
                    with cols[i]:
                        guessed = letter in s.hg_guessed
                        if guessed:
                            col = "#4CAF50" if letter in s.hg_word else "#880E4F"
                            bg  = "#0A2A10" if letter in s.hg_word else "#2A0A10"
                            st.markdown(
                                f'<div style="text-align:center;padding:5px 2px;background:{bg};'
                                f'color:{col};border-radius:6px;font-weight:700;font-size:12px;'
                                f'border:1px solid {col}">{letter}</div>',
                                unsafe_allow_html=True)
                        else:
                            if st.button(letter, key=f"hg_{letter}"):
                                s.hg_guessed.append(letter)
                                if letter not in s.hg_word: s.hg_wrong += 1
                                st.rerun()
        else:
            if s.hg_won:
                st.success(f"You got it! The word was **{s.hg_word}**!")
            else:
                st.error(f"Game over! The word was **{s.hg_word}**.")
            if st.button("Play Again", key="hg_again"):
                new_game(); st.rerun()
