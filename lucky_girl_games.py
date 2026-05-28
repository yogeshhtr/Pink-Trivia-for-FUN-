import streamlit as st
import random
import json
import os
import math

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="💖 Lucky Girl Games", page_icon="🌸",
                   layout="wide", initial_sidebar_state="expanded")

# ── CSS ──────────────────────────────────────────────────────────────────────
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
.ludo-cell{width:38px;height:38px;border:1px solid #ddd;display:inline-flex;
  align-items:center;justify-content:center;font-size:11px;border-radius:4px;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def init(keys):
    for k, v in keys.items():
        if k not in st.session_state:
            st.session_state[k] = v

PINK = ["#FF69B4","#FF1493","#FFB6C1","#C2185B","#F48FB1"]

# ════════════════════════════════════════════════════════════════════════════
# GAME 1 — Lottery Guess
# ════════════════════════════════════════════════════════════════════════════
def game_lottery():
    init({"lot_secret":0,"lot_tries":0,"lot_max_tries":5,"lot_max_num":50,
          "lot_done":False,"lot_history":[],"lot_wins":0,"lot_losses":0,
          "lot_started":False,"lot_streak":0,"lot_best":0})
    s = st.session_state
    st.markdown("## 🎰 Lucky Number Lottery")
    st.caption("Guess the secret number hiding in our pink vault! 💗")

    diff = st.selectbox("Difficulty",["🌸 Easy (1–30, 7 tries)","💗 Medium (1–50, 5 tries)","💀 Hard (1–99, 4 tries)"],key="lot_diff")
    cfg  = {"🌸 Easy (1–30, 7 tries)":(30,7),"💗 Medium (1–50, 5 tries)":(50,5),"💀 Hard (1–99, 4 tries)":(99,4)}
    max_num,max_tries = cfg[diff]

    if st.button("🌸 New Game",key="lot_new"):
        s.lot_secret=random.randint(1,max_num); s.lot_tries=0
        s.lot_max_tries=max_tries; s.lot_max_num=max_num
        s.lot_done=False; s.lot_history=[]; s.lot_started=True
        st.rerun()

    if not s.lot_started:
        st.info("Press **New Game** to start!"); return

    rem = s.lot_max_tries - s.lot_tries
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Guesses",s.lot_tries); c2.metric("Remaining",rem)
    c3.metric("Wins",s.lot_wins);    c4.metric("Best Streak",s.lot_best)
    st.progress(max(0.,rem/s.lot_max_tries))

    balls=""
    for i in range(s.lot_max_tries):
        if i<len(s.lot_history):
            g,k=s.lot_history[i]
            cls="ball-win" if k=="win" else "ball-guess"
            balls+=f'<span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:{"#E8F5E9" if k=="win" else "#FFE4EF"};border:2px solid {"#4CAF50" if k=="win" else "#FF69B4"};font-weight:700;color:{"#2E7D32" if k=="win" else "#8B1A4A"};margin:3px;font-size:13px">{g}</span>'
        else:
            balls+=f'<span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#FFF0F5;border:2px solid #FFB6C1;color:#F48FB1;margin:3px;font-size:13px">?</span>'
    st.markdown(f'<div style="text-align:center;margin:10px 0">{balls}</div>',unsafe_allow_html=True)

    if s.lot_history:
        chip_parts = []
        for g,k in s.lot_history:
            cls   = "win" if k=="win" else ("low" if k=="low" else "high")
            arrow = "checkmark" if k=="win" else ("up" if k=="low" else "down")
            symbol = "✓" if k=="win" else ("↑" if k=="low" else "↓")
            chip_parts.append('<span class="chip chip-' + cls + '">' + symbol + ' ' + str(g) + '</span>')
        st.markdown('<div style="margin:6px 0">' + "".join(chip_parts) + '</div>', unsafe_allow_html=True)

    if not s.lot_done:
        guess = st.number_input(f"Number (1–{s.lot_max_num})",1,s.lot_max_num,step=1,key="lot_inp")
        if st.button("💌 Submit Guess",key="lot_sub"):
            g=int(guess); s.lot_tries+=1
            if g==s.lot_secret:
                s.lot_history.append((g,"win")); s.lot_wins+=1
                s.lot_streak+=1; s.lot_best=max(s.lot_best,s.lot_streak)
                s.lot_done=True
                st.success(f"🎉 YAAAS! {s.lot_secret} was right! Won in {s.lot_tries} tries! 🏆")
            elif s.lot_tries>=s.lot_max_tries:
                s.lot_history.append((g,"high" if g>s.lot_secret else "low"))
                s.lot_losses+=1; s.lot_streak=0; s.lot_done=True
                st.error(f"💔 No more tries! The number was {s.lot_secret}. Try again!")
            else:
                d=abs(g-s.lot_secret); r=s.lot_max_num
                dir_="higher" if g<s.lot_secret else "lower"
                k="low" if g<s.lot_secret else "high"
                s.lot_history.append((g,k))
                if d<=r*.05:   hint=f"🔥 Sooo close! Go just a bit **{dir_}**!"
                elif d<=r*.15: hint=f"💗 Getting warmer! A bit **{dir_}**~"
                else:          hint=f"🧊 Way off! Go **{dir_}**, babe! ({rem-1} tries left)"
                st.info(hint)
            st.rerun()
    else:
        if st.button("💖 Play Again",key="lot_again"):
            s.lot_secret=random.randint(1,max_num); s.lot_tries=0
            s.lot_max_tries=max_tries; s.lot_max_num=max_num
            s.lot_done=False; s.lot_history=[]; st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# GAME 2 — Pink Trivia (JSON-driven, no repeats)
# ════════════════════════════════════════════════════════════════════════════
def load_questions():
    path = os.path.join(os.path.dirname(__file__), "trivia_questions.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def game_trivia():
    init({"tv_pool":[],"tv_used":[],"tv_questions":[],"tv_idx":0,
          "tv_score":0,"tv_answered":False,"tv_selected":"",
          "tv_done":False,"tv_started":False,"tv_streak":0,
          "tv_cat_filter":"All"})
    s = st.session_state
    all_q = load_questions()

    st.markdown("## 🌸 Pink Trivia Quiz")
    st.caption("How smart are you? No question repeats until all are done! 💅")

    cats = ["All"] + sorted(set(q["category"] for q in all_q))
    col1,col2 = st.columns([2,1])
    with col1:
        cat = st.selectbox("Category filter",cats,key="tv_cat")
    with col2:
        n_q = st.selectbox("Questions per round",[5,8,10,15],index=1,key="tv_nq")

    pool = [q for q in all_q if cat=="All" or q["category"]==cat]

    if st.button("🌸 New Quiz",key="tv_new") or not s.tv_started:
        if len(pool)==0:
            st.warning("No questions in this category!"); return
        avail = [q for q in pool if q not in s.tv_used]
        if len(avail) < n_q:
            s.tv_used = []
            avail = pool[:]
        selected = random.sample(avail, min(n_q, len(avail)))
        s.tv_used      += selected
        s.tv_questions  = selected
        s.tv_idx=0; s.tv_score=0; s.tv_answered=False
        s.tv_selected=""; s.tv_done=False; s.tv_started=True; s.tv_streak=0
        st.rerun()

    if not s.tv_started: return

    total = len(s.tv_questions)

    if s.tv_done:
        pct = int(s.tv_score/total*100)
        if pct>=80:   grade,msg="Quiz Queen!","You absolutely aced it! Bow down! 👑"
        elif pct>=60: grade,msg="Pretty Smart!","Great job! A few more and you'll be queen! ✨"
        elif pct>=40: grade,msg="Getting There!","Not bad! Keep practicing! 💪"
        else:         grade,msg="Keep Studying!","Try again — you'll slay it next time! 🌺"
        st.markdown(f"""<div class='pink-card' style='text-align:center'>
          <h2 style='color:#FF1493'>{grade}</h2>
          <p style='font-size:18px;color:#C2547A'>{msg}</p>
          <p style='font-size:40px;font-weight:700;color:#FF1493'>{s.tv_score}/{total}</p>
          <p style='color:#F48FB1'>({pct}% correct)</p>
        </div>""",unsafe_allow_html=True)
        exhausted = len(s.tv_used) >= len(pool)
        if exhausted:
            st.info("🎉 You've gone through all questions! Pool will reset next round.")
        if st.button("💖 Play Again",key="tv_again"):
            s.tv_started=False; st.rerun()
        return

    q = s.tv_questions[s.tv_idx]
    st.progress(s.tv_idx/total)
    st.caption(f"Question {s.tv_idx+1} of {total}  •  Score: {s.tv_score}  •  Category: {q['category']}")
    if s.tv_streak>=3:
        st.success(f"🔥 {s.tv_streak}-answer streak!")

    st.markdown(f"""<div class='pink-card'>
      <p style='font-size:19px;font-weight:700;color:#8B1A4A;text-align:center'>{q['question']}</p>
    </div>""",unsafe_allow_html=True)

    for opt in q["options"]:
        if s.tv_answered:
            if opt==q["answer"]:    st.success(f"✅ {opt}")
            elif opt==s.tv_selected: st.error(f"❌ {opt}")
            else:                    st.write(f"○ {opt}")
        else:
            if st.button(opt,key=f"tv_{s.tv_idx}_{opt}"):
                s.tv_selected=opt; s.tv_answered=True
                if opt==q["answer"]: s.tv_score+=1; s.tv_streak+=1
                else: s.tv_streak=0
                st.rerun()

    if s.tv_answered:
        if s.tv_selected==q["answer"]: st.success("🎉 Correct! +1 point")
        else: st.error(f"💔 The answer was: **{q['answer']}**")
        if st.button("Next Question ➡️",key="tv_next"):
            s.tv_idx+=1; s.tv_answered=False; s.tv_selected=""
            if s.tv_idx>=total: s.tv_done=True
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# GAME 3 — Hangman (girly words + custom drawing)
# ════════════════════════════════════════════════════════════════════════════
HANG_WORDS = [
    ("BUTTERFLY","insects"),("PRINCESS","royalty"),("DIAMOND","gems"),
    ("GLITTER","fashion"),("UNICORN","fantasy"),("BLOSSOM","nature"),
    ("SPARKLE","fashion"),("RAINBOW","nature"),("TIARA","royalty"),
    ("VELVET","fabric"),("CRYSTAL","gems"),("RIBBON","fashion"),
    ("PERFUME","beauty"),("LIPSTICK","beauty"),("MASCARA","beauty"),
    ("EYELINER","beauty"),("BLUSHES","beauty"),("HAIRPIN","fashion"),
    ("STILETTO","shoes"),("STILETTOS","shoes"),("BRACELET","jewelry"),
    ("NECKLACE","jewelry"),("EARRINGS","jewelry"),("SAPPHIRE","gems"),
    ("AMETHYST","gems"),("LAVENDER","nature"),("MAGNOLIA","nature"),
    ("CAMELLIA","nature"),("JASMINE","nature"),("GARDENIA","nature"),
    ("CUPCAKE","food"),("MACARON","food"),("CHOCOLATE","food"),
    ("STRAWBERRY","food"),("CHEESECAKE","food"),("LEMONADE","food"),
    ("FANTASY","misc"),("ELEGANCE","misc"),("ROMANCE","misc"),
    ("ENCHANTED","misc"),("GORGEOUS","misc"),("RADIANCE","misc"),
]

def hangman_svg(wrong):
    parts = [
        # head
        '<circle cx="200" cy="90" r="25" stroke="#FF1493" stroke-width="3" fill="#FFE4EF"/>',
        # body
        '<line x1="200" y1="115" x2="200" y2="200" stroke="#FF1493" stroke-width="3"/>',
        # left arm
        '<line x1="200" y1="140" x2="160" y2="170" stroke="#FF1493" stroke-width="3"/>',
        # right arm
        '<line x1="200" y1="140" x2="240" y2="170" stroke="#FF1493" stroke-width="3"/>',
        # left leg
        '<line x1="200" y1="200" x2="160" y2="240" stroke="#FF1493" stroke-width="3"/>',
        # right leg
        '<line x1="200" y1="200" x2="240" y2="240" stroke="#FF1493" stroke-width="3"/>',
    ]
    body_parts = "".join(parts[:wrong])
    bow = '<path d="M188 72 Q200 60 212 72 Q200 84 188 72 Z" fill="#FF69B4" opacity="0.6"/>' if wrong>0 else ""
    return f"""<svg width="300" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect width="300" height="280" fill="#FFF0F5" rx="16"/>
  <!-- gallows -->
  <line x1="60" y1="260" x2="260" y2="260" stroke="#C2547A" stroke-width="4"/>
  <line x1="120" y1="260" x2="120" y2="30" stroke="#C2547A" stroke-width="4"/>
  <line x1="120" y1="30" x2="200" y2="30" stroke="#C2547A" stroke-width="4"/>
  <line x1="200" y1="30" x2="200" y2="65" stroke="#C2547A" stroke-width="4"/>
  {body_parts}{bow}
</svg>"""

def game_hangman():
    init({"hg_word":"","hg_category":"","hg_guessed":[],"hg_wrong":0,
          "hg_done":False,"hg_won":False,"hg_started":False,
          "hg_wins":0,"hg_losses":0,"hg_streak":0,"hg_max_wrong":6,
          "hg_cat_filter":"All"})
    s = st.session_state
    st.markdown("## 🪢 Girly Hangman")
    st.caption("Guess the hidden word letter by letter before she's hanged! 💗")

    cats_hang = ["All"] + sorted(set(c for _,c in HANG_WORDS))
    hcat = st.selectbox("Word category",cats_hang,key="hg_cat")

    c1,c2,c3 = st.columns(3)
    c1.metric("Wins",s.hg_wins); c2.metric("Losses",s.hg_losses); c3.metric("Streak",s.hg_streak)

    def new_hangman():
        pool = [(w,c) for w,c in HANG_WORDS if hcat=="All" or c==hcat]
        word,cat = random.choice(pool)
        s.hg_word=word; s.hg_category=cat
        s.hg_guessed=[]; s.hg_wrong=0
        s.hg_done=False; s.hg_won=False; s.hg_started=True

    if st.button("🌸 New Game",key="hg_new") or not s.hg_started:
        new_hangman(); st.rerun()

    if not s.hg_started: return

    left,right = st.columns([1,1])
    with left:
        st.markdown(hangman_svg(s.hg_wrong),unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#C2547A'>Wrong: {s.hg_wrong}/{s.hg_max_wrong}</p>",unsafe_allow_html=True)

    with right:
        # Word display
        display = " ".join(("_" if c not in s.hg_guessed else c) for c in s.hg_word)
        st.markdown(f"""<div style='text-align:center;margin:20px 0'>
          <div style='font-size:32px;font-weight:700;letter-spacing:12px;color:#FF1493;
                      font-family:Playfair Display,serif'>{display}</div>
          <div style='color:#C2547A;font-size:13px;margin-top:8px'>Category: {s.hg_category}</div>
        </div>""",unsafe_allow_html=True)

        # Wrong letters
        if s.hg_guessed:
            wrong_letters = [l for l in s.hg_guessed if l not in s.hg_word]
            correct_letters = [l for l in s.hg_guessed if l in s.hg_word]
            if wrong_letters:
                wl = " ".join(wrong_letters)
                st.markdown(f"<p style='color:#E91E63'>Wrong guesses: <b>{wl}</b></p>",unsafe_allow_html=True)
            if correct_letters:
                cl = " ".join(correct_letters)
                st.markdown(f"<p style='color:#4CAF50'>Correct: <b>{cl}</b></p>",unsafe_allow_html=True)

        # Check win/loss
        won  = all(c in s.hg_guessed for c in s.hg_word)
        lost = s.hg_wrong >= s.hg_max_wrong
        if won and not s.hg_done:
            s.hg_done=True; s.hg_won=True
            s.hg_wins+=1; s.hg_streak+=1
        if lost and not s.hg_done:
            s.hg_done=True; s.hg_won=False
            s.hg_losses+=1; s.hg_streak=0

        if not s.hg_done:
            # Alphabet buttons (2 rows of 13)
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            rows = [alphabet[:13], alphabet[13:]]
            for row in rows:
                cols = st.columns(len(row))
                for i,letter in enumerate(row):
                    with cols[i]:
                        guessed = letter in s.hg_guessed
                        if guessed:
                            color = "#4CAF50" if letter in s.hg_word else "#E91E63"
                            st.markdown(f'<div style="text-align:center;padding:4px;background:{color};color:white;border-radius:8px;font-weight:700;font-size:12px">{letter}</div>',unsafe_allow_html=True)
                        else:
                            if st.button(letter,key=f"hg_{letter}"):
                                s.hg_guessed.append(letter)
                                if letter not in s.hg_word: s.hg_wrong+=1
                                st.rerun()
        else:
            if s.hg_won:
                st.success(f"🎉 You got it! The word was **{s.hg_word}**! 🌸")
            else:
                st.error(f"💔 Game over! The word was **{s.hg_word}**")
            if st.button("💖 Play Again",key="hg_again"):
                new_hangman(); st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# GAME 4 — Dice Duel (multiplayer: 2-4 players, PvP or PvCPU)
# ════════════════════════════════════════════════════════════════════════════
DICE_FACES = {1:"⚀",2:"⚁",3:"⚂",4:"⚃",5:"⚄",6:"⚅"}

def game_dice_duel():
    init({"dd_players":[],"dd_scores":{},"dd_last_roll":{},"dd_round":0,
          "dd_started":False,"dd_done":False,"dd_target":5,
          "dd_n_humans":2,"dd_n_cpu":0,"dd_current":0})
    s = st.session_state
    st.markdown("## 🎲 Dice Duel — Multiplayer")
    st.caption("Roll dice against friends or CPU — first to the target wins! 👑")

    if not s.dd_started:
        col1,col2,col3 = st.columns(3)
        with col1: n_h = st.selectbox("Human players",  [1,2,3,4], index=1, key="dd_nh")
        with col2: n_c = st.selectbox("CPU players",    [0,1,2,3], index=0, key="dd_nc")
        with col3: tgt = st.selectbox("Wins to win",    [3,5,7,10],index=1, key="dd_tgt")
        if n_h + n_c < 2: st.warning("Need at least 2 players total!"); return
        if n_h + n_c > 4: st.warning("Max 4 players total!"); return

        names = []
        for i in range(n_h):
            nm = st.text_input(f"Player {i+1} name", value=f"Player {i+1}", key=f"dd_name_{i}")
            names.append(nm)
        for i in range(n_c):
            names.append(f"CPU {i+1}")

        if st.button("🌸 Start Game", key="dd_start"):
            s.dd_players   = names
            s.dd_n_humans  = n_h
            s.dd_n_cpu     = n_c
            s.dd_scores    = {p:0 for p in names}
            s.dd_last_roll = {p:0 for p in names}
            s.dd_target    = tgt
            s.dd_round     = 0
            s.dd_current   = 0
            s.dd_started   = True
            s.dd_done      = False
            st.rerun()
        return

    players  = s.dd_players
    n_humans = s.dd_n_humans
    winner   = next((p for p,sc in s.dd_scores.items() if sc>=s.dd_target), None)

    if winner:
        st.balloons()
        st.markdown(f"""<div class='pink-card' style='text-align:center'>
          <h2 style='color:#FF1493'>👑 {winner} WINS THE GAME! 👑</h2>
          <p style='color:#C2547A'>What a dice queen! 🌸</p></div>""",unsafe_allow_html=True)
        cols = st.columns(len(players))
        for i,p in enumerate(players):
            cols[i].metric(p, f"{s.dd_scores[p]} wins")
        if st.button("🔄 Play Again", key="dd_reset"):
            s.dd_started=False; st.rerun()
        return

    # Scoreboard
    st.markdown("**Scoreboard:**")
    cols = st.columns(len(players))
    for i,p in enumerate(players):
        progress_pct = s.dd_scores[p]/s.dd_target
        cols[i].metric(("👑 " if s.dd_scores[p]==max(s.dd_scores.values()) and s.dd_scores[p]>0 else "")+p,
                       f"{s.dd_scores[p]}/{s.dd_target}")

    st.markdown(f"**Round {s.dd_round+1}** — Everyone rolls once per round!")
    st.markdown("---")

    # Each round: all players roll
    round_results = {}
    all_rolled = len(s.dd_last_roll) > 0 and s.dd_round > 0

    roll_cols = st.columns(len(players))
    for i,p in enumerate(players):
        with roll_cols[i]:
            is_cpu = i >= n_humans
            tag    = "🤖" if is_cpu else "🎀"
            st.markdown(f"<p style='text-align:center;font-weight:700;color:#C2547A'>{tag} {p}</p>",unsafe_allow_html=True)
            if p in s.dd_last_roll and s.dd_last_roll[p]>0:
                st.markdown(f"<p style='text-align:center;font-size:50px'>{DICE_FACES[s.dd_last_roll[p]]}</p>",unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;font-weight:700;color:#FF1493;font-size:20px'>{s.dd_last_roll[p]}</p>",unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align:center;font-size:50px'>🎲</p>",unsafe_allow_html=True)

    if st.button("🎲 Roll All Dice!", key=f"dd_roll_{s.dd_round}"):
        rolls = {p: random.randint(1,6) for p in players}
        s.dd_last_roll = rolls
        max_val = max(rolls.values())
        winners_this_round = [p for p,v in rolls.items() if v==max_val]
        if len(winners_this_round)==1:
            s.dd_scores[winners_this_round[0]] += 1
        s.dd_round += 1
        st.rerun()

    if s.dd_last_roll and s.dd_round>0:
        max_val = max(s.dd_last_roll.values())
        rnd_winners = [p for p,v in s.dd_last_roll.items() if v==max_val]
        if len(rnd_winners)==1:
            st.success(f"🌸 **{rnd_winners[0]}** wins this round with a {max_val}! +1 point")
        else:
            st.info(f"🤝 Tie between {', '.join(rnd_winners)} — no point awarded!")

        st.markdown("**Progress to victory:**")
        for p in players:
            pct = min(1., s.dd_scores[p]/s.dd_target)
            st.caption(p)
            st.progress(pct)

# ════════════════════════════════════════════════════════════════════════════
# GAME 5 — Snake Game (canvas via HTML component)
# ════════════════════════════════════════════════════════════════════════════
def game_snake():
    st.markdown("## 🐍 Pink Snake Game")
    st.caption("Use arrow keys or WASD to move! Eat the strawberries! 🍓")

    snake_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body{margin:0;background:#FFF0F5;display:flex;flex-direction:column;align-items:center;
       font-family:'Nunito',sans-serif;padding:10px;}
  canvas{border:3px solid #FF69B4;border-radius:12px;background:#FFF0F5;
         box-shadow:0 4px 18px rgba(255,105,180,.3);}
  #score-bar{display:flex;gap:20px;margin-bottom:10px;font-weight:700;color:#C2547A;font-size:16px;}
  .score-item span{color:#FF1493;font-size:20px;}
  #msg{font-size:18px;font-weight:700;color:#FF1493;margin-top:8px;min-height:28px;}
  button{background:linear-gradient(135deg,#FF69B4,#FF1493);color:white;border:none;
         border-radius:25px;padding:8px 24px;font-size:15px;font-weight:700;cursor:pointer;
         box-shadow:0 4px 12px rgba(255,105,180,.4);margin:6px;}
  button:hover{transform:translateY(-2px);}
  .ctrl-hint{font-size:12px;color:#F48FB1;margin-top:4px;}
</style>
</head>
<body>
<div id="score-bar">
  <div class="score-item">Score: <span id="score">0</span></div>
  <div class="score-item">Best: <span id="best">0</span></div>
  <div class="score-item">Level: <span id="level">1</span></div>
</div>
<canvas id="c" width="400" height="400"></canvas>
<div id="msg">Press Start to play! 🌸</div>
<div><button onclick="startGame()">🌸 Start</button>
     <button onclick="pauseGame()">⏸ Pause</button></div>
<div class="ctrl-hint">Arrow keys or W A S D to move</div>

<script>
const C=document.getElementById('c'), ctx=C.getContext('2d');
const SZ=20, COLS=20, ROWS=20;
let snake,dir,food,score,best=0,running=false,paused=false,loop,speed,level;

function startGame(){
  snake=[{x:10,y:10},{x:9,y:10},{x:8,y:10}];
  dir={x:1,y:0}; score=0; level=1; speed=150;
  placeFood(); running=true; paused=false;
  document.getElementById('msg').textContent='';
  clearInterval(loop); loop=setInterval(tick,speed);
  draw();
}

function pauseGame(){
  if(!running)return;
  paused=!paused;
  document.getElementById('msg').textContent=paused?'Paused ⏸':'';
  if(!paused){clearInterval(loop);loop=setInterval(tick,speed);}
  else clearInterval(loop);
}

function placeFood(){
  do{ food={x:Math.floor(Math.random()*COLS),y:Math.floor(Math.random()*ROWS)};
  }while(snake.some(s=>s.x===food.x&&s.y===food.y));
}

function tick(){
  if(!running||paused)return;
  const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
  // wall collision
  if(head.x<0||head.x>=COLS||head.y<0||head.y>=ROWS){endGame();return;}
  // self collision
  if(snake.some(s=>s.x===head.x&&s.y===head.y)){endGame();return;}
  snake.unshift(head);
  if(head.x===food.x&&head.y===food.y){
    score++;
    document.getElementById('score').textContent=score;
    if(score>best){best=score;document.getElementById('best').textContent=best;}
    if(score%5===0&&speed>60){speed=Math.max(60,speed-15);level++;
      document.getElementById('level').textContent=level;
      clearInterval(loop);loop=setInterval(tick,speed);}
    placeFood();
  } else snake.pop();
  draw();
}

function endGame(){
  running=false; clearInterval(loop);
  document.getElementById('msg').textContent=`💔 Game Over! Score: ${score} — Press Start to retry!`;
}

function draw(){
  ctx.clearRect(0,0,400,400);
  // grid
  ctx.strokeStyle='#FFE4EF'; ctx.lineWidth=0.5;
  for(let i=0;i<=COLS;i++){ctx.beginPath();ctx.moveTo(i*SZ,0);ctx.lineTo(i*SZ,400);ctx.stroke();}
  for(let j=0;j<=ROWS;j++){ctx.beginPath();ctx.moveTo(0,j*SZ);ctx.lineTo(400,j*SZ);ctx.stroke();}

  // food (strawberry)
  ctx.font='16px serif';
  ctx.fillText('🍓',food.x*SZ+2,food.y*SZ+16);

  // snake
  snake.forEach((seg,i)=>{
    const pct=i/snake.length;
    const r=255,g=Math.floor(105+(1-pct)*50),b=Math.floor(180-(1-pct)*60);
    ctx.fillStyle=`rgb(${r},${g},${b})`;
    ctx.beginPath();
    ctx.roundRect(seg.x*SZ+1,seg.y*SZ+1,SZ-2,SZ-2,4);
    ctx.fill();
    if(i===0){// eyes
      ctx.fillStyle='white';
      ctx.beginPath();ctx.arc(seg.x*SZ+6,seg.y*SZ+7,3,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*SZ+14,seg.y*SZ+7,3,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#8B1A4A';
      ctx.beginPath();ctx.arc(seg.x*SZ+6+dir.x,seg.y*SZ+7+dir.y,1.5,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*SZ+14+dir.x,seg.y*SZ+7+dir.y,1.5,0,Math.PI*2);ctx.fill();
    }
  });
}

let nextDir={x:1,y:0};
document.addEventListener('keydown',e=>{
  const k=e.key;
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d'].includes(k))e.preventDefault();
  if((k==='ArrowUp'||k==='w')    &&dir.y!==1) nextDir={x:0,y:-1};
  if((k==='ArrowDown'||k==='s')  &&dir.y!==-1)nextDir={x:0,y:1};
  if((k==='ArrowLeft'||k==='a')  &&dir.x!==1) nextDir={x:-1,y:0};
  if((k==='ArrowRight'||k==='d') &&dir.x!==-1)nextDir={x:1,y:0};
  dir=nextDir;
});

// mobile swipe
let tx=0,ty=0;
C.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY;},{passive:true});
C.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-tx, dy=e.changedTouches[0].clientY-ty;
  if(Math.abs(dx)>Math.abs(dy)){
    if(dx>0&&dir.x!==-1)dir={x:1,y:0}; else if(dx<0&&dir.x!==1)dir={x:-1,y:0};
  } else {
    if(dy>0&&dir.y!==-1)dir={x:0,y:1}; else if(dy<0&&dir.y!==1)dir={x:0,y:-1};
  }
},{passive:true});

draw();
</script>
</body>
</html>
"""
    st.components.v1.html(snake_html, height=560, scrolling=False)

# ════════════════════════════════════════════════════════════════════════════
# GAME 6 — Ludo (2-4 players, PvP or PvCPU)
# ════════════════════════════════════════════════════════════════════════════

# Ludo board path: 52 main squares + home column per color
# Colors: Red(0) Green(1) Yellow(2) Blue(3)
LUDO_COLORS  = ["Red","Green","Yellow","Blue"]
LUDO_HEX     = {"Red":"#E91E63","Green":"#4CAF50","Yellow":"#FFC107","Blue":"#2196F3"}
LUDO_LIGHT   = {"Red":"#FCE4EC","Green":"#E8F5E9","Yellow":"#FFFDE7","Blue":"#E3F2FD"}
# Starting squares on the main path (index into 52-square ring)
LUDO_START   = {"Red":0,"Green":13,"Yellow":26,"Blue":39}
# Safe squares (star positions on real ludo board)
LUDO_SAFE    = {0,8,13,21,26,34,39,47}
# Home column entry square (player must be at this square to enter home column)
LUDO_HOME_ENTRY = {"Red":50,"Green":11,"Yellow":24,"Blue":37}
LUDO_PIECES  = 4  # pieces per player

def ludo_path_pos(color, steps):
    """Return (type, index): type='board'(0-51) or 'home'(0-5) or 'done'"""
    start = LUDO_START[color]
    entry = LUDO_HOME_ENTRY[color]
    # steps from start on the 52-square ring
    pos = (start + steps) % 52
    # once passed entry, enter home column
    steps_to_entry = (entry - start) % 52
    if steps > steps_to_entry:
        home_idx = steps - steps_to_entry - 1  # 0..4 = home column, 5 = done
        if home_idx >= 5:
            return ("done", 0)
        return ("home", home_idx)
    return ("board", pos)

def init_ludo():
    s = st.session_state
    players  = s.ld_players
    n_humans = s.ld_n_humans
    s.ld_pieces = {}
    for p in players:
        s.ld_pieces[p] = [{"steps":0,"out":False,"done":False} for _ in range(LUDO_PIECES)]
    s.ld_current_player = 0
    s.ld_dice_val       = 0
    s.ld_rolled         = False
    s.ld_message        = "Roll the dice to begin!"
    s.ld_winner         = None
    s.ld_consecutive6   = 0

def game_ludo():
    init({"ld_started":False,"ld_players":[],"ld_n_humans":2,"ld_n_cpu":0,
          "ld_pieces":{},"ld_current_player":0,"ld_dice_val":0,
          "ld_rolled":False,"ld_message":"","ld_winner":None,
          "ld_consecutive6":0})
    s = st.session_state
    st.markdown("## 🎯 Ludo — Multiplayer")
    st.caption("Race all 4 pieces home before your opponents! Classic Ludo rules. 👑")

    if not s.ld_started:
        col1,col2 = st.columns(2)
        with col1: n_h = st.selectbox("Human players",[1,2,3,4],index=1,key="ld_nh")
        with col2: n_c = st.selectbox("CPU players",  [0,1,2,3],index=0,key="ld_nc")
        if n_h+n_c<2: st.warning("Need at least 2 players!"); return
        if n_h+n_c>4: st.warning("Max 4 players!"); return

        names=[]
        for i in range(n_h):
            nm = st.text_input(f"Player {i+1} name",value=LUDO_COLORS[i],key=f"ld_name_{i}")
            names.append(nm)
        for i in range(n_c):
            names.append(f"CPU({LUDO_COLORS[n_h+i]})")

        # Assign colors
        color_map = {names[i]: LUDO_COLORS[i] for i in range(len(names))}

        if st.button("🌸 Start Ludo",key="ld_start"):
            s.ld_players   = names
            s.ld_n_humans  = n_h
            s.ld_n_cpu     = n_c
            s.ld_color_map = color_map
            s.ld_started   = True
            init_ludo()
            st.rerun()
        st.markdown("""
        **Rules:**
        - Roll a 6 to bring a piece out of home base
        - Roll a 6 to get an extra turn
        - Land on opponent's piece to send them back to base
        - Safe squares protect your pieces
        - First to get all 4 pieces home wins!
        """)
        return

    if s.ld_winner:
        st.balloons()
        st.success(f"👑 **{s.ld_winner}** wins Ludo! 🌸🎉")
        if st.button("🔄 New Game",key="ld_newgame"):
            s.ld_started=False; st.rerun()
        return

    players    = s.ld_players
    n_humans   = s.ld_n_humans
    cur_idx    = s.ld_current_player
    cur_player = players[cur_idx]
    cur_color  = s.ld_color_map[cur_player]
    is_cpu     = cur_idx >= n_humans

    st.markdown(f"**Current turn:** {'🤖' if is_cpu else '🎀'} **{cur_player}** ({cur_color})")
    st.info(s.ld_message)

    # Scoreboard
    score_cols = st.columns(len(players))
    for i,p in enumerate(players):
        col = s.ld_color_map[p]
        done_count = sum(1 for pc in s.ld_pieces[p] if pc["done"])
        score_cols[i].metric(f"{'🤖' if i>=n_humans else '🎀'} {p}",
                              f"{done_count}/4 home",
                              delta=col)

    # Board visualisation (simplified text board)
    _draw_ludo_board()

    # Dice + actions
    if not s.ld_rolled:
        if is_cpu:
            if st.button("🤖 CPU Rolls",key="ld_cpu_roll"):
                _ludo_roll_and_auto(); st.rerun()
        else:
            if st.button(f"🎲 Roll Dice ({cur_player})",key="ld_roll"):
                _ludo_roll(); st.rerun()
    else:
        st.markdown(f"### Dice: {DICE_FACES[s.ld_dice_val]} = **{s.ld_dice_val}**")
        pieces  = s.ld_pieces[cur_player]
        movable = _get_movable_pieces(cur_player, s.ld_dice_val)

        if not movable:
            st.warning("No movable pieces — turn passes.")
            if st.button("Next Turn ➡️",key="ld_pass"):
                _next_turn(rolled_six=(s.ld_dice_val==6)); st.rerun()
        else:
            if is_cpu:
                # CPU auto-selects best piece
                _cpu_move(cur_player, movable)
                st.rerun()
            else:
                st.markdown("**Choose a piece to move:**")
                cols = st.columns(len(movable))
                for i,(pi,desc) in enumerate(movable):
                    with cols[i]:
                        if st.button(f"Piece {pi+1}\n{desc}",key=f"ld_move_{pi}"):
                            _ludo_move_piece(cur_player, pi, s.ld_dice_val)
                            st.rerun()

def _draw_ludo_board():
    s   = st.session_state
    # Simple ASCII-style board showing piece positions
    board_html = "<div style='font-family:monospace;font-size:12px;background:white;border-radius:12px;padding:12px;border:1.5px solid #FFB6C1;overflow-x:auto'>"
    board_html += "<b>Piece Positions:</b><br>"
    for p in s.ld_players:
        col   = s.ld_color_map[p]
        hexc  = LUDO_HEX[col]
        board_html += f"<span style='color:{hexc};font-weight:700'>{p} ({col})</span>: "
        for i,pc in enumerate(s.ld_pieces[p]):
            if pc["done"]:
                board_html += f"<span style='background:#E8F5E9;padding:2px 6px;border-radius:6px;margin:2px;color:#2E7D32'>P{i+1}:HOME</span>"
            elif not pc["out"]:
                board_html += f"<span style='background:#FFF0F5;padding:2px 6px;border-radius:6px;margin:2px;color:#F48FB1'>P{i+1}:BASE</span>"
            else:
                typ, idx = ludo_path_pos(col, pc["steps"])
                pos_str  = f"sq{idx}" if typ=="board" else (f"H{idx+1}" if typ=="home" else "DONE")
                board_html += f"<span style='background:{LUDO_LIGHT[col]};padding:2px 6px;border-radius:6px;margin:2px;color:{LUDO_HEX[col]}'>{pos_str}</span>"
        board_html += "<br>"
    board_html += "</div>"
    st.markdown(board_html, unsafe_allow_html=True)

def _get_movable_pieces(player, dice):
    s      = st.session_state
    col    = s.ld_color_map[player]
    pieces = s.ld_pieces[player]
    movable = []
    for i,pc in enumerate(pieces):
        if pc["done"]: continue
        if not pc["out"]:
            if dice==6: movable.append((i,"Bring out"))
        else:
            new_steps = pc["steps"] + dice
            typ,idx   = ludo_path_pos(col, new_steps)
            if typ=="done" or typ=="home" or typ=="board":
                # Check won't overshoot home
                steps_to_entry = (LUDO_HOME_ENTRY[col] - LUDO_START[col]) % 52
                if pc["steps"] > steps_to_entry:
                    home_remaining = 5 - (pc["steps"] - steps_to_entry - 1)
                    if dice > home_remaining: continue  # overshoot
                movable.append((i,f"Move +{dice}"))
    return movable

def _ludo_roll():
    s = st.session_state
    val = random.randint(1,6)
    s.ld_dice_val = val
    s.ld_rolled   = True
    if val==6: s.ld_consecutive6+=1
    else:       s.ld_consecutive6=0
    if s.ld_consecutive6>=3:
        s.ld_message  = "Three 6s in a row! Turn forfeited."
        s.ld_consecutive6=0
        _next_turn(rolled_six=False)
    else:
        cur = s.ld_players[s.ld_current_player]
        s.ld_message = f"{cur} rolled a {val}!"

def _ludo_roll_and_auto():
    _ludo_roll()
    s = st.session_state
    if s.ld_rolled and s.ld_consecutive6<3:
        cur     = s.ld_players[s.ld_current_player]
        movable = _get_movable_pieces(cur, s.ld_dice_val)
        if movable:
            _cpu_move(cur, movable)
        else:
            _next_turn(rolled_six=(s.ld_dice_val==6))

def _cpu_move(player, movable):
    s   = st.session_state
    col = s.ld_color_map[player]
    # Strategy: prefer capture > bring home > advance furthest
    best = None
    for pi, desc in movable:
        pc = s.ld_pieces[player][pi]
        if not pc["out"]:
            best = (pi, desc); break  # bring out on 6
    if best is None:
        # prefer piece closest to home
        best = max(movable, key=lambda x: s.ld_pieces[player][x[0]]["steps"])
    _ludo_move_piece(player, best[0], s.ld_dice_val)

def _ludo_move_piece(player, piece_idx, dice):
    s   = st.session_state
    col = s.ld_color_map[player]
    pc  = s.ld_pieces[player][piece_idx]

    if not pc["out"]:
        pc["out"]   = True
        pc["steps"] = 0
        s.ld_message = f"{player} brought Piece {piece_idx+1} out!"
    else:
        pc["steps"] += dice
        typ, idx     = ludo_path_pos(col, pc["steps"])
        if typ=="done":
            pc["done"]   = True
            s.ld_message = f"{player}'s Piece {piece_idx+1} reached HOME! 🎉"
        elif typ=="home":
            s.ld_message = f"{player}'s Piece {piece_idx+1} is in home column (step {idx+1})"
        else:
            board_sq = idx
            s.ld_message = f"{player}'s Piece {piece_idx+1} moved to square {board_sq}"
            # Capture check
            if board_sq not in LUDO_SAFE:
                for other_p in s.ld_players:
                    if other_p==player: continue
                    other_col = s.ld_color_map[other_p]
                    for opc in s.ld_pieces[other_p]:
                        if not opc["out"] or opc["done"]: continue
                        otyp,oidx = ludo_path_pos(other_col, opc["steps"])
                        if otyp=="board" and oidx==board_sq:
                            opc["out"]   = False
                            opc["steps"] = 0
                            s.ld_message += f" — captured {other_p}'s piece! 💥"

    # Check winner
    if all(p["done"] for p in s.ld_pieces[player]):
        s.ld_winner = player
        return

    _next_turn(rolled_six=(dice==6))

def _next_turn(rolled_six):
    s = st.session_state
    s.ld_rolled = False
    if not rolled_six:
        s.ld_current_player = (s.ld_current_player+1) % len(s.ld_players)
    # If CPU's turn, auto-proceed signal (handled in UI)

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR & MAIN
# ════════════════════════════════════════════════════════════════════════════
def main():
    with st.sidebar:
        st.markdown("# 💖 Lucky Girl Games")
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
            "🎰 Lottery Guess": "Guess the number!\nHot/cold hints & streaks 🔥",
            "🌸 Pink Trivia":   "No question repeats!\nFilter by category 💅",
            "🪢 Hangman":       "Guess letters!\n6 wrong = game over 💔",
            "🎲 Dice Duel":     "2–4 players!\nPvP or vs CPU 🤖",
            "🐍 Snake Game":    "Arrow keys / WASD\nEat strawberries! 🍓",
            "🎯 Ludo":          "2–4 players, PvP/CPU\nRoll 6 to start! 🎯",
        }
        st.caption(tips.get(game,""))
        st.markdown("---")
        st.caption("made with 💗 & Python")

    st.markdown("<h1>💖 Lucky Girl Games 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#F48FB1'>your favourite girly game hub ✨</p>", unsafe_allow_html=True)
    st.divider()

    if   game == "🎰 Lottery Guess": game_lottery()
    elif game == "🌸 Pink Trivia":   game_trivia()
    elif game == "🪢 Hangman":       game_hangman()
    elif game == "🎲 Dice Duel":     game_dice_duel()
    elif game == "🐍 Snake Game":    game_snake()
    elif game == "🎯 Ludo":          game_ludo()

if __name__ == "__main__":
    main()
