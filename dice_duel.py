# -*- coding: utf-8 -*-
"""games/dice_duel.py — TP Games: Dice Duel Multiplayer"""
import random
import streamlit as st
from theme import init, reset_game, dice_svg

PLAYER_COLORS = ["#E91E63","#4CAF50","#2196F3","#FF9800"]
PLAYER_ICONS  = ["🎀","🌟","💎","🔥"]

def run():
    init({"dd_players":[],"dd_scores":{},"dd_types":{},"dd_last_roll":{},
          "dd_round":0,"dd_started":False,"dd_target":5})
    s = st.session_state

    st.markdown("## 🎲 Dice Duel")
    st.caption("Everyone rolls — highest roll wins the round. First to the target wins!")

    if not s.dd_started:
        _setup_screen()
        return

    players = s.dd_players
    winner  = next((p for p,sc in s.dd_scores.items() if sc >= s.dd_target), None)

    if winner:
        st.balloons()
        idx = players.index(winner)
        st.markdown(
            f'<div class="tp-card" style="text-align:center;padding:32px">'
            f'<div style="font-size:48px">{PLAYER_ICONS[idx]}</div>'
            f'<h2 style="color:{PLAYER_COLORS[idx]}">{winner} WINS THE GAME!</h2>'
            f'<p style="color:#C2547A">What a champion!</p>'
            f'</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play Again", key="dd_again"):
                s.dd_scores  = {p:0 for p in players}
                s.dd_last_roll = {}; s.dd_round = 0; st.rerun()
        with col2:
            if st.button("Change Players", key="dd_change"):
                reset_game("dd_"); st.rerun()
        # Final scoreboard
        st.divider()
        cols = st.columns(len(players))
        for i,p in enumerate(players):
            cols[i].metric(PLAYER_ICONS[i]+" "+p, f"{s.dd_scores[p]}/{s.dd_target}")
        return

    # ── Scoreboard ──
    st.markdown(f"**Round {s.dd_round+1}** — First to **{s.dd_target}** round wins!")
    cols = st.columns(len(players))
    for i,p in enumerate(players):
        is_leading = s.dd_scores[p] == max(s.dd_scores.values()) and s.dd_scores[p]>0
        label = ("👑 " if is_leading else PLAYER_ICONS[i]+" ") + p
        cols[i].metric(label, f"{s.dd_scores[p]}/{s.dd_target}")

    # Progress bars
    for i,p in enumerate(players):
        pct = s.dd_scores[p] / s.dd_target
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin:3px 0">'
            f'<span style="width:90px;font-size:12px;color:{PLAYER_COLORS[i]};font-weight:700">{PLAYER_ICONS[i]} {p}</span>'
            f'<div style="flex:1;background:#3D1E34;border-radius:99px;height:8px">'
            f'<div style="width:{int(pct*100)}%;background:{PLAYER_COLORS[i]};height:8px;border-radius:99px;transition:width .4s"></div>'
            f'</div><span style="font-size:12px;color:#8B3060">{s.dd_scores[p]}/{s.dd_target}</span></div>',
            unsafe_allow_html=True)

    st.divider()

    # ── Dice display ──
    roll_cols = st.columns(len(players))
    for i,p in enumerate(players):
        with roll_cols[i]:
            tag  = "🤖 CPU" if s.dd_types.get(p)=="cpu" else PLAYER_ICONS[i]
            st.markdown(
                f'<p style="text-align:center;font-weight:700;color:{PLAYER_COLORS[i]};font-size:14px">'
                f'{tag}<br>{p}</p>', unsafe_allow_html=True)
            if p in s.dd_last_roll:
                v = s.dd_last_roll[p]
                st.markdown(f'<div style="text-align:center">{dice_svg(v,72)}</div>', unsafe_allow_html=True)
                st.markdown(f'<p style="text-align:center;font-size:22px;font-weight:800;color:{PLAYER_COLORS[i]}">{v}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="text-align:center;font-size:52px">🎲</p>', unsafe_allow_html=True)

    if st.button("Roll All Dice!", key=f"dd_roll_{s.dd_round}"):
        rolls  = {p: random.randint(1,6) for p in players}
        s.dd_last_roll = rolls
        max_v  = max(rolls.values())
        winners = [p for p,v in rolls.items() if v==max_v]
        if len(winners)==1: s.dd_scores[winners[0]] += 1
        s.dd_round += 1
        st.rerun()

    if s.dd_last_roll and s.dd_round > 0:
        max_v    = max(s.dd_last_roll.values())
        rnd_wins = [p for p,v in s.dd_last_roll.items() if v==max_v]
        if len(rnd_wins)==1:
            idx = players.index(rnd_wins[0])
            st.success(f"{PLAYER_ICONS[idx]} **{rnd_wins[0]}** wins this round with a {max_v}! +1 point")
        else:
            st.info(f"Tie between {', '.join(rnd_wins)} — no point awarded!")

    col1, _ = st.columns([1,3])
    with col1:
        if st.button("Reset Game", key="dd_reset"):
            reset_game("dd_"); st.rerun()


def _setup_screen():
    st.markdown(
        '<div class="tp-card" style="padding:24px">'
        '<h3 style="color:#FF69B4;margin-top:0">Game Setup</h3>'
        '<p style="color:#C2547A;font-size:13px">Configure players, then hit Start!</p>'
        '</div>', unsafe_allow_html=True)

    total_players = st.slider("Total number of players", 2, 4, 2, key="dd_total")
    target        = st.select_slider("Rounds needed to win", [3,5,7,10], value=5, key="dd_tgt_s")

    st.markdown("**Configure each player:**")
    player_configs = []
    for i in range(total_players):
        col_icon, col_name, col_type = st.columns([1,3,2])
        with col_icon:
            st.markdown(
                f'<div style="background:{PLAYER_COLORS[i]};width:40px;height:40px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-size:20px;margin-top:8px">'
                f'{PLAYER_ICONS[i]}</div>', unsafe_allow_html=True)
        with col_name:
            name = st.text_input(
                f"Name", value=f"Player {i+1}",
                key=f"dd_cfg_name_{i}", label_visibility="collapsed")
        with col_type:
            ptype = st.selectbox(
                "Type", ["Human", "Computer"],
                key=f"dd_cfg_type_{i}", label_visibility="collapsed")
        player_configs.append((name.strip() or f"Player {i+1}", ptype.lower()[:5]))

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Dice Duel!", key="dd_start"):
        names  = [c[0] for c in player_configs]
        types  = {c[0]: ("cpu" if c[1]=="compu" else "human") for c in player_configs}
        st.session_state.dd_players   = names
        st.session_state.dd_types     = types
        st.session_state.dd_scores    = {p:0 for p in names}
        st.session_state.dd_last_roll = {}
        st.session_state.dd_target    = target
        st.session_state.dd_round     = 0
        st.session_state.dd_started   = True
        st.rerun()
