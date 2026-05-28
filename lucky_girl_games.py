# -*- coding: utf-8 -*-
import streamlit as st
import random
import json
import os
import math

st.set_page_config(page_title="TP Girl Games", page_icon="🌸",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,500&family=Nunito:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Nunito',sans-serif;background-color:#FFF0F5!important;}
.stApp{background:linear-gradient(135deg,#FFF0F5 0%,#FFE4EF 100%)!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#FF69B4 0%,#C2185B 100%)!important;}
[data-testid="stSidebar"] *{color:white!important;}
[data-testid="stSidebar"] .stRadio label{font-size:15px;font-weight:700;}
h1{font-family:'Playfair Display',serif!important;color:#FF1493!important;text-align:center;}
h2,h3{font-family:'Playfair Display',serif!important;color:#C2547A!important;}
.stButton>button{background:linear-gradient(135deg,#FF69B4,#FF1493)!important;color:white!important;
  border:none!important;border-radius:25px!important;font-family:'Nunito',sans-serif!important;
  font-weight:700!important;padding:10px 26px!important;
  box-shadow:0 4px 12px rgba(255,105,180,.4)!important;transition:all .2s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(255,20,147,.5)!important;}
.stNumberInput input,.stTextInput input{border:2px solid #FFB6C1!important;border-radius:15px!important;
  background:white!important;color:#8B1A4A!important;font-family:'Nunito',sans-serif!important;
  font-size:18px!important;font-weight:700!important;text-align:center!important;}
[data-testid="stMetric"]{background:white!important;border-radius:16px!important;
  padding:12px 16px!important;border:1.5px solid #FFB6C1!important;
  box-shadow:0 2px 10px rgba(255,105,180,.15)!important;}
[data-testid="stMetricLabel"]{color:#C2547A!important;font-size:12px!important;}
[data-testid="stMetricValue"]{color:#FF1493!important;font-weight:700!important;}
.stProgress>div>div{background:linear-gradient(90deg,#FFB6C1,#FF1493)!important;border-radius:99px!important;}
.pink-card{background:white;border-radius:20px;padding:20px 24px;
  border:1.5px solid #FFB6C1;box-shadow:0 4px 18px rgba(255,105,180,.12);margin-bottom:14px;}
.chip{display:inline-block;border-radius:99px;padding:4px 14px;font-size:13px;font-weight:700;margin:3px;}
.chip-low{background:#E3F2FD;color:#1565C0;border:1px solid #90CAF9;}
.chip-high{background:#FCE4EC;color:#C62828;border:1px solid #F48FB1;}
.chip-win{background:#E8F5E9;color:#2E7D32;border:1px solid #A5D6A7;}
</style>
""", unsafe_allow_html=True)

def init(keys):
    for k, v in keys.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ============================================================
# GAME 1 — Lottery Guess
# ============================================================
def game_lottery():
    init({"lot_secret":0,"lot_tries":0,"lot_max_tries":5,"lot_max_num":50,
          "lot_done":False,"lot_history":[],"lot_wins":0,"lot_losses":0,
          "lot_started":False,"lot_streak":0,"lot_best":0})
    s = st.session_state
    st.markdown("## 🎰 TP Number Lottery")
    st.caption("Guess the secret number hiding in our pink vault! 💗")

    diff = st.selectbox("Difficulty",
        ["🌸 Easy (1-30, 7 tries)","💗 Medium (1-50, 5 tries)","💀 Hard (1-99, 4 tries)"],
        key="lot_diff")
    cfg = {"🌸 Easy (1-30, 7 tries)":(30,7),
           "💗 Medium (1-50, 5 tries)":(50,5),
           "💀 Hard (1-99, 4 tries)":(99,4)}
    max_num, max_tries = cfg[diff]

    if st.button("🌸 New Game", key="lot_new"):
        s.lot_secret=random.randint(1,max_num); s.lot_tries=0
        s.lot_max_tries=max_tries; s.lot_max_num=max_num
        s.lot_done=False; s.lot_history=[]; s.lot_started=True
        st.rerun()

    if not s.lot_started:
        st.info("Press **New Game** to start!"); return

    rem = s.lot_max_tries - s.lot_tries
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Guesses", s.lot_tries)
    c2.metric("Remaining", rem)
    c3.metric("Wins", s.lot_wins)
    c4.metric("Best Streak", s.lot_best)
    st.progress(max(0., rem/s.lot_max_tries))

    # Ball display
    balls = ""
    for i in range(s.lot_max_tries):
        if i < len(s.lot_history):
            g, k = s.lot_history[i]
            bg  = "#E8F5E9" if k=="win" else "#FFE4EF"
            bdr = "#4CAF50" if k=="win" else "#FF69B4"
            clr = "#2E7D32" if k=="win" else "#8B1A4A"
            balls += ('<span style="display:inline-flex;align-items:center;justify-content:center;'
                      'width:40px;height:40px;border-radius:50%;background:' + bg + ';'
                      'border:2px solid ' + bdr + ';font-weight:700;color:' + clr + ';'
                      'margin:3px;font-size:13px">' + str(g) + '</span>')
        else:
            balls += ('<span style="display:inline-flex;align-items:center;justify-content:center;'
                      'width:40px;height:40px;border-radius:50%;background:#FFF0F5;'
                      'border:2px solid #FFB6C1;color:#F48FB1;margin:3px;font-size:13px">?</span>')
    st.markdown('<div style="text-align:center;margin:10px 0">' + balls + '</div>', unsafe_allow_html=True)

    if s.lot_history:
        parts = []
        for g, k in s.lot_history:
            cls    = "win" if k=="win" else ("low" if k=="low" else "high")
            symbol = "V" if k=="win" else ("^" if k=="low" else "v")
            parts.append('<span class="chip chip-' + cls + '">' + symbol + ' ' + str(g) + '</span>')
        st.markdown('<div style="margin:6px 0">' + "".join(parts) + '</div>', unsafe_allow_html=True)

    if not s.lot_done:
        guess = st.number_input(f"Number (1-{s.lot_max_num})", 1, s.lot_max_num, step=1, key="lot_inp")
        if st.button("💌 Submit Guess", key="lot_sub"):
            g = int(guess); s.lot_tries += 1
            if g == s.lot_secret:
                s.lot_history.append((g,"win")); s.lot_wins += 1
                s.lot_streak += 1; s.lot_best = max(s.lot_best, s.lot_streak)
                s.lot_done = True
                st.success(f"🎉 YAAAS! {s.lot_secret} was right! Won in {s.lot_tries} tries! 🏆")
            elif s.lot_tries >= s.lot_max_tries:
                s.lot_history.append((g, "high" if g>s.lot_secret else "low"))
                s.lot_losses += 1; s.lot_streak = 0; s.lot_done = True
                st.error(f"💔 No more tries! The number was {s.lot_secret}. Try again!")
            else:
                d = abs(g - s.lot_secret); r = s.lot_max_num
                direction = "higher" if g < s.lot_secret else "lower"
                k = "low" if g < s.lot_secret else "high"
                s.lot_history.append((g, k))
                if d <= r*.05:   hint = f"🔥 So close! Go just a bit **{direction}**!"
                elif d <= r*.15: hint = f"💗 Getting warmer! A bit **{direction}**~"
                else:            hint = f"🧊 Way off! Go **{direction}**, babe! ({rem-1} tries left)"
                st.info(hint)
            st.rerun()
    else:
        if st.button("💖 Play Again", key="lot_again"):
            s.lot_secret=random.randint(1,max_num); s.lot_tries=0
            s.lot_max_tries=max_tries; s.lot_max_num=max_num
            s.lot_done=False; s.lot_history=[]; st.rerun()

# ============================================================
# GAME 2 — Pink Trivia (JSON-driven, visual card UI)
# ============================================================
def load_questions():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trivia_questions.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []

TRIVIA_CSS = """
<style>
.tv-header{background:linear-gradient(135deg,#FF69B4,#C2185B);border-radius:20px;
  padding:18px 24px;color:white;text-align:center;margin-bottom:16px;}
.tv-header h2{color:white!important;margin:0;font-size:22px;}
.tv-header p{margin:4px 0 0 0;opacity:.85;font-size:13px;}
.tv-qcard{background:white;border-radius:20px;padding:24px 28px;
  border:2px solid #FFB6C1;box-shadow:0 6px 24px rgba(255,105,180,.18);
  margin:16px 0;text-align:center;}
.tv-qnum{font-size:12px;color:#F48FB1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.tv-cat{display:inline-block;background:#FFE4EF;color:#C2185B;border-radius:99px;
  padding:3px 14px;font-size:12px;font-weight:700;margin-bottom:14px;}
.tv-question{font-size:20px;font-weight:700;color:#8B1A4A;line-height:1.4;}
.tv-opts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;}
.tv-opt{background:#FFF0F5;border:2px solid #FFB6C1;border-radius:14px;
  padding:14px 16px;cursor:pointer;font-size:15px;font-weight:600;color:#8B1A4A;
  transition:all .2s;text-align:center;}
.tv-opt:hover{background:#FFE4EF;border-color:#FF69B4;transform:translateY(-2px);}
.tv-opt.correct{background:#E8F5E9;border-color:#4CAF50;color:#1B5E20;}
.tv-opt.wrong{background:#FCE4EC;border-color:#E91E63;color:#880E4F;}
.tv-opt.neutral{background:#F5F5F5;border-color:#ddd;color:#999;}
.tv-streak{background:linear-gradient(135deg,#FF8C00,#FF4500);color:white;
  border-radius:12px;padding:8px 16px;font-weight:700;display:inline-block;margin-bottom:8px;}
.tv-progress-bar{height:8px;background:#FFE4EF;border-radius:99px;overflow:hidden;margin:12px 0;}
.tv-progress-fill{height:8px;background:linear-gradient(90deg,#FFB6C1,#FF1493);border-radius:99px;transition:width .4s;}
.tv-score-badge{background:linear-gradient(135deg,#FF69B4,#FF1493);color:white;
  border-radius:99px;padding:6px 20px;font-weight:700;font-size:15px;display:inline-block;}
.tv-result{background:white;border-radius:24px;padding:32px;text-align:center;
  border:2px solid #FFB6C1;box-shadow:0 8px 32px rgba(255,105,180,.2);}
.tv-result-grade{font-size:48px;font-weight:800;color:#FF1493;margin-bottom:8px;}
.tv-result-msg{font-size:16px;color:#C2547A;margin-bottom:16px;}
.tv-result-score{font-size:52px;font-weight:900;color:#FF1493;}
.tv-result-pct{font-size:14px;color:#F48FB1;margin-top:4px;}
.tv-stat-row{display:flex;justify-content:center;gap:24px;margin:16px 0;}
.tv-stat{background:#FFF0F5;border-radius:14px;padding:12px 20px;text-align:center;border:1px solid #FFB6C1;}
.tv-stat-val{font-size:24px;font-weight:800;color:#FF1493;}
.tv-stat-lbl{font-size:11px;color:#F48FB1;font-weight:600;text-transform:uppercase;letter-spacing:1px;}
</style>
"""

def game_trivia():
    init({"tv_used":[],"tv_questions":[],"tv_idx":0,
          "tv_score":0,"tv_answered":False,"tv_selected":"",
          "tv_done":False,"tv_started":False,"tv_streak":0,
          "tv_correct":0,"tv_total_played":0})
    s = st.session_state
    all_q = load_questions()

    st.markdown(TRIVIA_CSS, unsafe_allow_html=True)

    if not all_q:
        st.error("trivia_questions.json not found next to the script! Place both files in the same folder.")
        return

    cats = ["All"] + sorted(set(q["category"] for q in all_q))
    col1, col2 = st.columns([2,1])
    with col1:
        cat = st.selectbox("Category filter", cats, key="tv_cat")
    with col2:
        n_q = st.selectbox("Questions per round", [5,8,10,15], index=1, key="tv_nq")

    pool = [q for q in all_q if cat=="All" or q["category"]==cat]

    st.markdown("""<div class="tv-header">
        <h2>🌸 Pink Trivia Quiz</h2>
        <p>No question repeats until all are used — how well do you know your stuff? 💅</p>
    </div>""", unsafe_allow_html=True)

    if st.button("🌸 Start New Quiz", key="tv_new") or not s.tv_started:
        if not pool:
            st.warning("No questions in this category!"); return
        avail = [q for q in pool if q not in s.tv_used]
        if len(avail) < n_q:
            s.tv_used = []; avail = pool[:]
        selected = random.sample(avail, min(n_q, len(avail)))
        s.tv_used += selected
        s.tv_questions = selected
        s.tv_idx=0; s.tv_score=0; s.tv_answered=False
        s.tv_selected=""; s.tv_done=False; s.tv_started=True; s.tv_streak=0
        st.rerun()

    if not s.tv_started: return
    total = len(s.tv_questions)

    if s.tv_done:
        pct = int(s.tv_score/total*100)
        if pct>=80:   grade,msg = "Quiz Queen! 👑","You absolutely aced it! Bow down!"
        elif pct>=60: grade,msg = "Pretty Smart! 💅","Great job! A few more and you will be queen!"
        elif pct>=40: grade,msg = "Getting There! 💗","Not bad! Keep practicing!"
        else:         grade,msg = "Keep Studying! 📚","Try again — you will slay it next time!"

        st.markdown("""
        <div class="tv-result">
          <div class="tv-result-grade">""" + grade + """</div>
          <div class="tv-result-msg">""" + msg + """</div>
          <div class="tv-result-score">""" + str(s.tv_score) + "/" + str(total) + """</div>
          <div class="tv-result-pct">""" + str(pct) + """% correct</div>
          <div class="tv-stat-row">
            <div class="tv-stat"><div class="tv-stat-val">""" + str(s.tv_score) + """</div><div class="tv-stat-lbl">Correct</div></div>
            <div class="tv-stat"><div class="tv-stat-val">""" + str(total-s.tv_score) + """</div><div class="tv-stat-lbl">Wrong</div></div>
            <div class="tv-stat"><div class="tv-stat-val">""" + str(s.tv_streak) + """</div><div class="tv-stat-lbl">Best Streak</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💖 Play Again", key="tv_again"):
            s.tv_started=False; st.rerun()
        return

    q     = s.tv_questions[s.tv_idx]
    prog  = s.tv_idx / total
    pfill = int(prog * 100)

    # Progress
    st.markdown(
        '<div class="tv-progress-bar"><div class="tv-progress-fill" style="width:' + str(pfill) + '%"></div></div>',
        unsafe_allow_html=True)

    top_left, top_right = st.columns([3,1])
    with top_left:
        st.markdown('<span class="tv-score-badge">Score: ' + str(s.tv_score) + ' / ' + str(total) + '</span>', unsafe_allow_html=True)
    with top_right:
        if s.tv_streak >= 3:
            st.markdown('<span class="tv-streak">🔥 ' + str(s.tv_streak) + ' streak!</span>', unsafe_allow_html=True)

    # Question card
    st.markdown("""
    <div class="tv-qcard">
      <div class="tv-qnum">Question """ + str(s.tv_idx+1) + " of " + str(total) + """</div>
      <div class="tv-cat">""" + q["category"] + """</div>
      <div class="tv-question">""" + q["question"] + """</div>
    </div>""", unsafe_allow_html=True)

    # Options — 2 columns
    opts = q["options"]
    col_a, col_b = st.columns(2)
    pairs = [(opts[0], opts[1]), (opts[2] if len(opts)>2 else None, opts[3] if len(opts)>3 else None)]

    for pair, col in zip(pairs, [col_a, col_b]):
        pass  # rendered below via buttons

    # Render all 4 option buttons in a 2x2 grid
    row1 = st.columns(2)
    row2 = st.columns(2)
    all_cols = [row1[0], row1[1], row2[0], row2[1]]

    for i, opt in enumerate(opts):
        with all_cols[i]:
            if s.tv_answered:
                if opt == q["answer"]:
                    st.success("✅  " + opt)
                elif opt == s.tv_selected:
                    st.error("❌  " + opt)
                else:
                    st.markdown(
                        '<div style="background:#F5F5F5;border:1.5px solid #ddd;border-radius:14px;'
                        'padding:12px;text-align:center;color:#999;font-size:15px;">' + opt + '</div>',
                        unsafe_allow_html=True)
            else:
                if st.button(opt, key="tv_" + str(s.tv_idx) + "_" + str(i), use_container_width=True):
                    s.tv_selected = opt
                    s.tv_answered = True
                    if opt == q["answer"]:
                        s.tv_score += 1; s.tv_streak += 1
                    else:
                        s.tv_streak = 0
                    st.rerun()

    if s.tv_answered:
        st.markdown("<br>", unsafe_allow_html=True)
        if s.tv_selected == q["answer"]:
            st.success("🎉 Correct!  +" + ("2 points (streak bonus!)" if s.tv_streak >= 3 else "1 point"))
        else:
            st.error("💔 The answer was: **" + q["answer"] + "**")
        if st.button("Next Question ➡️", key="tv_next"):
            s.tv_idx += 1; s.tv_answered=False; s.tv_selected=""
            if s.tv_idx >= total: s.tv_done=True
            st.rerun()

# ============================================================
# GAME 3 — Hangman
# ============================================================
HANG_WORDS = [
    ("BUTTERFLY","nature"),("PRINCESS","royalty"),("DIAMOND","gems"),
    ("GLITTER","fashion"),("UNICORN","fantasy"),("BLOSSOM","nature"),
    ("SPARKLE","fashion"),("RAINBOW","nature"),("TIARA","royalty"),
    ("VELVET","fabric"),("CRYSTAL","gems"),("RIBBON","fashion"),
    ("PERFUME","beauty"),("LIPSTICK","beauty"),("MASCARA","beauty"),
    ("EYELINER","beauty"),("BRACELET","jewelry"),("NECKLACE","jewelry"),
    ("EARRINGS","jewelry"),("SAPPHIRE","gems"),("AMETHYST","gems"),
    ("LAVENDER","nature"),("MAGNOLIA","nature"),("JASMINE","nature"),
    ("CUPCAKE","food"),("MACARON","food"),("STRAWBERRY","food"),
    ("CHEESECAKE","food"),("FANTASY","misc"),("ELEGANCE","misc"),
    ("ROMANCE","misc"),("ENCHANTED","misc"),("GORGEOUS","misc"),
]

def hangman_svg(wrong):
    parts = [
        '<circle cx="200" cy="90" r="25" stroke="#FF1493" stroke-width="3" fill="#FFE4EF"/>',
        '<line x1="200" y1="115" x2="200" y2="200" stroke="#FF1493" stroke-width="3"/>',
        '<line x1="200" y1="140" x2="160" y2="170" stroke="#FF1493" stroke-width="3"/>',
        '<line x1="200" y1="140" x2="240" y2="170" stroke="#FF1493" stroke-width="3"/>',
        '<line x1="200" y1="200" x2="160" y2="240" stroke="#FF1493" stroke-width="3"/>',
        '<line x1="200" y1="200" x2="240" y2="240" stroke="#FF1493" stroke-width="3"/>',
    ]
    body = "".join(parts[:wrong])
    bow  = '<path d="M188 72 Q200 60 212 72 Q200 84 188 72 Z" fill="#FF69B4" opacity="0.6"/>' if wrong>0 else ""
    return ('<svg width="300" height="280" xmlns="http://www.w3.org/2000/svg">'
            '<rect width="300" height="280" fill="#FFF0F5" rx="16"/>'
            '<line x1="60" y1="260" x2="260" y2="260" stroke="#C2547A" stroke-width="4"/>'
            '<line x1="120" y1="260" x2="120" y2="30" stroke="#C2547A" stroke-width="4"/>'
            '<line x1="120" y1="30" x2="200" y2="30" stroke="#C2547A" stroke-width="4"/>'
            '<line x1="200" y1="30" x2="200" y2="65" stroke="#C2547A" stroke-width="4"/>'
            + body + bow + '</svg>')

def game_hangman():
    init({"hg_word":"","hg_category":"","hg_guessed":[],"hg_wrong":0,
          "hg_done":False,"hg_won":False,"hg_started":False,
          "hg_wins":0,"hg_losses":0,"hg_streak":0})
    s = st.session_state
    st.markdown("## 🪢 Girly Hangman")
    st.caption("Guess the hidden word letter by letter before she's hanged! 💗")

    cats_hang = ["All"] + sorted(set(c for _,c in HANG_WORDS))
    hcat = st.selectbox("Word category", cats_hang, key="hg_cat")

    c1,c2,c3 = st.columns(3)
    c1.metric("Wins", s.hg_wins); c2.metric("Losses", s.hg_losses); c3.metric("Streak", s.hg_streak)

    def new_hangman():
        pool = [(w,c) for w,c in HANG_WORDS if hcat=="All" or c==hcat]
        word,cat = random.choice(pool)
        s.hg_word=word; s.hg_category=cat
        s.hg_guessed=[]; s.hg_wrong=0
        s.hg_done=False; s.hg_won=False; s.hg_started=True

    if st.button("🌸 New Game", key="hg_new") or not s.hg_started:
        new_hangman(); st.rerun()

    if not s.hg_started: return

    left, right = st.columns([1,1])
    with left:
        st.markdown(hangman_svg(s.hg_wrong), unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#C2547A'>Wrong: " + str(s.hg_wrong) + "/6</p>", unsafe_allow_html=True)

    with right:
        display = " ".join(("_" if c not in s.hg_guessed else c) for c in s.hg_word)
        st.markdown(
            "<div style='text-align:center;margin:20px 0'>"
            "<div style='font-size:32px;font-weight:700;letter-spacing:12px;color:#FF1493;"
            "font-family:Playfair Display,serif'>" + display + "</div>"
            "<div style='color:#C2547A;font-size:13px;margin-top:8px'>Category: " + s.hg_category + "</div>"
            "</div>", unsafe_allow_html=True)

        wrong_letters   = [l for l in s.hg_guessed if l not in s.hg_word]
        correct_letters = [l for l in s.hg_guessed if l in s.hg_word]
        if wrong_letters:
            st.markdown("<p style='color:#E91E63'>Wrong: <b>" + " ".join(wrong_letters) + "</b></p>", unsafe_allow_html=True)
        if correct_letters:
            st.markdown("<p style='color:#4CAF50'>Correct: <b>" + " ".join(correct_letters) + "</b></p>", unsafe_allow_html=True)

        won  = all(c in s.hg_guessed for c in s.hg_word)
        lost = s.hg_wrong >= 6
        if won and not s.hg_done:
            s.hg_done=True; s.hg_won=True; s.hg_wins+=1; s.hg_streak+=1
        if lost and not s.hg_done:
            s.hg_done=True; s.hg_won=False; s.hg_losses+=1; s.hg_streak=0

        if not s.hg_done:
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            rows = [alphabet[:13], alphabet[13:]]
            for row in rows:
                cols = st.columns(len(row))
                for i, letter in enumerate(row):
                    with cols[i]:
                        guessed = letter in s.hg_guessed
                        if guessed:
                            color = "#4CAF50" if letter in s.hg_word else "#E91E63"
                            st.markdown(
                                '<div style="text-align:center;padding:4px;background:' + color + ';'
                                'color:white;border-radius:8px;font-weight:700;font-size:12px">' + letter + '</div>',
                                unsafe_allow_html=True)
                        else:
                            if st.button(letter, key="hg_" + letter):
                                s.hg_guessed.append(letter)
                                if letter not in s.hg_word: s.hg_wrong += 1
                                st.rerun()
        else:
            if s.hg_won:
                st.success("🎉 You got it! The word was **" + s.hg_word + "**! 🌸")
            else:
                st.error("💔 Game over! The word was **" + s.hg_word + "**")
            if st.button("💖 Play Again", key="hg_again"):
                new_hangman(); st.rerun()

# ============================================================
# GAME 4 — Dice Duel Multiplayer
# ============================================================
DICE_FACES = {1:"1",2:"2",3:"3",4:"4",5:"5",6:"6"}
DICE_SVG   = {
    1: '<circle cx="25" cy="25" r="5" fill="#FF1493"/>',
    2: '<circle cx="10" cy="10" r="4" fill="#FF1493"/><circle cx="40" cy="40" r="4" fill="#FF1493"/>',
    3: '<circle cx="10" cy="10" r="4" fill="#FF1493"/><circle cx="25" cy="25" r="4" fill="#FF1493"/><circle cx="40" cy="40" r="4" fill="#FF1493"/>',
    4: '<circle cx="12" cy="12" r="4" fill="#FF1493"/><circle cx="38" cy="12" r="4" fill="#FF1493"/><circle cx="12" cy="38" r="4" fill="#FF1493"/><circle cx="38" cy="38" r="4" fill="#FF1493"/>',
    5: '<circle cx="12" cy="12" r="4" fill="#FF1493"/><circle cx="38" cy="12" r="4" fill="#FF1493"/><circle cx="25" cy="25" r="4" fill="#FF1493"/><circle cx="12" cy="38" r="4" fill="#FF1493"/><circle cx="38" cy="38" r="4" fill="#FF1493"/>',
    6: '<circle cx="12" cy="10" r="4" fill="#FF1493"/><circle cx="38" cy="10" r="4" fill="#FF1493"/><circle cx="12" cy="25" r="4" fill="#FF1493"/><circle cx="38" cy="25" r="4" fill="#FF1493"/><circle cx="12" cy="40" r="4" fill="#FF1493"/><circle cx="38" cy="40" r="4" fill="#FF1493"/>',
}

def dice_svg(val, size=60):
    return ('<svg width="' + str(size) + '" height="' + str(size) + '" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">'
            '<rect width="50" height="50" rx="10" fill="white" stroke="#FFB6C1" stroke-width="2"/>'
            + DICE_SVG.get(val, "") + '</svg>')

def game_dice_duel():
    init({"dd_players":[],"dd_scores":{},"dd_last_roll":{},"dd_round":0,
          "dd_started":False,"dd_target":5,"dd_n_humans":2,"dd_n_cpu":0})
    s = st.session_state
    st.markdown("## 🎲 Dice Duel - Multiplayer")
    st.caption("Roll dice against friends or CPU — first to the target wins! 👑")

    if not s.dd_started:
        col1,col2,col3 = st.columns(3)
        with col1: n_h = st.selectbox("Human players",[1,2,3,4],index=1,key="dd_nh")
        with col2: n_c = st.selectbox("CPU players",  [0,1,2,3],index=0,key="dd_nc")
        with col3: tgt = st.selectbox("Wins to win",  [3,5,7,10],index=1,key="dd_tgt")
        if n_h+n_c < 2: st.warning("Need at least 2 players!"); return
        if n_h+n_c > 4: st.warning("Max 4 players!"); return

        names = []
        for i in range(n_h):
            nm = st.text_input(f"Player {i+1} name", value=f"Player {i+1}", key=f"dd_name_{i}")
            names.append(nm)
        for i in range(n_c):
            names.append("CPU " + str(i+1))

        if st.button("🌸 Start Game", key="dd_start"):
            s.dd_players=names; s.dd_n_humans=n_h; s.dd_n_cpu=n_c
            s.dd_scores={p:0 for p in names}; s.dd_last_roll={}
            s.dd_target=tgt; s.dd_round=0; s.dd_started=True
            st.rerun()
        return

    players = s.dd_players
    winner  = next((p for p,sc in s.dd_scores.items() if sc>=s.dd_target), None)

    if winner:
        st.balloons()
        st.markdown(
            "<div class='pink-card' style='text-align:center'>"
            "<h2 style='color:#FF1493'>👑 " + winner + " WINS THE GAME! 👑</h2>"
            "<p style='color:#C2547A'>What a dice queen! 🌸</p></div>",
            unsafe_allow_html=True)
        if st.button("🔄 Play Again", key="dd_reset"):
            s.dd_started=False; st.rerun()
        return

    # Scoreboard
    cols = st.columns(len(players))
    for i,p in enumerate(players):
        label = ("👑 " if s.dd_scores[p]==max(s.dd_scores.values()) and s.dd_scores[p]>0 else "") + p
        cols[i].metric(label, str(s.dd_scores[p]) + "/" + str(s.dd_target))

    st.markdown("**Round " + str(s.dd_round+1) + "** - Everyone rolls once!")
    st.divider()

    roll_cols = st.columns(len(players))
    for i,p in enumerate(players):
        with roll_cols[i]:
            tag = "🤖" if i>=s.dd_n_humans else "🎀"
            st.markdown("<p style='text-align:center;font-weight:700;color:#C2547A'>" + tag + " " + p + "</p>", unsafe_allow_html=True)
            if p in s.dd_last_roll:
                v = s.dd_last_roll[p]
                st.markdown("<div style='text-align:center'>" + dice_svg(v, 70) + "</div>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center;font-weight:700;font-size:20px;color:#FF1493'>" + str(v) + "</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align:center;font-size:48px'>🎲</p>", unsafe_allow_html=True)

    if st.button("🎲 Roll All Dice!", key="dd_roll_" + str(s.dd_round)):
        rolls = {p: random.randint(1,6) for p in players}
        s.dd_last_roll = rolls
        max_val = max(rolls.values())
        rnd_win = [p for p,v in rolls.items() if v==max_val]
        if len(rnd_win)==1: s.dd_scores[rnd_win[0]] += 1
        s.dd_round += 1
        st.rerun()

    if s.dd_last_roll and s.dd_round > 0:
        max_val = max(s.dd_last_roll.values())
        rnd_win = [p for p,v in s.dd_last_roll.items() if v==max_val]
        if len(rnd_win)==1:
            st.success("🌸 **" + rnd_win[0] + "** wins this round with a " + str(max_val) + "! +1 point")
        else:
            st.info("🤝 Tie between " + ", ".join(rnd_win) + " — no point awarded!")

        st.markdown("**Progress to victory:**")
        for p in players:
            st.caption(p)
            st.progress(min(1., s.dd_scores[p]/s.dd_target))

# ============================================================
# GAME 5 — Snake
# ============================================================
def game_snake():
    st.markdown("## 🐍 Pink Snake Game")
    st.caption("Use arrow keys or WASD to move! Eat the strawberries! 🍓")
    snake_html = """<!DOCTYPE html><html><head><style>
body{margin:0;background:#FFF0F5;display:flex;flex-direction:column;align-items:center;font-family:Nunito,sans-serif;padding:10px;}
canvas{border:3px solid #FF69B4;border-radius:12px;background:#FFF0F5;box-shadow:0 4px 18px rgba(255,105,180,.3);}
#score-bar{display:flex;gap:20px;margin-bottom:10px;font-weight:700;color:#C2547A;font-size:16px;}
.si span{color:#FF1493;font-size:20px;}
#msg{font-size:18px;font-weight:700;color:#FF1493;margin-top:8px;min-height:28px;}
button{background:linear-gradient(135deg,#FF69B4,#FF1493);color:white;border:none;border-radius:25px;
  padding:8px 24px;font-size:15px;font-weight:700;cursor:pointer;margin:6px;}
.hint{font-size:12px;color:#F48FB1;margin-top:4px;}
</style></head><body>
<div id="score-bar">
  <div class="si">Score: <span id="sc">0</span></div>
  <div class="si">Best: <span id="bs">0</span></div>
  <div class="si">Level: <span id="lv">1</span></div>
</div>
<canvas id="c" width="400" height="400"></canvas>
<div id="msg">Press Start to play!</div>
<div><button onclick="startGame()">Start</button><button onclick="pauseGame()">Pause</button></div>
<div class="hint">Arrow keys or W A S D to move</div>
<script>
const C=document.getElementById('c'),ctx=C.getContext('2d');
const SZ=20,COLS=20,ROWS=20;
let snake,dir,food,score,best=0,running=false,paused=false,loop,speed,level;
function startGame(){
  snake=[{x:10,y:10},{x:9,y:10},{x:8,y:10}];
  dir={x:1,y:0};score=0;level=1;speed=150;
  placeFood();running=true;paused=false;
  document.getElementById('msg').textContent='';
  clearInterval(loop);loop=setInterval(tick,speed);draw();
}
function pauseGame(){
  if(!running)return;paused=!paused;
  document.getElementById('msg').textContent=paused?'Paused':'';
  if(!paused){clearInterval(loop);loop=setInterval(tick,speed);}else clearInterval(loop);
}
function placeFood(){
  do{food={x:Math.floor(Math.random()*COLS),y:Math.floor(Math.random()*ROWS)};
  }while(snake.some(s=>s.x===food.x&&s.y===food.y));
}
function tick(){
  if(!running||paused)return;
  const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
  if(head.x<0||head.x>=COLS||head.y<0||head.y>=ROWS){endGame();return;}
  if(snake.some(s=>s.x===head.x&&s.y===head.y)){endGame();return;}
  snake.unshift(head);
  if(head.x===food.x&&head.y===food.y){
    score++;document.getElementById('sc').textContent=score;
    if(score>best){best=score;document.getElementById('bs').textContent=best;}
    if(score%5===0&&speed>60){speed=Math.max(60,speed-15);level++;
      document.getElementById('lv').textContent=level;
      clearInterval(loop);loop=setInterval(tick,speed);}
    placeFood();
  }else snake.pop();
  draw();
}
function endGame(){
  running=false;clearInterval(loop);
  document.getElementById('msg').textContent='Game Over! Score:'+score+' — Press Start to retry!';
}
function draw(){
  ctx.clearRect(0,0,400,400);
  ctx.strokeStyle='#FFE4EF';ctx.lineWidth=0.5;
  for(let i=0;i<=COLS;i++){ctx.beginPath();ctx.moveTo(i*SZ,0);ctx.lineTo(i*SZ,400);ctx.stroke();}
  for(let j=0;j<=ROWS;j++){ctx.beginPath();ctx.moveTo(0,j*SZ);ctx.lineTo(400,j*SZ);ctx.stroke();}
  ctx.font='16px serif';ctx.fillText('',food.x*SZ+2,food.y*SZ+16);
  ctx.fillStyle='#E91E63';ctx.beginPath();
  ctx.arc(food.x*SZ+10,food.y*SZ+10,7,0,Math.PI*2);ctx.fill();
  snake.forEach((seg,i)=>{
    const p=i/snake.length;
    ctx.fillStyle='rgb(255,'+Math.floor(105+(1-p)*50)+','+Math.floor(180-(1-p)*60)+')';
    ctx.beginPath();ctx.roundRect(seg.x*SZ+1,seg.y*SZ+1,SZ-2,SZ-2,4);ctx.fill();
    if(i===0){
      ctx.fillStyle='white';
      ctx.beginPath();ctx.arc(seg.x*SZ+6,seg.y*SZ+7,3,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*SZ+14,seg.y*SZ+7,3,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#8B1A4A';
      ctx.beginPath();ctx.arc(seg.x*SZ+6+dir.x,seg.y*SZ+7+dir.y,1.5,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*SZ+14+dir.x,seg.y*SZ+7+dir.y,1.5,0,Math.PI*2);ctx.fill();
    }
  });
}
document.addEventListener('keydown',e=>{
  const k=e.key;
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d'].includes(k))e.preventDefault();
  if((k==='ArrowUp'||k==='w')&&dir.y!==1)dir={x:0,y:-1};
  if((k==='ArrowDown'||k==='s')&&dir.y!==-1)dir={x:0,y:1};
  if((k==='ArrowLeft'||k==='a')&&dir.x!==1)dir={x:-1,y:0};
  if((k==='ArrowRight'||k==='d')&&dir.x!==-1)dir={x:1,y:0};
});
let tx=0,ty=0;
C.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY;},{passive:true});
C.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-tx,dy=e.changedTouches[0].clientY-ty;
  if(Math.abs(dx)>Math.abs(dy)){
    if(dx>0&&dir.x!==-1)dir={x:1,y:0};else if(dx<0&&dir.x!==1)dir={x:-1,y:0};
  }else{
    if(dy>0&&dir.y!==-1)dir={x:0,y:1};else if(dy<0&&dir.y!==1)dir={x:0,y:-1};
  }
},{passive:true});
draw();
</script></body></html>"""
    st.components.v1.html(snake_html, height=540, scrolling=False)

# ============================================================
# GAME 6 — Ludo (SVG visual board)
# ============================================================
LUDO_COLORS  = ["Red","Green","Yellow","Blue"]
LUDO_HEX     = {"Red":"#E91E63","Green":"#4CAF50","Yellow":"#FFC107","Blue":"#2196F3"}
LUDO_LIGHT   = {"Red":"#FCE4EC","Green":"#E8F5E9","Yellow":"#FFFDE7","Blue":"#E3F2FD"}
LUDO_DARK    = {"Red":"#C62828","Green":"#1B5E20","Yellow":"#F57F17","Blue":"#0D47A1"}
LUDO_START   = {"Red":0,"Green":13,"Yellow":26,"Blue":39}
LUDO_HOME_ENTRY = {"Red":50,"Green":11,"Yellow":24,"Blue":37}
LUDO_SAFE    = {0,8,13,21,26,34,39,47}

# --- SVG Ludo Board renderer ---
# Board is 15x15 grid. Each cell = 36px => 540x540 total
CS  = 36   # cell size px
BSZ = 15*CS  # board size

def _cell_color(r, c):
    """Return fill color for each cell on the 15x15 ludo grid."""
    # Color zones (home bases 6x6 corners)
    if r<6 and c<6:   return LUDO_LIGHT["Red"]    # Red home
    if r<6 and c>8:   return LUDO_LIGHT["Green"]  # Green home
    if r>8 and c<6:   return LUDO_LIGHT["Blue"]   # Blue home
    if r>8 and c>8:   return LUDO_LIGHT["Yellow"] # Yellow home
    # Center home triangle colors (simplified 3x3 center)
    if 6<=r<=8 and 6<=c<=8: return "#FFF0F5"
    return "white"

def _is_safe_cell(r, c):
    """Highlight star safe squares."""
    safe_cells = {
        (2,6),(6,2),(12,8),(8,12),
        (6,12),(2,8),(8,2),(12,6),
    }
    return (r,c) in safe_cells

# Map board square index (0-51) to (row, col) on 15x15 grid
# Standard ludo path going clockwise starting Red=top-left entry
_PATH = [
    # Red start going down left column (col6, rows 14->9)
    (14,6),(13,6),(12,6),(11,6),(10,6),(9,6),
    # turn right along bottom (row8, cols 6->0) -- actually standard ludo:
    # We'll use a standard mapping
    (8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
    # up left side (col0 -> but ludo path goes col0 up then right)
    (7,0),(6,0),
    (6,1),(6,2),(6,3),(6,4),(6,5),
    (5,6),(4,6),(3,6),(2,6),(1,6),(0,6),
    (0,7),
    (0,8),(1,8),(2,8),(3,8),(4,8),(5,8),
    (6,9),(6,10),(6,11),(6,12),(6,13),(6,14),
    (7,14),
    (8,14),(8,13),(8,12),(8,11),(8,10),(8,9),
    (9,8),(10,8),(11,8),(12,8),(13,8),(14,8),
    (14,7),
]
# Home columns (pieces slide in after entry)
_HOME_COL = {
    "Red":    [(13,7),(12,7),(11,7),(10,7),(9,7)],
    "Green":  [(7,1), (7,2), (7,3), (7,4), (7,5)],
    "Yellow": [(1,7), (2,7), (3,7), (4,7), (5,7)],
    "Blue":   [(7,13),(7,12),(7,11),(7,10),(7,9)],
}
_HOME_CENTER = (7,7)

def _ludo_board_svg(pieces_state, color_map, active_player_idx, players):
    """Generate full SVG ludo board with pieces drawn on it."""
    cells_html = []
    # Draw grid cells
    for r in range(15):
        for c in range(15):
            x = c*CS; y = r*CS
            fill = _cell_color(r,c)
            # Color the entry columns
            if c==6 and 1<=r<=5:  fill=LUDO_LIGHT["Red"]
            if r==7 and 1<=c<=5:  fill=LUDO_LIGHT["Green"]
            if c==8 and 1<=r<=5:  fill=LUDO_LIGHT["Yellow"]
            if r==7 and 9<=c<=13: fill=LUDO_LIGHT["Blue"]
            if c==7 and 9<=r<=13: fill=LUDO_LIGHT["Red"]
            if c==7 and 1<=r<=5:  fill=LUDO_LIGHT["Yellow"]

            stroke = "#ddd"
            sw     = "0.5"
            # Safe star cells
            is_safe = _is_safe_cell(r,c)
            if is_safe: fill="#FFFF99"

            cells_html.append(
                '<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(CS) + '" height="' + str(CS) + '" '
                'fill="' + fill + '" stroke="' + stroke + '" stroke-width="' + sw + '"/>')
            if is_safe:
                cx_ = x+CS//2; cy_ = y+CS//2
                cells_html.append('<text x="' + str(cx_) + '" y="' + str(cy_+5) + '" text-anchor="middle" font-size="14" fill="#888">*</text>')

    # Home base squares (inner 4x4 safe zones)
    for col, (r0,c0) in [("Red",(1,1)),("Green",(1,9)),("Yellow",(9,9)),("Blue",(9,1))]:
        x0=c0*CS; y0=r0*CS; sz=4*CS
        cells_html.append('<rect x="' + str(x0) + '" y="' + str(y0) + '" width="' + str(sz) + '" height="' + str(sz) + '" fill="' + LUDO_HEX[col] + '" rx="8" opacity="0.18"/>')
        cells_html.append('<rect x="' + str(x0+CS//2) + '" y="' + str(y0+CS//2) + '" width="' + str(sz-CS) + '" height="' + str(sz-CS) + '" fill="white" rx="6" opacity="0.7"/>')

    # Center triangle
    cx_ = 7*CS+CS//2; cy_ = 7*CS+CS//2; half=CS*1.5
    cells_html.append(
        '<polygon points="' +
        str(cx_-half)+','+str(cy_-half)+' '+
        str(cx_+half)+','+str(cy_-half)+' '+
        str(cx_)+','+str(cy_) +
        '" fill="' + LUDO_HEX["Red"] + '" opacity="0.7"/>')
    cells_html.append(
        '<polygon points="' +
        str(cx_+half)+','+str(cy_-half)+' '+
        str(cx_+half)+','+str(cy_+half)+' '+
        str(cx_)+','+str(cy_) +
        '" fill="' + LUDO_HEX["Green"] + '" opacity="0.7"/>')
    cells_html.append(
        '<polygon points="' +
        str(cx_-half)+','+str(cy_+half)+' '+
        str(cx_+half)+','+str(cy_+half)+' '+
        str(cx_)+','+str(cy_) +
        '" fill="' + LUDO_HEX["Blue"] + '" opacity="0.7"/>')
    cells_html.append(
        '<polygon points="' +
        str(cx_-half)+','+str(cy_-half)+' '+
        str(cx_-half)+','+str(cy_+half)+' '+
        str(cx_)+','+str(cy_) +
        '" fill="' + LUDO_HEX["Yellow"] + '" opacity="0.7"/>')

    # Draw pieces
    # Piece positions in base: fixed spots inside home base
    base_offsets = [(1,1),(2,1),(1,2),(2,2)]
    base_origins = {
        "Red":    (1,1), "Green": (1,9),
        "Yellow": (9,9), "Blue":  (9,1),
    }
    piece_elements = []
    # count pieces per cell to offset overlaps
    cell_counts = {}

    for player in players:
        col   = color_map[player]
        hexc  = LUDO_HEX[col]
        darkc = LUDO_DARK[col]
        br,bc = base_origins[col]
        for pi, pc in enumerate(pieces_state[player]):
            if pc["done"]:
                # draw in center
                off = pi * 5
                cx2 = _HOME_CENTER[1]*CS + CS//2 + (pi%2)*10 - 5
                cy2 = _HOME_CENTER[0]*CS + CS//2 + (pi//2)*10 - 5
                piece_elements.append(
                    '<circle cx="'+str(cx2)+'" cy="'+str(cy2)+'" r="10" fill="'+hexc+'" stroke="'+darkc+'" stroke-width="2" opacity="0.9"/>'
                    '<text x="'+str(cx2)+'" y="'+str(cy2+4)+'" text-anchor="middle" font-size="9" font-weight="bold" fill="white">'+str(pi+1)+'</text>')
            elif not pc["out"]:
                # in base
                dr, dc = base_offsets[pi]
                r2 = br + dr; c2 = bc + dc
                cx2 = c2*CS + CS//2; cy2 = r2*CS + CS//2
                piece_elements.append(
                    '<circle cx="'+str(cx2)+'" cy="'+str(cy2)+'" r="12" fill="'+hexc+'" stroke="'+darkc+'" stroke-width="2.5"/>'
                    '<text x="'+str(cx2)+'" y="'+str(cy2+5)+'" text-anchor="middle" font-size="10" font-weight="bold" fill="white">'+str(pi+1)+'</text>')
            else:
                steps_to_entry = (LUDO_HOME_ENTRY[col] - LUDO_START[col]) % 52
                if pc["steps"] > steps_to_entry:
                    home_idx = pc["steps"] - steps_to_entry - 1
                    if home_idx < len(_HOME_COL[col]):
                        r2,c2 = _HOME_COL[col][home_idx]
                    else:
                        r2,c2 = _HOME_CENTER
                else:
                    board_idx = (LUDO_START[col] + pc["steps"]) % 52
                    if board_idx < len(_PATH):
                        r2,c2 = _PATH[board_idx]
                    else:
                        r2,c2 = _HOME_CENTER
                key = (r2,c2)
                cnt = cell_counts.get(key,0)
                cell_counts[key] = cnt+1
                off_x = (cnt%2)*8 - 4
                off_y = (cnt//2)*8 - 4
                cx2 = c2*CS + CS//2 + off_x
                cy2 = r2*CS + CS//2 + off_y
                piece_elements.append(
                    '<circle cx="'+str(cx2)+'" cy="'+str(cy2)+'" r="11" fill="'+hexc+'" stroke="'+darkc+'" stroke-width="2.5" opacity="0.95"/>'
                    '<text x="'+str(cx2)+'" y="'+str(cy2+4)+'" text-anchor="middle" font-size="9" font-weight="bold" fill="white">'+str(pi+1)+'</text>')

    svg = ('<svg width="' + str(BSZ) + '" height="' + str(BSZ) + '" xmlns="http://www.w3.org/2000/svg">'
           '<rect width="' + str(BSZ) + '" height="' + str(BSZ) + '" fill="#FFF0F5" rx="12" stroke="#FFB6C1" stroke-width="2"/>'
           + "".join(cells_html) + "".join(piece_elements) + '</svg>')
    return svg

def ludo_path_pos(color, steps):
    start = LUDO_START[color]
    entry = LUDO_HOME_ENTRY[color]
    steps_to_entry = (entry - start) % 52
    if steps > steps_to_entry:
        home_idx = steps - steps_to_entry - 1
        if home_idx >= 5: return ("done", 0)
        return ("home", home_idx)
    return ("board", (start + steps) % 52)

def init_ludo():
    s = st.session_state
    s.ld_pieces = {p:[{"steps":0,"out":False,"done":False} for _ in range(4)] for p in s.ld_players}
    s.ld_current_player = 0
    s.ld_dice_val       = 0
    s.ld_rolled         = False
    s.ld_message        = "Roll the dice to begin!"
    s.ld_winner         = None
    s.ld_consecutive6   = 0

def game_ludo():
    init({"ld_started":False,"ld_players":[],"ld_n_humans":2,"ld_n_cpu":0,
          "ld_pieces":{},"ld_current_player":0,"ld_dice_val":0,
          "ld_rolled":False,"ld_message":"","ld_winner":None,"ld_consecutive6":0,
          "ld_color_map":{}})
    s = st.session_state
    st.markdown("## 🎯 Ludo - Multiplayer")
    st.caption("Race all 4 pieces home before your opponents! Roll a 6 to start. 👑")

    if not s.ld_started:
        col1,col2 = st.columns(2)
        with col1: n_h = st.selectbox("Human players",[1,2,3,4],index=1,key="ld_nh")
        with col2: n_c = st.selectbox("CPU players",  [0,1,2,3],index=0,key="ld_nc")
        if n_h+n_c<2: st.warning("Need at least 2 players!"); return
        if n_h+n_c>4: st.warning("Max 4 players!"); return

        names=[]
        for i in range(n_h):
            nm = st.text_input(LUDO_COLORS[i]+" player name", value=LUDO_COLORS[i], key="ld_name_"+str(i))
            names.append(nm)
        for i in range(n_c):
            names.append("CPU("+LUDO_COLORS[n_h+i]+")")

        st.markdown("**Color assignment:** " + ", ".join(n+"="+LUDO_COLORS[i] for i,n in enumerate(names)))

        if st.button("🌸 Start Ludo", key="ld_start"):
            s.ld_players   = names
            s.ld_n_humans  = n_h
            s.ld_color_map = {names[i]: LUDO_COLORS[i] for i in range(len(names))}
            s.ld_started   = True
            init_ludo()
            st.rerun()
        st.markdown("**Rules:** Roll 6 to bring piece out | Extra turn on 6 | Land on opponent = send back | Safe squares (*) protect pieces | First to get all 4 home wins!")
        return

    if s.ld_winner:
        st.balloons()
        st.success("👑 **" + s.ld_winner + "** wins Ludo! 🌸🎉")
        if st.button("🔄 New Game", key="ld_newgame"):
            s.ld_started=False; st.rerun()
        return

    players    = s.ld_players
    n_humans   = s.ld_n_humans
    cur_idx    = s.ld_current_player
    cur_player = players[cur_idx]
    cur_color  = s.ld_color_map[cur_player]
    is_cpu     = cur_idx >= n_humans

    # Layout: board left, controls right
    board_col, ctrl_col = st.columns([3,2])

    with board_col:
        svg = _ludo_board_svg(s.ld_pieces, s.ld_color_map, cur_idx, players)
        st.markdown('<div style="overflow-x:auto">' + svg + '</div>', unsafe_allow_html=True)

    with ctrl_col:
        # Current player + color swatch
        hexc = LUDO_HEX[cur_color]
        st.markdown(
            "<div style='background:"+hexc+";color:white;border-radius:14px;padding:10px 16px;margin-bottom:10px;'>"
            "<b>"+("🤖 " if is_cpu else "🎀 ")+cur_player+"</b><br>"
            "<span style='font-size:12px;opacity:.85'>Color: "+cur_color+"</span></div>",
            unsafe_allow_html=True)

        st.info(s.ld_message)

        # Scoreboard
        st.markdown("**Scoreboard:**")
        for p in players:
            col_ = s.ld_color_map[p]
            done = sum(1 for pc in s.ld_pieces[p] if pc["done"])
            hx   = LUDO_HEX[col_]
            bar  = "█"*done + "░"*(4-done)
            st.markdown(
                "<div style='display:flex;align-items:center;gap:8px;margin:4px 0'>"
                "<span style='background:"+hx+";color:white;border-radius:8px;padding:2px 10px;font-size:12px;font-weight:700'>"+p+"</span>"
                "<span style='font-family:monospace;color:"+hx+";font-size:16px'>"+bar+"</span>"
                "<span style='font-size:12px;color:#C2547A'>"+str(done)+"/4 home</span>"
                "</div>", unsafe_allow_html=True)

        st.divider()

        # Dice display
        if s.ld_rolled and s.ld_dice_val > 0:
            st.markdown("<div style='text-align:center'>" + dice_svg(s.ld_dice_val, 80) + "</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;font-size:24px;font-weight:700;color:#FF1493'>" + str(s.ld_dice_val) + "</p>", unsafe_allow_html=True)

        if not s.ld_rolled:
            if is_cpu:
                if st.button("🤖 CPU Rolls", key="ld_cpu_roll"):
                    _ludo_roll_and_auto(); st.rerun()
            else:
                if st.button("🎲 Roll Dice", key="ld_roll"):
                    _ludo_roll(); st.rerun()
        else:
            movable = _get_movable_pieces(cur_player, s.ld_dice_val)
            if not movable:
                st.warning("No movable pieces — turn passes.")
                if st.button("Next Turn", key="ld_pass"):
                    _next_turn(rolled_six=(s.ld_dice_val==6)); st.rerun()
            else:
                if is_cpu:
                    _cpu_move(cur_player, movable); st.rerun()
                else:
                    st.markdown("**Choose a piece to move:**")
                    for pi, desc in movable:
                        if st.button("Piece " + str(pi+1) + " - " + desc, key="ld_move_"+str(pi)):
                            _ludo_move_piece(cur_player, pi, s.ld_dice_val); st.rerun()

def _get_movable_pieces(player, dice):
    s      = st.session_state
    col    = s.ld_color_map[player]
    pieces = s.ld_pieces[player]
    movable = []
    for i,pc in enumerate(pieces):
        if pc["done"]: continue
        if not pc["out"]:
            if dice==6: movable.append((i,"Bring out of base"))
        else:
            new_steps = pc["steps"] + dice
            steps_to_entry = (LUDO_HOME_ENTRY[col] - LUDO_START[col]) % 52
            if pc["steps"] > steps_to_entry:
                home_remaining = 5 - (pc["steps"] - steps_to_entry - 1)
                if dice > home_remaining: continue
            movable.append((i,"Move +" + str(dice) + " steps"))
    return movable

def _ludo_roll():
    s   = st.session_state
    val = random.randint(1,6)
    s.ld_dice_val = val; s.ld_rolled = True
    if val==6: s.ld_consecutive6 += 1
    else:       s.ld_consecutive6  = 0
    if s.ld_consecutive6 >= 3:
        s.ld_message = "Three 6s in a row! Turn forfeited."
        s.ld_consecutive6 = 0; _next_turn(rolled_six=False)
    else:
        s.ld_message = s.ld_players[s.ld_current_player] + " rolled a " + str(val) + "!"

def _ludo_roll_and_auto():
    _ludo_roll()
    s = st.session_state
    if s.ld_rolled and s.ld_consecutive6 < 3:
        cur     = s.ld_players[s.ld_current_player]
        movable = _get_movable_pieces(cur, s.ld_dice_val)
        if movable: _cpu_move(cur, movable)
        else:       _next_turn(rolled_six=(s.ld_dice_val==6))

def _cpu_move(player, movable):
    s = st.session_state
    # Strategy: prefer piece furthest along, or bring out if roll is 6
    out_pieces = [(pi,d) for pi,d in movable if "Bring" not in d]
    in_pieces  = [(pi,d) for pi,d in movable if "Bring" in d]
    if out_pieces:
        best = max(out_pieces, key=lambda x: s.ld_pieces[player][x[0]]["steps"])
    else:
        best = in_pieces[0]
    _ludo_move_piece(player, best[0], s.ld_dice_val)

def _ludo_move_piece(player, piece_idx, dice):
    s   = st.session_state
    col = s.ld_color_map[player]
    pc  = s.ld_pieces[player][piece_idx]
    if not pc["out"]:
        pc["out"]=True; pc["steps"]=0
        s.ld_message = player + " brought Piece " + str(piece_idx+1) + " out of base!"
    else:
        pc["steps"] += dice
        typ, idx = ludo_path_pos(col, pc["steps"])
        if typ=="done":
            pc["done"]=True
            s.ld_message = player + "'s Piece " + str(piece_idx+1) + " reached HOME! Celebrating!"
        elif typ=="home":
            s.ld_message = player + "'s Piece " + str(piece_idx+1) + " is in the home column (step " + str(idx+1) + ")"
        else:
            board_sq = idx
            s.ld_message = player + "'s Piece " + str(piece_idx+1) + " moved to square " + str(board_sq)
            if board_sq not in LUDO_SAFE:
                for other_p in s.ld_players:
                    if other_p==player: continue
                    other_col = s.ld_color_map[other_p]
                    for opc in s.ld_pieces[other_p]:
                        if not opc["out"] or opc["done"]: continue
                        otyp,oidx = ludo_path_pos(other_col, opc["steps"])
                        if otyp=="board" and oidx==board_sq:
                            opc["out"]=False; opc["steps"]=0
                            s.ld_message += " -- captured " + other_p + "'s piece! Sent back to base!"
    if all(p["done"] for p in s.ld_pieces[player]):
        s.ld_winner = player; return
    _next_turn(rolled_six=(dice==6))

def _next_turn(rolled_six):
    s = st.session_state; s.ld_rolled=False
    if not rolled_six:
        s.ld_current_player = (s.ld_current_player+1) % len(s.ld_players)

# ============================================================
# MAIN
# ============================================================
def main():
    with st.sidebar:
        st.markdown("# TP Girl Games")
        st.markdown("*your girly game hub* 🌸")
        st.markdown("---")
        game = st.radio("Choose a game:", [
            "🎰 Lottery Guess",
            "🌸 Pink Trivia",
            "🪢 Hangman",
            "🎲 Dice Duel",
            "🐍 Snake Game",
            "🎯 Ludo",
        ], key="game_sel")
        st.markdown("---")
        tips = {
            "🎰 Lottery Guess": "Guess the number!\nHot/cold hints & streaks",
            "🌸 Pink Trivia":   "No repeats until all done!\nFilter by category",
            "🪢 Hangman":       "Guess letters!\n6 wrong = game over",
            "🎲 Dice Duel":     "2-4 players PvP or CPU!\nFirst to target wins",
            "🐍 Snake Game":    "Arrow keys or WASD\nEat the pink food!",
            "🎯 Ludo":          "2-4 players PvP or CPU\nRoll 6 to start pieces!",
        }
        st.caption(tips.get(game,""))
        st.markdown("---")
        st.caption("made with love & Python")

    st.markdown("<h1>💖 TP Girl Games 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#F48FB1'>your favourite girly game hub</p>", unsafe_allow_html=True)
    st.divider()

    if   game == "🎰 Lottery Guess": game_lottery()
    elif game == "🌸 Pink Trivia":   game_trivia()
    elif game == "🪢 Hangman":       game_hangman()
    elif game == "🎲 Dice Duel":     game_dice_duel()
    elif game == "🐍 Snake Game":    game_snake()
    elif game == "🎯 Ludo":          game_ludo()

if __name__ == "__main__":
    main()
