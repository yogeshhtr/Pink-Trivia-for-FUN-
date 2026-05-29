# -*- coding: utf-8 -*-
"""games/ludo.py — TP Games: Ludo  (HTML5 canvas, click-to-move)"""
import random
import json
import streamlit as st
from theme import init, reset_game, LUDO_HEX, LUDO_DARK, LUDO_LIGHT

# ── Constants ────────────────────────────────────────────────────────────────
COLORS       = ["Red", "Green", "Yellow", "Blue"]
COLOR_ICONS  = {"Red":"🔴","Green":"🟢","Yellow":"🟡","Blue":"🔵"}
PLAYER_ICONS = ["🎀","🌟","💎","🔥"]
START_SQ     = {"Red":0,"Green":13,"Yellow":26,"Blue":39}
HOME_ENTRY   = {"Red":50,"Green":11,"Yellow":24,"Blue":37}
SAFE_SQ      = {0,8,13,21,26,34,39,47}

def path_pos(color: str, steps: int):
    """Return (type, index): 'board'|'home'|'done'."""
    start          = START_SQ[color]
    entry          = HOME_ENTRY[color]
    steps_to_entry = (entry - start) % 52
    if steps > steps_to_entry:
        hi = steps - steps_to_entry - 1
        return ("done", 0) if hi >= 5 else ("home", hi)
    return ("board", (start + steps) % 52)

def init_ludo_state():
    s = st.session_state
    s.ld_pieces = {
        p: [{"steps":0,"out":False,"done":False} for _ in range(4)]
        for p in s.ld_players
    }
    s.ld_current = 0
    s.ld_dice    = 0
    s.ld_rolled  = False
    s.ld_message = "Roll the dice to begin!"
    s.ld_winner  = None
    s.ld_consec6 = 0
    s.ld_movable = []

def get_movable(player: str, dice: int):
    s   = st.session_state
    col = s.ld_color_map[player]
    out = []
    for i, pc in enumerate(s.ld_pieces[player]):
        if pc["done"]: continue
        if not pc["out"]:
            if dice == 6: out.append(i)
        else:
            ste = (HOME_ENTRY[col] - START_SQ[col]) % 52
            if pc["steps"] > ste:
                hr = 5 - (pc["steps"] - ste - 1)
                if dice > hr: continue
            out.append(i)
    return out

def do_move(player: str, pi: int, dice: int):
    s   = st.session_state
    col = s.ld_color_map[player]
    pc  = s.ld_pieces[player][pi]
    if not pc["out"]:
        pc["out"] = True; pc["steps"] = 0
        s.ld_message = f"{player} brought piece {pi+1} out of base!"
    else:
        pc["steps"] += dice
        typ, idx = path_pos(col, pc["steps"])
        if typ == "done":
            pc["done"] = True
            s.ld_message = f"{player}'s piece {pi+1} reached HOME!"
        elif typ == "home":
            s.ld_message = f"{player}'s piece {pi+1} → home column step {idx+1}"
        else:
            s.ld_message = f"{player}'s piece {pi+1} → square {idx}"
            if idx not in SAFE_SQ:
                for op in s.ld_players:
                    if op == player: continue
                    oc = s.ld_color_map[op]
                    for opc in s.ld_pieces[op]:
                        if not opc["out"] or opc["done"]: continue
                        ot, oi = path_pos(oc, opc["steps"])
                        if ot == "board" and oi == idx:
                            opc["out"] = False; opc["steps"] = 0
                            s.ld_message += f" — captured {op}'s piece!"
    if all(p["done"] for p in s.ld_pieces[player]):
        s.ld_winner = player; return
    _next_turn(dice == 6)

def _next_turn(extra: bool):
    s = st.session_state
    s.ld_rolled  = False
    s.ld_movable = []
    if not extra:
        s.ld_current = (s.ld_current + 1) % len(s.ld_players)

def do_roll():
    s   = st.session_state
    val = random.randint(1, 6)
    s.ld_dice   = val
    s.ld_rolled = True
    if val == 6: s.ld_consec6 += 1
    else:         s.ld_consec6  = 0
    if s.ld_consec6 >= 3:
        s.ld_message  = "Three 6s in a row! Turn forfeited."
        s.ld_consec6  = 0
        s.ld_rolled   = False
        _next_turn(False)
        return
    cur     = s.ld_players[s.ld_current]
    movable = get_movable(cur, val)
    s.ld_movable = movable
    s.ld_message = f"{cur} rolled {val}!"
    if not movable:
        s.ld_message += " — No valid moves. Turn passes."
        _next_turn(val == 6)

def cpu_auto():
    s   = st.session_state
    cur = s.ld_players[s.ld_current]
    if not s.ld_rolled:
        do_roll()
    if s.ld_rolled and s.ld_movable:
        out_p = [i for i in s.ld_movable if s.ld_pieces[cur][i]["out"]]
        in_p  = [i for i in s.ld_movable if not s.ld_pieces[cur][i]["out"]]
        if out_p:
            best = max(out_p, key=lambda i: s.ld_pieces[cur][i]["steps"])
        else:
            best = in_p[0]
        do_move(cur, best, s.ld_dice)

# ── Board path mapping (52 squares → row,col on 15×15 grid) ─────────────────
_PATH = [
    (14,6),(13,6),(12,6),(11,6),(10,6),(9,6),
    (8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
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
_HOME_COLS = {
    "Red":    [(13,7),(12,7),(11,7),(10,7),(9,7)],
    "Green":  [(7,1),(7,2),(7,3),(7,4),(7,5)],
    "Yellow": [(1,7),(2,7),(3,7),(4,7),(5,7)],
    "Blue":   [(7,13),(7,12),(7,11),(7,10),(7,9)],
}
_BASE_OFFSETS = [(1,1),(2,1),(1,2),(2,2)]
_BASE_ORIGINS = {"Red":(1,1),"Green":(1,9),"Yellow":(9,9),"Blue":(9,1)}

def _build_ludo_html(pieces_state, color_map, players, n_humans,
                     rolled, dice_val, movable_indices, cur_idx, message):
    """Return a self-contained HTML page with the Ludo board and JS click handler."""

    CS  = 40    # cell size px
    BSZ = 15*CS # 600px

    # ── Serialise state for JS ──────────────────────────────────────────────
    js_pieces = {}
    for p in players:
        col = color_map[p]
        js_pieces[p] = []
        for pi, pc in enumerate(pieces_state[p]):
            # Compute pixel centre of piece
            if pc["done"]:
                cx = 7*CS+CS//2 + (pi%2-1)*14
                cy = 7*CS+CS//2 + (pi//2-1)*14
            elif not pc["out"]:
                br, bc = _BASE_ORIGINS[col]
                dr, dc = _BASE_OFFSETS[pi]
                r2 = br+dr; c2 = bc+dc
                cx = c2*CS+CS//2; cy = r2*CS+CS//2
            else:
                ste = (HOME_ENTRY[col]-START_SQ[col])%52
                if pc["steps"] > ste:
                    hidx = pc["steps"]-ste-1
                    if hidx < 5:
                        r2,c2 = _HOME_COLS[col][hidx]
                    else:
                        r2,c2 = (7,7)
                else:
                    bidx = (START_SQ[col]+pc["steps"])%52
                    r2,c2 = _PATH[bidx] if bidx<len(_PATH) else (7,7)
                cx = c2*CS+CS//2; cy = r2*CS+CS//2

            is_movable = (pi in movable_indices) and (players[cur_idx]==p)
            js_pieces[p].append({
                "idx":pi,"cx":cx,"cy":cy,
                "color":LUDO_HEX[col],"dark":LUDO_DARK[col],
                "out":pc["out"],"done":pc["done"],"movable":is_movable,
                "player":p,"pieceIdx":pi
            })

    pieces_json = json.dumps(js_pieces)
    players_json= json.dumps(players)

    # Build color map for JS
    col_map_js  = json.dumps({p: color_map[p] for p in players})
    hex_map_js  = json.dumps(LUDO_HEX)

    cur_player  = players[cur_idx]
    cur_color   = color_map[cur_player]
    cur_hex     = LUDO_HEX[cur_color]
    is_cpu      = cur_idx >= n_humans

    # Dice SVG dots
    DICE_DOTS = {
        1:"25,25",
        2:"13,13 37,37",
        3:"13,13 25,25 37,37",
        4:"13,13 37,13 13,37 37,37",
        5:"13,13 37,13 25,25 13,37 37,37",
        6:"13,10 37,10 13,25 37,25 13,40 37,40",
    }
    dice_dots_str = ""
    if dice_val > 0:
        for xy in DICE_DOTS.get(dice_val,"").split(" "):
            if xy:
                x,y = xy.split(",")
                dice_dots_str += f'<circle cx="{x}" cy="{y}" r="4" fill="#FF1493"/>'

    # Safe-square set for JS highlighting
    safe_js = json.dumps(list(SAFE_SQ))

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:#1A0A12;font-family:'Nunito',sans-serif;color:#F8D7E8;
  display:flex;flex-direction:column;align-items:center;padding:8px;}}
#board-wrap{{position:relative;}}
canvas{{border:2px solid #8B2050;border-radius:10px;
  box-shadow:0 0 24px rgba(255,20,147,.3);cursor:pointer;}}
#info{{width:{BSZ}px;margin-top:10px;}}
#msg-bar{{background:#2D1224;border:1px solid #8B2050;border-radius:8px;
  padding:8px 14px;font-size:13px;color:#F8D7E8;margin-bottom:8px;}}
#dice-area{{display:flex;align-items:center;gap:12px;}}
#dice-svg{{flex-shrink:0;}}
#action-hint{{font-size:12px;color:#8B3060;font-style:italic;}}
.piece-btn{{background:linear-gradient(135deg,#8B2050,#FF1493);color:white;
  border:none;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:700;
  cursor:pointer;margin:3px;text-transform:uppercase;letter-spacing:1px;}}
.piece-btn:hover{{box-shadow:0 0 10px rgba(255,20,147,.5);}}
#movable-btns{{margin-top:6px;display:flex;flex-wrap:wrap;gap:4px;}}
#turn-tag{{display:inline-block;background:{cur_hex};color:white;border-radius:6px;
  padding:3px 12px;font-size:12px;font-weight:700;margin-bottom:6px;}}
</style>
</head>
<body>
<div id="board-wrap"><canvas id="cv" width="{BSZ}" height="{BSZ}"></canvas></div>
<div id="info">
  <div id="turn-tag">{COLOR_ICONS.get(cur_color,"")} {cur_player}'s turn ({cur_color})</div>
  <div id="msg-bar">{message}</div>
  <div id="dice-area">
    <svg id="dice-svg" width="52" height="52" viewBox="0 0 50 50">
      <rect width="50" height="50" rx="10" fill="#2D1224" stroke="{cur_hex}" stroke-width="2"/>
      {dice_dots_str if dice_val>0 else '<text x="25" y="32" text-anchor="middle" font-size="20" fill="#8B3060">?</text>'}
    </svg>
    <div>
      <div id="action-hint">{'Click a glowing piece to move it' if rolled and movable_indices else ('Roll the dice first!' if not rolled else 'No valid moves — passing turn')}</div>
      <div id="movable-btns"></div>
    </div>
  </div>
</div>

<script>
const cv  = document.getElementById('cv');
const ctx = cv.getContext('2d');
const CS  = {CS};
const BSZ = {BSZ};
const pieces   = {pieces_json};
const players  = {players_json};
const colorMap = {col_map_js};
const hexMap   = {hex_map_js};
const safeSq   = new Set({safe_js});
const rolled   = {'true' if rolled else 'false'};
const diceVal  = {dice_val};
const movableIdx = {json.dumps(movable_indices)};
const curPlayer  = {json.dumps(cur_player)};
const isCpu      = {'true' if is_cpu else 'false'};

// ── Board drawing ────────────────────────────────────────────────────────
function cellFill(r,c){{
  if(r<6&&c<6)   return '#3A0810';
  if(r<6&&c>8)   return '#0A2A10';
  if(r>8&&c<6)   return '#0A1A3A';
  if(r>8&&c>8)   return '#2A1800';
  if(6<=r&&r<=8&&6<=c&&c<=8) return '#2D1224';
  if(c===6&&r>=1&&r<=5) return '#3A0810';
  if(r===7&&c>=1&&c<=5) return '#0A2A10';
  if(c===8&&r>=1&&r<=5) return '#2A1800';
  if(r===7&&c>=9&&c<=13) return '#0A1A3A';
  if(c===7&&r>=9&&r<=13) return '#3A0810';
  if(c===7&&r>=1&&r<=5)  return '#2A1800';
  return '#1E0E1A';
}}

function drawBoard(){{
  ctx.clearRect(0,0,BSZ,BSZ);
  // Cells
  for(let r=0;r<15;r++){{
    for(let c=0;c<15;c++){{
      ctx.fillStyle=cellFill(r,c);
      ctx.fillRect(c*CS,r*CS,CS,CS);
      ctx.strokeStyle='rgba(139,32,80,.3)';
      ctx.lineWidth=0.5;
      ctx.strokeRect(c*CS,r*CS,CS,CS);
    }}
  }}
  // Safe star squares
  const path = {json.dumps(_PATH)};
  safeSq.forEach(sq=>{{
    if(sq<path.length){{
      const [r,c]=path[sq];
      ctx.fillStyle='rgba(255,215,0,.12)';
      ctx.fillRect(c*CS,r*CS,CS,CS);
      ctx.fillStyle='rgba(255,215,0,.5)';
      ctx.font='bold 16px serif';
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText('★',c*CS+CS/2,r*CS+CS/2);
    }}
  }});
  // Colored home zones
  const zones=[
    ['Red',1,1],['Green',1,9],['Yellow',9,9],['Blue',9,1]
  ];
  zones.forEach(([col,r0,c0])=>{{
    const hx=hexMap[col];
    ctx.fillStyle=hx+'22';
    ctx.beginPath();
    roundRect(ctx,c0*CS+2,r0*CS+2,4*CS-4,4*CS-4,10);
    ctx.fill();
    ctx.strokeStyle=hx+'66';ctx.lineWidth=2;
    ctx.beginPath();roundRect(ctx,c0*CS+CS/2,r0*CS+CS/2,3*CS,3*CS,8);ctx.stroke();
  }});
  // Center triangles
  const cx=7*CS+CS/2, cy=7*CS+CS/2, h=CS*1.5;
  [['Red',-1,-1],['Green',1,-1],['Yellow',1,1],['Blue',-1,1]].forEach(([col,sx,sy])=>{{
    ctx.fillStyle=hexMap[col]+'BB';
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.lineTo(cx+sx*h,cy+sy*h);
    ctx.lineTo(cx+(sy)*h,cy+(-sx)*h);
    ctx.closePath();ctx.fill();
  }});
  // Home column colouring
  const homeCols = {json.dumps({k:v for k,v in _HOME_COLS.items()})};
  Object.entries(homeCols).forEach(([col,cells])=>{{
    cells.forEach(([r,c])=>{{
      ctx.fillStyle=hexMap[col]+'44';
      ctx.fillRect(c*CS,r*CS,CS,CS);
    }});
  }});
}}

function roundRect(ctx,x,y,w,h,r){{
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);
  ctx.closePath();
}}

function drawPieces(){{
  const cellCounts={{}};
  Object.values(pieces).flat().forEach(pc=>{{
    const key=pc.cx+','+pc.cy;
    cellCounts[key]=(cellCounts[key]||0)+1;
  }});
  const drawn={{}};
  Object.values(pieces).flat().forEach(pc=>{{
    const key=pc.cx+','+pc.cy;
    drawn[key]=(drawn[key]||0);
    const cnt=drawn[key]; drawn[key]++;
    const total=cellCounts[key];
    // offset pieces sharing a cell
    let ox=0,oy=0;
    if(total>1){{
      const offsets=[[-8,-8],[8,-8],[-8,8],[8,8]];
      ox=offsets[cnt%4][0]; oy=offsets[cnt%4][1];
    }}
    const x=pc.cx+ox, y=pc.cy+oy, R=pc.movable?14:12;
    // Glow for movable
    if(pc.movable){{
      ctx.save();
      ctx.shadowColor=pc.color;ctx.shadowBlur=18;
      ctx.beginPath();ctx.arc(x,y,R+3,0,Math.PI*2);
      ctx.fillStyle=pc.color+'44';ctx.fill();
      ctx.restore();
    }}
    // Piece circle
    const grad=ctx.createRadialGradient(x-3,y-3,2,x,y,R);
    grad.addColorStop(0,'#fff');
    grad.addColorStop(0.3,pc.color);
    grad.addColorStop(1,pc.dark);
    ctx.beginPath();ctx.arc(x,y,R,0,Math.PI*2);
    ctx.fillStyle=grad;ctx.fill();
    ctx.strokeStyle=pc.movable?'#FFD700':pc.dark;
    ctx.lineWidth=pc.movable?2.5:1.5;ctx.stroke();
    // Number label
    ctx.fillStyle='white';
    ctx.font='bold 11px Nunito,sans-serif';
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(pc.pieceIdx+1,x,y);
  }});
}}

function render(){{ drawBoard(); drawPieces(); }}
render();

// ── Click to move ─────────────────────────────────────────────────────────
cv.addEventListener('click', e=>{{
  if(!rolled||isCpu) return;
  const rect=cv.getBoundingClientRect();
  const mx=e.clientX-rect.left, my=e.clientY-rect.top;
  const allPieces=Object.values(pieces).flat();
  const cellCounts={{}};
  allPieces.forEach(pc=>{{const k=pc.cx+','+pc.cy;cellCounts[k]=(cellCounts[k]||0)+1;}});
  const drawn={{}};
  allPieces.forEach(pc=>{{
    const key=pc.cx+','+pc.cy;
    drawn[key]=(drawn[key]||0);
    const cnt=drawn[key]; drawn[key]++;
    const total=cellCounts[key];
    let ox=0,oy=0;
    if(total>1){{const offs=[[-8,-8],[8,-8],[-8,8],[8,8]];ox=offs[cnt%4][0];oy=offs[cnt%4][1];}}
    const x=pc.cx+ox, y=pc.cy+oy;
    const dist=Math.hypot(mx-x,my-y);
    if(dist<=16 && pc.movable && pc.player===curPlayer){{
      // Send choice back to Streamlit via query param trick
      const url=new URL(window.location.href);
      url.searchParams.set('ludo_move',''+pc.pieceIdx);
      window.parent.postMessage({{type:'streamlit:setComponentValue',value:pc.pieceIdx}},'*');
    }}
  }});
}});

// Pulse animation for movable pieces
let pulse=0;
function animate(){{
  render();
  // draw pulsing ring on movable pieces
  const allPieces=Object.values(pieces).flat().filter(p=>p.movable&&p.player===curPlayer);
  const t=Date.now()/600;
  allPieces.forEach(pc=>{{
    const r=16+4*Math.sin(t*Math.PI);
    ctx.beginPath();ctx.arc(pc.cx,pc.cy,r,0,Math.PI*2);
    ctx.strokeStyle='rgba(255,215,0,'+(.5+.4*Math.sin(t*Math.PI))+')';
    ctx.lineWidth=2;ctx.stroke();
  }});
  requestAnimationFrame(animate);
}}
animate();
</script>
</body>
</html>"""


def run():
    init({"ld_started":False,"ld_players":[],"ld_n_humans":2,
          "ld_pieces":{},"ld_current":0,"ld_dice":0,"ld_rolled":False,
          "ld_message":"Roll the dice to begin!","ld_winner":None,
          "ld_consec6":0,"ld_color_map":{},"ld_movable":[],"ld_move_flag":-1})
    s = st.session_state

    st.markdown("## 🎯 Ludo")

    # ── Setup screen ────────────────────────────────────────────────────────
    if not s.ld_started:
        _setup_screen(); return

    # ── Winner ──────────────────────────────────────────────────────────────
    if s.ld_winner:
        st.balloons()
        widx = s.ld_players.index(s.ld_winner)
        st.markdown(
            f'<div class="tp-card" style="text-align:center;padding:32px">'
            f'<div style="font-size:52px">{PLAYER_ICONS[widx]}</div>'
            f'<h2 style="color:{LUDO_HEX[s.ld_color_map[s.ld_winner]]}">'
            f'{s.ld_winner} WINS!</h2></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play Again", key="ld_again"):
                init_ludo_state(); st.rerun()
        with col2:
            if st.button("Change Players", key="ld_change"):
                reset_game("ld_"); st.rerun()
        return

    players   = s.ld_players
    n_humans  = s.ld_n_humans
    cur_idx   = s.ld_current
    cur_player= players[cur_idx]
    cur_color = s.ld_color_map[cur_player]
    is_cpu    = cur_idx >= n_humans

    # ── Scoreboard strip ────────────────────────────────────────────────────
    scols = st.columns(len(players))
    for i, p in enumerate(players):
        col   = s.ld_color_map[p]
        done  = sum(1 for pc in s.ld_pieces[p] if pc["done"])
        hexc  = LUDO_HEX[col]
        bar   = "█"*done + "░"*(4-done)
        active= "border: 1px solid #FFD700;" if i==cur_idx else ""
        scols[i].markdown(
            f'<div style="background:#2D1224;border-radius:8px;padding:8px;text-align:center;{active}">'
            f'<div style="color:{hexc};font-weight:800;font-size:13px">{PLAYER_ICONS[i]} {p}</div>'
            f'<div style="color:{hexc};font-family:monospace;font-size:14px;letter-spacing:1px">{bar}</div>'
            f'<div style="color:#8B3060;font-size:11px">{done}/4 home</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Board + controls layout ──────────────────────────────────────────────
    board_col, ctrl_col = st.columns([3, 2])

    with board_col:
        html = _build_ludo_html(
            s.ld_pieces, s.ld_color_map, players, n_humans,
            s.ld_rolled, s.ld_dice, s.ld_movable, cur_idx, s.ld_message)
        st.components.v1.html(html, height=760, scrolling=False)

    with ctrl_col:
        st.markdown(f"**{PLAYER_ICONS[cur_idx]} {cur_player}'s Turn**")
        st.caption(f"Color: {cur_color}  {'(Computer)' if is_cpu else '(You)'}")

        # Dice display
        from theme import dice_svg
        if s.ld_dice > 0:
            st.markdown(
                f'<div style="text-align:center;margin:10px 0">'
                f'{dice_svg(s.ld_dice, 72)}'
                f'<p style="font-size:28px;font-weight:800;color:#FF1493;margin:4px 0">{s.ld_dice}</p>'
                f'</div>', unsafe_allow_html=True)

        st.info(s.ld_message)

        if not s.ld_rolled:
            if is_cpu:
                if st.button("Let CPU Play", key="ld_cpu"):
                    cpu_auto(); st.rerun()
            else:
                if st.button("Roll Dice", key="ld_roll"):
                    do_roll(); st.rerun()
        else:
            movable = s.ld_movable
            if not movable:
                if st.button("Pass Turn", key="ld_pass"):
                    _next_turn(s.ld_dice == 6); st.rerun()
            elif is_cpu:
                if st.button("Let CPU Move", key="ld_cpu_move"):
                    cpu_auto(); st.rerun()
            else:
                st.markdown("**Click a glowing piece on the board, or pick below:**")
                for pi in movable:
                    pc  = s.ld_pieces[cur_player][pi]
                    loc = "Base" if not pc["out"] else f"Step {pc['steps']}"
                    if st.button(
                        f"{COLOR_ICONS[cur_color]} Piece {pi+1}  ({loc})",
                        key=f"ld_mv_{pi}"):
                        do_move(cur_player, pi, s.ld_dice); st.rerun()

        st.divider()

        # Rules reminder
        with st.expander("Rules"):
            st.markdown("""
- Roll **6** to bring a piece out of base
- Rolling **6** gives you another turn
- Land on opponent → send them back to base
- **★ Star squares** are safe (no captures)
- Three 6s in a row → turn forfeited
- First to get all 4 pieces home wins!
""")
        if st.button("Reset Game", key="ld_reset"):
            reset_game("ld_"); st.rerun()


def _setup_screen():
    st.caption("Race all 4 pieces to the center — first player to finish all pieces wins!")

    st.markdown("### Setup Players")
    total = st.slider("How many players?", 2, 4, 2, key="ld_total_s")
    st.markdown("**Configure each player:**")

    configs = []
    for i in range(total):
        col_icon, col_name, col_type = st.columns([1, 3, 2])
        col   = COLORS[i]
        hexc  = LUDO_HEX[col]
        with col_icon:
            st.markdown(
                f'<div style="background:{hexc};width:42px;height:42px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-size:20px;margin-top:8px">'
                f'{PLAYER_ICONS[i]}</div>', unsafe_allow_html=True)
        with col_name:
            name = st.text_input(
                "Name", value=col, key=f"ld_sname_{i}",
                label_visibility="collapsed")
        with col_type:
            ptype = st.selectbox(
                "Type", ["Human Player", "Computer (CPU)"],
                key=f"ld_stype_{i}", label_visibility="collapsed")
        configs.append((name.strip() or col, ptype, col))

    st.markdown("")
    if st.button("Start Ludo!", key="ld_go"):
        names     = [c[0] for c in configs]
        n_humans  = sum(1 for c in configs if "Human" in c[1])
        color_map = {c[0]: c[2] for c in configs}
        st.session_state.ld_players   = names
        st.session_state.ld_n_humans  = n_humans
        st.session_state.ld_color_map = color_map
        st.session_state.ld_started   = True
        init_ludo_state()
        st.rerun()

    st.divider()
    st.markdown("""
**How to play:**
- Each color starts with 4 pieces locked in their base corner
- Roll a **6** to release a piece onto the board
- Move pieces clockwise around the board towards your home column
- Landing on an opponent's piece sends it back to their base
- **Gold star squares** are safe zones — no captures there
- First to get all 4 pieces into the center home wins!
""")
