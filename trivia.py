# -*- coding: utf-8 -*-
"""games/trivia.py — TP Games: Pink Trivia Quiz"""
import random
import json
import os
import streamlit as st
from theme import init, reset_game

TRIVIA_CSS = """
<style>
.tv-prog-wrap{height:8px;background:#3D1E34;border-radius:99px;overflow:hidden;margin:10px 0 16px;}
.tv-prog-fill{height:8px;background:linear-gradient(90deg,#8B2050,#FF1493);border-radius:99px;transition:width .4s;}
.tv-cat-badge{display:inline-block;background:#3D1E34;color:#FF69B4;border:1px solid #8B2050;
  border-radius:6px;padding:2px 12px;font-size:12px;font-weight:700;letter-spacing:1px;
  text-transform:uppercase;margin-bottom:12px;}
.tv-qcard{background:#2D1224;border-radius:14px;padding:28px 32px;border:1px solid #8B2050;
  box-shadow:0 0 24px rgba(255,20,147,.15);margin:12px 0;text-align:center;}
.tv-qnum{font-size:11px;color:#8B3060;font-weight:700;letter-spacing:3px;
  text-transform:uppercase;margin-bottom:10px;}
.tv-question{font-size:20px;font-weight:700;color:#F8D7E8;line-height:1.5;}
.tv-streak-badge{background:linear-gradient(135deg,#FF8C00,#FF4500);color:white;
  border-radius:8px;padding:6px 16px;font-weight:700;font-size:13px;display:inline-block;margin-bottom:8px;}
.tv-score-badge{background:linear-gradient(135deg,#8B2050,#FF1493);color:white;
  border-radius:8px;padding:6px 18px;font-weight:700;font-size:14px;display:inline-block;}
.tv-result{background:#2D1224;border-radius:16px;padding:36px;text-align:center;
  border:1px solid #8B2050;box-shadow:0 0 40px rgba(255,20,147,.2);}
.tv-grade{font-size:36px;font-weight:800;color:#FF1493;margin-bottom:6px;}
.tv-msg{font-size:15px;color:#C2547A;margin-bottom:20px;}
.tv-big-score{font-size:56px;font-weight:900;
  background:linear-gradient(135deg,#FF69B4,#FF1493);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.tv-pct{font-size:13px;color:#8B3060;margin-top:4px;}
.tv-stat-row{display:flex;justify-content:center;gap:16px;margin:20px 0;flex-wrap:wrap;}
.tv-stat{background:#3D1E34;border-radius:10px;padding:14px 22px;text-align:center;
  border:1px solid #8B2050;min-width:80px;}
.tv-stat-val{font-size:26px;font-weight:800;color:#FF69B4;}
.tv-stat-lbl{font-size:10px;color:#8B3060;font-weight:700;text-transform:uppercase;letter-spacing:1px;}
.tv-opt-neutral{background:#3D1E34;border:1px solid #5A2040;border-radius:10px;
  padding:13px;text-align:center;color:#8B3060;font-size:14px;}
</style>
"""

def load_questions(base_dir: str):
    path = os.path.join(base_dir, "trivia_questions.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []

def run(base_dir: str):
    init({"tv_used":[],"tv_questions":[],"tv_idx":0,
          "tv_score":0,"tv_answered":False,"tv_selected":"",
          "tv_done":False,"tv_started":False,"tv_streak":0,"tv_best_streak":0})
    s    = st.session_state
    all_q = load_questions(base_dir)

    st.markdown(TRIVIA_CSS, unsafe_allow_html=True)
    st.markdown("## 🌸 Pink Trivia Quiz")

    if not all_q:
        st.error("trivia_questions.json not found! Place it in the same folder as app.py.")
        return

    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        cats = ["All"] + sorted(set(q["category"] for q in all_q))
        cat  = st.selectbox("Category", cats, key="tv_cat")
    with col2:
        n_q  = st.selectbox("Questions", [5,8,10,15], index=1, key="tv_nq")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Stats", key="tv_rst"):
            reset_game("tv_"); st.rerun()

    pool = [q for q in all_q if cat=="All" or q["category"]==cat]

    col_start, _ = st.columns([1,2])
    with col_start:
        if st.button("Start New Quiz", key="tv_new") or not s.tv_started:
            if not pool:
                st.warning("No questions in this category!"); return
            avail = [q for q in pool if q not in s.tv_used]
            if len(avail) < n_q:
                s.tv_used = []; avail = pool[:]
            selected      = random.sample(avail, min(n_q, len(avail)))
            s.tv_used    += selected
            s.tv_questions = selected
            s.tv_idx=0; s.tv_score=0; s.tv_answered=False
            s.tv_selected=""; s.tv_done=False; s.tv_started=True; s.tv_streak=0
            st.rerun()

    if not s.tv_started: return
    total = len(s.tv_questions)

    # ── Results screen ──────────────────────────────────────────
    if s.tv_done:
        pct = int(s.tv_score / total * 100)
        if pct>=80:   grade,msg = "Quiz Queen!",    "You absolutely aced it!"
        elif pct>=60: grade,msg = "Pretty Sharp!",  "Great job — almost there!"
        elif pct>=40: grade,msg = "Getting There!", "Keep practicing!"
        else:         grade,msg = "Keep Studying!", "Try again — you'll get it!"

        st.markdown(
            f'<div class="tv-result">'
            f'<div class="tv-grade">{grade}</div>'
            f'<div class="tv-msg">{msg}</div>'
            f'<div class="tv-big-score">{s.tv_score}/{total}</div>'
            f'<div class="tv-pct">{pct}% correct</div>'
            f'<div class="tv-stat-row">'
            f'<div class="tv-stat"><div class="tv-stat-val">{s.tv_score}</div><div class="tv-stat-lbl">Correct</div></div>'
            f'<div class="tv-stat"><div class="tv-stat-val">{total-s.tv_score}</div><div class="tv-stat-lbl">Wrong</div></div>'
            f'<div class="tv-stat"><div class="tv-stat-val">{s.tv_best_streak}</div><div class="tv-stat-lbl">Best Streak</div></div>'
            f'</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Play Again", key="tv_again"):
            s.tv_started = False; st.rerun()
        return

    # ── Active question ──────────────────────────────────────────
    q    = s.tv_questions[s.tv_idx]
    prog = s.tv_idx / total

    st.markdown(
        f'<div class="tv-prog-wrap"><div class="tv-prog-fill" style="width:{int(prog*100)}%"></div></div>',
        unsafe_allow_html=True)

    top_l, top_r = st.columns([3,1])
    with top_l:
        st.markdown(f'<span class="tv-score-badge">Score: {s.tv_score} / {total}</span>', unsafe_allow_html=True)
    with top_r:
        if s.tv_streak >= 3:
            st.markdown(f'<span class="tv-streak-badge">🔥 {s.tv_streak} streak!</span>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="tv-qcard">'
        f'<div class="tv-qnum">Question {s.tv_idx+1} of {total}</div>'
        f'<div class="tv-cat-badge">{q["category"]}</div><br>'
        f'<div class="tv-question">{q["question"]}</div>'
        f'</div>', unsafe_allow_html=True)

    # 2×2 option grid
    opts  = q["options"]
    row1  = st.columns(2)
    row2  = st.columns(2)
    all_c = [row1[0], row1[1], row2[0], row2[1]]

    for i, opt in enumerate(opts):
        with all_c[i]:
            if s.tv_answered:
                if opt == q["answer"]:
                    st.success(f"✓  {opt}")
                elif opt == s.tv_selected:
                    st.error(f"✗  {opt}")
                else:
                    st.markdown(f'<div class="tv-opt-neutral">{opt}</div>', unsafe_allow_html=True)
            else:
                if st.button(opt, key=f"tv_{s.tv_idx}_{i}", use_container_width=True):
                    s.tv_selected = opt; s.tv_answered = True
                    if opt == q["answer"]:
                        s.tv_score   += 1; s.tv_streak += 1
                        s.tv_best_streak = max(s.tv_best_streak, s.tv_streak)
                    else:
                        s.tv_streak = 0
                    st.rerun()

    if s.tv_answered:
        st.markdown("<br>", unsafe_allow_html=True)
        if s.tv_selected == q["answer"]:
            bonus = " (streak bonus!)" if s.tv_streak >= 3 else ""
            st.success(f"Correct!{bonus}")
        else:
            st.error(f"The answer was: **{q['answer']}**")
        if st.button("Next Question", key="tv_next"):
            s.tv_idx += 1; s.tv_answered = False; s.tv_selected = ""
            if s.tv_idx >= total: s.tv_done = True
            st.rerun()
