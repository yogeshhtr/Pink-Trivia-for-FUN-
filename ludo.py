import streamlit as st
from theme import init, reset_game, LUDO_HEX, LUDO_DARK

COLORS       = ["Red", "Green", "Yellow", "Blue"]
COLOR_ICONS  = {"Red":"🔴","Green":"🟢","Yellow":"🟡","Blue":"🔵"}
PLAYER_ICONS = ["🎀","🌟","💎","🔥"]

LUDO_GAME_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#1A0A12;font-family:'Nunito',sans-serif;color:#F8D7E8;
  display:flex;flex-direction:column;align-items:center;padding:6px;min-height:100vh;}

/* ── Setup screen ── */
#setup{width:100%;max-width:700px;}
.setup-title{font-size:26px;font-weight:800;color:#FF1493;text-align:center;
  text-shadow:0 0 18px rgba(255,20,147,.5);margin:8px 0 4px;}
.setup-sub{text-align:center;color:#8B3060;font-size:13px;margin-bottom:16px;}
.setup-card{background:#2D1224;border:1px solid #8B2050;border-radius:12px;padding:16px;margin-bottom:12px;}
.setup-row{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.color-dot{width:36px;height:36px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:16px;}
.setup-input{flex:1;background:#1A0A12;border:1px solid #8B2050;border-radius:8px;
  color:#F8D7E8;padding:7px 12px;font-size:14px;font-family:Nunito,sans-serif;}
.setup-input:focus{outline:none;border-color:#FF1493;}
.type-select{background:#1A0A12;border:1px solid #8B2050;border-radius:8px;
  color:#F8D7E8;padding:7px 10px;font-size:13px;font-family:Nunito,sans-serif;}
.type-select:focus{outline:none;border-color:#FF1493;}
.slider-row{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.slider-label{color:#C2547A;font-size:13px;font-weight:700;white-space:nowrap;}
input[type=range]{flex:1;accent-color:#FF1493;}
.player-count{color:#FF69B4;font-weight:800;font-size:16px;min-width:20px;}

/* ── Buttons ── */
.btn{background:linear-gradient(135deg,#8B2050,#FF1493);color:white;border:none;
  border-radius:8px;padding:10px 24px;font-size:14px;font-weight:700;cursor:pointer;
  text-transform:uppercase;letter-spacing:1px;box-shadow:0 0 12px rgba(255,20,147,.35);
  transition:all .2s;}
.btn:hover{box-shadow:0 0 22px rgba(255,20,147,.65);transform:translateY(-1px);}
.btn:active{transform:scale(.97);}
.btn-secondary{background:#2D1224;border:1px solid #8B2050;color:#F8D7E8;}
.btn-secondary:hover{border-color:#FF1493;box-shadow:0 0 10px rgba(255,20,147,.3);}
.btn-sm{padding:6px 14px;font-size:12px;}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:10px;}

/* ── Game layout ── */
#game{display:none;width:100%;max-width:1000px;}
.game-top{display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap;}
.score-card{flex:1;min-width:100px;background:#2D1224;border:1px solid #8B2050;
  border-radius:8px;padding:8px;text-align:center;transition:border-color .3s;}
.score-card.active{border-color:#FFD700;box-shadow:0 0 10px rgba(255,215,0,.3);}
.score-name{font-size:12px;font-weight:700;margin-bottom:2px;}
.score-bar{font-family:monospace;font-size:14px;letter-spacing:1px;margin:2px 0;}
.score-sub{font-size:10px;color:#8B3060;}

.game-body{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap;}
#canvas-wrap{position:relative;flex-shrink:0;}
canvas{display:block;border:2px solid #8B2050;border-radius:10px;
  box-shadow:0 0 24px rgba(255,20,147,.3);cursor:pointer;}

/* ── Side panel ── */
#panel{flex:1;min-width:200px;max-width:260px;}
.panel-card{background:#2D1224;border:1px solid #8B2050;border-radius:10px;
  padding:12px;margin-bottom:10px;}
.panel-title{font-size:11px;font-weight:700;color:#8B3060;text-transform:uppercase;
  letter-spacing:2px;margin-bottom:8px;}
.turn-badge{font-size:14px;font-weight:800;padding:4px 12px;border-radius:6px;
  display:inline-block;color:white;margin-bottom:8px;}
.msg-box{font-size:13px;color:#F8D7E8;line-height:1.5;min-height:40px;}

/* ── Dice ── */
#dice-container{display:flex;justify-content:center;margin:10px 0;}
#dice-svg-el{transition:transform .05s;}
.dice-num{text-align:center;font-size:26px;font-weight:800;color:#FF1493;
  text-shadow:0 0 10px rgba(255,20,147,.5);}

/* ── Movable piece buttons ── */
.mv-btn{display:block;width:100%;background:#3D1E34;border:1px solid #8B2050;
  border-radius:8px;padding:8px 10px;font-size:12px;font-weight:700;color:#F8D7E8;
  cursor:pointer;margin-bottom:6px;text-align:left;transition:all .15s;}
.mv-btn:hover{background:#8B2050;border-color:#FF1493;}
.mv-btn.highlighted{border-color:#FFD700;box-shadow:0 0 8px rgba(255,215,0,.4);}

/* ── CPU countdown ── */
#cpu-timer{text-align:center;color:#FFC107;font-size:12px;font-weight:700;}
.countdown{font-size:20px;color:#FF1493;}

/* ── Winner overlay ── */
#winner-overlay{display:none;position:fixed;inset:0;background:rgba(26,10,18,.92);
  z-index:100;flex-direction:column;align-items:center;justify-content:center;}
.winner-card{background:#2D1224;border:2px solid #FFD700;border-radius:20px;
  padding:40px 60px;text-align:center;box-shadow:0 0 60px rgba(255,215,0,.3);}
.winner-icon{font-size:64px;margin-bottom:10px;}
.winner-name{font-size:32px;font-weight:800;margin-bottom:6px;}
.winner-sub{font-size:15px;color:#8B3060;margin-bottom:20px;}

/* ── Rules ── */
.rules-list{font-size:12px;color:#C2547A;line-height:1.8;}
.rules-list li{margin-bottom:2px;}
</style>
</head>
<body>

<!-- ══════════════════ SETUP SCREEN ══════════════════ -->
<div id="setup">
  <div class="setup-title">🎯 Ludo</div>
  <div class="setup-sub">Race all 4 pieces home — classic Ludo rules!</div>

  <div class="setup-card">
    <div class="slider-row">
      <span class="slider-label">Number of players:</span>
      <input type="range" id="player-count-slider" min="2" max="4" value="2"
             oninput="updatePlayerCount(this.value)">
      <span class="player-count" id="player-count-display">2</span>
    </div>
    <div id="player-rows"></div>
  </div>

  <div class="setup-card">
    <div class="panel-title">Rules</div>
    <ul class="rules-list">
      <li>Roll a <b style="color:#FF69B4">6</b> to bring a piece out of base</li>
      <li>Rolling 6 gives you an extra turn</li>
      <li>Land on opponent's piece → sends it back to base</li>
      <li><b style="color:#FFD700">★ Star squares</b> are safe — no captures</li>
      <li>Three 6s in a row → turn forfeited</li>
      <li>First to get all 4 pieces home wins!</li>
    </ul>
  </div>

  <div class="btn-row">
    <button class="btn" onclick="startGame()">▶  Start Ludo!</button>
  </div>
</div>

<!-- ══════════════════ GAME SCREEN ══════════════════ -->
<div id="game">
  <!-- Scoreboard -->
  <div class="game-top" id="scoreboard"></div>

  <div class="game-body">
    <!-- Board -->
    <div id="canvas-wrap">
      <canvas id="cv"></canvas>
    </div>

    <!-- Side Panel -->
    <div id="panel">
      <div class="panel-card">
        <div class="panel-title">Current Turn</div>
        <div id="turn-badge" class="turn-badge">—</div>
        <div class="msg-box" id="msg-box">Roll the dice to begin!</div>
      </div>

      <div class="panel-card">
        <div class="panel-title">Dice</div>
        <div id="dice-container">
          <svg id="dice-svg-el" width="70" height="70" viewBox="0 0 50 50">
            <rect id="dice-rect" width="50" height="50" rx="10" fill="#2D1224" stroke="#8B2050" stroke-width="2"/>
            <g id="dice-dots">
              <text x="25" y="33" text-anchor="middle" font-size="22" fill="#8B3060">?</text>
            </g>
          </svg>
        </div>
        <div class="dice-num" id="dice-num">–</div>
        <div id="cpu-timer" style="display:none"></div>
      </div>

      <div class="panel-card" id="action-panel">
        <div class="panel-title">Action</div>
        <div id="action-content"></div>
      </div>

      <div class="btn-row" style="flex-direction:column;align-items:stretch;">
        <button class="btn btn-secondary btn-sm" onclick="resetToSetup()">Change Players</button>
        <button class="btn btn-secondary btn-sm" onclick="resetGame()">Restart Game</button>
      </div>
    </div>
  </div>
</div>

<!-- Winner Overlay -->
<div id="winner-overlay">
  <div class="winner-card">
    <div class="winner-icon" id="winner-icon">🏆</div>
    <div class="winner-name" id="winner-name">Player Wins!</div>
    <div class="winner-sub">Congratulations!</div>
    <div class="btn-row">
      <button class="btn" onclick="resetGame()">Play Again</button>
      <button class="btn btn-secondary" onclick="resetToSetup()">Change Players</button>
    </div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════════════════════════════
// CONSTANTS
// ══════════════════════════════════════════════════════════════════════
const COLORS      = ["Red","Green","Yellow","Blue"];
const COLOR_HEX   = {Red:"#E91E63",Green:"#4CAF50",Yellow:"#FFC107",Blue:"#2196F3"};
const COLOR_DARK  = {Red:"#880E4F",Green:"#1B5E20",Yellow:"#795548",Blue:"#0D47A1"};
const COLOR_LIGHT = {Red:"#3A0810",Green:"#0A2A10",Yellow:"#2A1800",Blue:"#0A1A3A"};
const COLOR_ICONS = {Red:"🔴",Green:"🟢",Yellow:"🟡",Blue:"🔵"};
const P_ICONS     = ["🎀","🌟","💎","🔥"];
const START_SQ    = {Red:0,Green:13,Yellow:26,Blue:39};
const HOME_ENTRY  = {Red:50,Green:11,Yellow:24,Blue:37};
const SAFE_SQ     = new Set([0,8,13,21,26,34,39,47]);

// Board path: 52 squares → [row,col] on 15×15 grid
const PATH = [
  [14,6],[13,6],[12,6],[11,6],[10,6],[9,6],
  [8,5],[8,4],[8,3],[8,2],[8,1],[8,0],
  [7,0],[6,0],
  [6,1],[6,2],[6,3],[6,4],[6,5],
  [5,6],[4,6],[3,6],[2,6],[1,6],[0,6],
  [0,7],
  [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],
  [6,9],[6,10],[6,11],[6,12],[6,13],[6,14],
  [7,14],
  [8,14],[8,13],[8,12],[8,11],[8,10],[8,9],
  [9,8],[10,8],[11,8],[12,8],[13,8],[14,8],
  [14,7],
];
const HOME_COLS = {
  Red:    [[13,7],[12,7],[11,7],[10,7],[9,7]],
  Green:  [[7,1],[7,2],[7,3],[7,4],[7,5]],
  Yellow: [[1,7],[2,7],[3,7],[4,7],[5,7]],
  Blue:   [[7,13],[7,12],[7,11],[7,10],[7,9]],
};
const BASE_ORIGINS = {Red:[1,1],Green:[1,9],Yellow:[9,9],Blue:[9,1]};
const BASE_OFFSETS = [[1,1],[2,1],[1,2],[2,2]];

// ══════════════════════════════════════════════════════════════════════
// SETUP UI
// ══════════════════════════════════════════════════════════════════════
let numPlayers = 2;
function updatePlayerCount(n){
  numPlayers = parseInt(n);
  document.getElementById('player-count-display').textContent = n;
  renderPlayerRows();
}
function renderPlayerRows(){
  const cont = document.getElementById('player-rows');
  cont.innerHTML = '';
  for(let i=0;i<numPlayers;i++){
    const col = COLORS[i];
    const hex = COLOR_HEX[col];
    cont.innerHTML += `
      <div class="setup-row">
        <div class="color-dot" style="background:${hex}">${P_ICONS[i]}</div>
        <input class="setup-input" id="pname_${i}" value="${col}" placeholder="Player name">
        <select class="type-select" id="ptype_${i}">
          <option value="human">Human</option>
          <option value="cpu">Computer (CPU)</option>
        </select>
      </div>`;
  }
}
renderPlayerRows();

// ══════════════════════════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════════════════════════
let players=[], playerTypes={}, colorMap={};
let pieces={};   // {playerName: [{steps,out,done}, ...]}
let curIdx=0, diceVal=0, rolled=false, movable=[], consec6=0;
let gameMsg="Roll the dice to begin!";
let winner=null;

// Animation state
let diceAnim=false, moveAnim=null, cpuTimer=null;
let animPiece=null; // {player,pi,fromX,fromY,toX,toY,progress}

// Canvas
const cv  = document.getElementById('cv');
const ctx = cv.getContext('2d');
const CS  = 38;   // cell size
const BSZ = 15*CS;
cv.width  = BSZ;
cv.height = BSZ;

function startGame(){
  players=[]; playerTypes={}; colorMap={};
  for(let i=0;i<numPlayers;i++){
    const nm   = document.getElementById('pname_'+i).value.trim()||COLORS[i];
    const type = document.getElementById('ptype_'+i).value;
    players.push(nm);
    playerTypes[nm] = type;
    colorMap[nm]    = COLORS[i];
  }
  initState();
  document.getElementById('setup').style.display='none';
  document.getElementById('game').style.display='block';
  buildScoreboard();
  updatePanel();
  requestAnimationFrame(loop);
  // if first player is CPU, trigger after delay
  if(playerTypes[players[0]]==='cpu') scheduleCpuTurn();
}

function initState(){
  curIdx=0; diceVal=0; rolled=false; movable=[]; consec6=0; winner=null;
  pieces={};
  players.forEach(p=>{
    pieces[p]=[{steps:0,out:false,done:false},{steps:0,out:false,done:false},
               {steps:0,out:false,done:false},{steps:0,out:false,done:false}];
  });
  gameMsg="Roll the dice to begin!";
}

function resetGame(){
  clearTimers();
  initState();
  document.getElementById('winner-overlay').style.display='none';
  buildScoreboard();
  updatePanel();
}

function resetToSetup(){
  clearTimers();
  document.getElementById('winner-overlay').style.display='none';
  document.getElementById('game').style.display='none';
  document.getElementById('setup').style.display='block';
}

function clearTimers(){
  if(cpuTimer){clearTimeout(cpuTimer);cpuTimer=null;}
  diceAnim=false; moveAnim=null; animPiece=null;
}

// ══════════════════════════════════════════════════════════════════════
// PATH HELPERS
// ══════════════════════════════════════════════════════════════════════
function pathPos(color, steps){
  const start = START_SQ[color];
  const entry = HOME_ENTRY[color];
  const ste   = (entry - start + 52) % 52;
  if(steps > ste){
    const hi = steps - ste - 1;
    if(hi >= 5) return {type:'done',idx:0};
    return {type:'home',idx:hi};
  }
  return {type:'board',idx:(start+steps)%52};
}

function getMovable(player, dice){
  const col = colorMap[player];
  const out = [];
  pieces[player].forEach((pc,i)=>{
    if(pc.done) return;
    if(!pc.out){
      if(dice===6) out.push(i);
    } else {
      const ste=(HOME_ENTRY[col]-START_SQ[col]+52)%52;
      if(pc.steps>ste){
        const hr=5-(pc.steps-ste-1);
        if(dice>hr) return;
      }
      out.push(i);
    }
  });
  return out;
}

// ══════════════════════════════════════════════════════════════════════
// PIECE PIXEL POSITION
// ══════════════════════════════════════════════════════════════════════
function piecePixel(player, pi){
  const col = colorMap[player];
  const pc  = pieces[player][pi];
  let r,c;
  if(pc.done){
    return {x:7*CS+CS/2+(pi%2-0.5)*12, y:7*CS+CS/2+(Math.floor(pi/2)-0.5)*12};
  }
  if(!pc.out){
    const [br,bc]=BASE_ORIGINS[col];
    const [dr,dc]=BASE_OFFSETS[pi];
    r=br+dr; c=bc+dc;
    return {x:c*CS+CS/2, y:r*CS+CS/2};
  }
  const ste=(HOME_ENTRY[col]-START_SQ[col]+52)%52;
  if(pc.steps>ste){
    const hi=pc.steps-ste-1;
    [r,c]=hi<5?HOME_COLS[col][hi]:[7,7];
  } else {
    const bidx=(START_SQ[col]+pc.steps)%52;
    [r,c]=bidx<PATH.length?PATH[bidx]:[7,7];
  }
  return {x:c*CS+CS/2, y:r*CS+CS/2};
}

// ══════════════════════════════════════════════════════════════════════
// DICE
// ══════════════════════════════════════════════════════════════════════
const DICE_DOTS={
  1:[[25,25]],
  2:[[13,13],[37,37]],
  3:[[13,13],[25,25],[37,37]],
  4:[[13,13],[37,13],[13,37],[37,37]],
  5:[[13,13],[37,13],[25,25],[13,37],[37,37]],
  6:[[13,10],[37,10],[13,25],[37,25],[13,40],[37,40]],
};
let diceAngle=0, diceShakeFrame=0, diceFinalVal=0;

function rollDice(){
  if(diceAnim||rolled||winner) return;
  const col = colorMap[players[curIdx]];
  diceFinalVal = 1+Math.floor(Math.random()*6);
  diceVal      = 0;
  diceAnim     = true;
  diceShakeFrame=0;
  animateDice(col);
}

function animateDice(col){
  if(!diceAnim) return;
  diceShakeFrame++;
  // Show random face while rolling
  const fakeVal=1+Math.floor(Math.random()*6);
  updateDiceSVG(fakeVal, col, diceShakeFrame);
  if(diceShakeFrame < 18){
    setTimeout(()=>animateDice(col), 60);
  } else {
    // Final land
    diceAnim = false;
    diceVal  = diceFinalVal;
    updateDiceSVG(diceVal, col, 0);
    document.getElementById('dice-num').textContent = diceVal;
    finishRoll();
  }
}

function updateDiceSVG(val, col, frame){
  const hex   = COLOR_HEX[col]||'#FF1493';
  const angle = frame>0?(Math.sin(frame*1.2)*8*(1-frame/20)):0;
  const el    = document.getElementById('dice-svg-el');
  el.style.transform=`rotate(${angle}deg)`;
  document.getElementById('dice-rect').setAttribute('stroke',hex);
  const g=document.getElementById('dice-dots');
  g.innerHTML='';
  (DICE_DOTS[val]||[]).forEach(([x,y])=>{
    const c=document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r','4');
    c.setAttribute('fill',hex);g.appendChild(c);
  });
}

function finishRoll(){
  const cur=players[curIdx];
  const col=colorMap[cur];
  if(diceVal===6) consec6++; else consec6=0;
  if(consec6>=3){
    gameMsg="Three 6s in a row! Turn forfeited.";
    consec6=0; rolled=false;
    nextTurn(false); updatePanel(); return;
  }
  rolled  = true;
  movable = getMovable(cur,diceVal);
  gameMsg = `${cur} rolled ${diceVal}!`;
  if(movable.length===0){
    gameMsg+=" — No valid moves, turn passes.";
    rolled=false;
    setTimeout(()=>{ nextTurn(diceVal===6); updatePanel(); },900);
  }
  updatePanel();
}

// ══════════════════════════════════════════════════════════════════════
// MOVE PIECE (with animation)
// ══════════════════════════════════════════════════════════════════════
function movePiece(player, pi){
  if(!rolled||winner) return;
  if(!movable.includes(pi)) return;
  const col = colorMap[player];
  const pc  = pieces[player][pi];

  const fromPos = piecePixel(player,pi);

  // Apply move to state
  let captured=false, capMsg='';
  if(!pc.out){
    pc.out=true; pc.steps=0;
    gameMsg=`${player} brought piece ${pi+1} out of base!`;
  } else {
    pc.steps += diceVal;
    const pos = pathPos(col, pc.steps);
    if(pos.type==='done'){
      pc.done=true;
      gameMsg=`${player}'s piece ${pi+1} reached HOME!`;
    } else if(pos.type==='home'){
      gameMsg=`${player}'s piece ${pi+1} → home column step ${pos.idx+1}`;
    } else {
      gameMsg=`${player}'s piece ${pi+1} → square ${pos.idx}`;
      if(!SAFE_SQ.has(pos.idx)){
        players.forEach(op=>{
          if(op===player) return;
          const oc=colorMap[op];
          pieces[op].forEach((opc,opi)=>{
            if(!opc.out||opc.done) return;
            const op2=pathPos(oc,opc.steps);
            if(op2.type==='board'&&op2.idx===pos.idx){
              opc.out=false; opc.steps=0;
              capMsg=` — captured ${op}'s piece!`;
            }
          });
        });
      }
    }
  }
  if(capMsg) gameMsg+=capMsg;

  const toPos = piecePixel(player,pi);

  // Animate the move
  animPiece={player,pi,
    fromX:fromPos.x,fromY:fromPos.y,
    toX:toPos.x,toY:toPos.y,
    progress:0, col:COLOR_HEX[col], dark:COLOR_DARK[col]};

  setTimeout(()=>{
    animPiece=null;
    // Check winner
    if(pieces[player].every(p=>p.done)){
      winner=player; showWinner(player); updatePanel(); return;
    }
    rolled=false; movable=[];
    nextTurn(diceVal===6);
    updatePanel();
    updateScoreboard();
    // CPU auto-play
    if(!winner && playerTypes[players[curIdx]]==='cpu') scheduleCpuTurn();
  }, 500);

  updatePanel();
  updateScoreboard();
}

// ══════════════════════════════════════════════════════════════════════
// TURN MANAGEMENT
// ══════════════════════════════════════════════════════════════════════
function nextTurn(extra){
  if(!extra) curIdx=(curIdx+1)%players.length;
  rolled=false; movable=[];
}

function scheduleCpuTurn(){
  clearTimers();
  let count=3;
  const el=document.getElementById('cpu-timer');
  el.style.display='block';
  el.innerHTML=`CPU plays in <span class="countdown">${count}</span>s`;
  cpuTimer=setInterval(()=>{
    count--;
    if(count<=0){
      clearInterval(cpuTimer); cpuTimer=null;
      el.style.display='none';
      doCpuTurn();
    } else {
      el.innerHTML=`CPU plays in <span class="countdown">${count}</span>s`;
    }
  },1000);
}

function doCpuTurn(){
  if(winner) return;
  const cur=players[curIdx];
  if(playerTypes[cur]!=='cpu') return;
  if(!rolled){
    rollDice();
    // Wait for dice anim then move
    setTimeout(()=>{
      if(movable.length>0) doCpuMove(cur);
      else if(!winner && playerTypes[players[curIdx]]==='cpu') scheduleCpuTurn();
    },1400);
  }
}

function doCpuMove(player){
  if(!rolled||movable.length===0) return;
  // Strategy: prefer capturing, else furthest piece
  let best=movable[0];
  let bestSteps=-1;
  movable.forEach(i=>{
    const pc=pieces[player][i];
    if(pc.out&&pc.steps>bestSteps){ bestSteps=pc.steps; best=i; }
  });
  movePiece(player,best);
}

// ══════════════════════════════════════════════════════════════════════
// CANVAS CLICK
// ══════════════════════════════════════════════════════════════════════
cv.addEventListener('click',e=>{
  if(!rolled||winner||animPiece) return;
  const cur=players[curIdx];
  if(playerTypes[cur]==='cpu') return;
  const rect=cv.getBoundingClientRect();
  const mx=e.clientX-rect.left, my=e.clientY-rect.top;
  // Check each movable piece
  movable.forEach(pi=>{
    const pos=piecePixel(cur,pi);
    const dist=Math.hypot(mx-pos.x,my-pos.y);
    if(dist<=18){ movePiece(cur,pi); }
  });
});

// ══════════════════════════════════════════════════════════════════════
// PANEL / SCOREBOARD UI
// ══════════════════════════════════════════════════════════════════════
function buildScoreboard(){
  const sb=document.getElementById('scoreboard');
  sb.innerHTML='';
  players.forEach((p,i)=>{
    const col=colorMap[p];
    const hex=COLOR_HEX[col];
    sb.innerHTML+=`<div class="score-card" id="sc_${i}">
      <div class="score-name" style="color:${hex}">${P_ICONS[i]} ${p}</div>
      <div class="score-bar" id="sbar_${i}" style="color:${hex}">░░░░</div>
      <div class="score-sub" id="ssub_${i}">0/4 home</div>
    </div>`;
  });
  updateScoreboard();
}

function updateScoreboard(){
  players.forEach((p,i)=>{
    const done=pieces[p].filter(pc=>pc.done).length;
    const bar='█'.repeat(done)+'░'.repeat(4-done);
    const el=document.getElementById('sc_'+i);
    if(el){
      document.getElementById('sbar_'+i).textContent=bar;
      document.getElementById('ssub_'+i).textContent=`${done}/4 home`;
      el.classList.toggle('active',i===curIdx);
    }
  });
}

function updatePanel(){
  const cur  =players[curIdx];
  const col  =colorMap[cur];
  const hex  =COLOR_HEX[col];
  const isCpu=playerTypes[cur]==='cpu';

  document.getElementById('turn-badge').textContent=
    `${COLOR_ICONS[col]} ${cur} (${col})`;
  document.getElementById('turn-badge').style.background=hex;
  document.getElementById('msg-box').textContent=gameMsg;

  const ac=document.getElementById('action-content');
  if(winner){ ac.innerHTML=''; return; }

  if(!rolled){
    if(isCpu){
      ac.innerHTML=`<p style="color:#C2547A;font-size:12px">CPU is thinking…</p>`;
    } else {
      ac.innerHTML=`<button class="btn" onclick="rollDice()" style="width:100%">🎲 Roll Dice</button>`;
    }
  } else if(movable.length===0){
    ac.innerHTML=`<p style="color:#C2547A;font-size:12px">No moves available — passing turn.</p>`;
  } else if(isCpu){
    ac.innerHTML=`<p style="color:#C2547A;font-size:12px">CPU choosing move…</p>`;
  } else {
    let html=`<p style="color:#8B3060;font-size:11px;margin-bottom:6px">Click a glowing piece on the board, or:</p>`;
    movable.forEach(pi=>{
      const pc=pieces[cur][pi];
      const loc=pc.out?`Step ${pc.steps}`:'In Base';
      html+=`<button class="mv-btn" onclick="movePiece('${cur}',${pi})">
        ${COLOR_ICONS[col]} Piece ${pi+1} <span style="color:#8B3060">(${loc})</span>
      </button>`;
    });
    ac.innerHTML=html;
  }
}

function showWinner(player){
  const idx=players.indexOf(player);
  const col=colorMap[player];
  const hex=COLOR_HEX[col];
  const ov=document.getElementById('winner-overlay');
  document.getElementById('winner-icon').textContent=P_ICONS[idx];
  const nm=document.getElementById('winner-name');
  nm.textContent=`${player} Wins!`;
  nm.style.color=hex;
  ov.style.display='flex';
}

// ══════════════════════════════════════════════════════════════════════
// DRAWING
// ══════════════════════════════════════════════════════════════════════
function cellFill(r,c){
  if(r<6&&c<6)   return COLOR_LIGHT.Red;
  if(r<6&&c>8)   return COLOR_LIGHT.Green;
  if(r>8&&c>8)   return COLOR_LIGHT.Yellow;
  if(r>8&&c<6)   return COLOR_LIGHT.Blue;
  if(6<=r&&r<=8&&6<=c&&c<=8) return '#2D1224';
  // Home column tints
  if(c===7&&r>=9&&r<=13) return COLOR_LIGHT.Red;
  if(r===7&&c>=1&&c<=5)  return COLOR_LIGHT.Green;
  if(c===7&&r>=1&&r<=5)  return COLOR_LIGHT.Yellow;
  if(r===7&&c>=9&&c<=13) return COLOR_LIGHT.Blue;
  // Entry column tints
  if(c===6&&r>=1&&r<=5)  return '#2A0818';
  if(r===6&&c>=1&&c<=5)  return '#0A2410';
  if(c===8&&r>=1&&r<=5)  return '#2A1400';
  if(r===8&&c>=9&&c<=13) return '#0A1430';
  return '#1E0E1A';
}

function drawBoard(){
  ctx.clearRect(0,0,BSZ,BSZ);
  for(let r=0;r<15;r++){
    for(let c=0;c<15;c++){
      ctx.fillStyle=cellFill(r,c);
      ctx.fillRect(c*CS,r*CS,CS,CS);
      ctx.strokeStyle='rgba(139,32,80,.25)';
      ctx.lineWidth=0.5;
      ctx.strokeRect(c*CS,r*CS,CS,CS);
    }
  }
  // Safe star squares
  PATH.forEach(([r,c],idx)=>{
    if(SAFE_SQ.has(idx)){
      ctx.fillStyle='rgba(255,215,0,.08)';
      ctx.fillRect(c*CS,r*CS,CS,CS);
      ctx.fillStyle='rgba(255,215,0,.55)';
      ctx.font=`bold ${Math.floor(CS*.44)}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText('★',c*CS+CS/2,r*CS+CS/2);
    }
  });
  // Home base inner boxes
  [['Red',1,1],['Green',1,9],['Yellow',9,9],['Blue',9,1]].forEach(([col,r0,c0])=>{
    const hex=COLOR_HEX[col];
    ctx.fillStyle=hex+'1A';
    ctx.strokeStyle=hex+'66';
    ctx.lineWidth=2;
    ctx.beginPath();
    roundRect(ctx,c0*CS+4,r0*CS+4,4*CS-8,4*CS-8,8);
    ctx.fill();ctx.stroke();
    // Inner white circle
    ctx.fillStyle='rgba(255,255,255,.06)';
    ctx.beginPath();
    ctx.arc(c0*CS+2*CS,r0*CS+2*CS,CS*.9,0,Math.PI*2);
    ctx.fill();
  });
  // Center star/home triangles
  const cx=7*CS+CS/2, cy=7*CS+CS/2, h=CS*1.45;
  [['Red',-1,-1],['Green',1,-1],['Yellow',1,1],['Blue',-1,1]].forEach(([col,sx,sy])=>{
    ctx.fillStyle=COLOR_HEX[col]+'99';
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.lineTo(cx+sx*h,cy+sy*h);
    ctx.lineTo(cx+sy*h,cy-sx*h);
    ctx.closePath();ctx.fill();
  });
  ctx.fillStyle='rgba(255,215,0,.15)';
  ctx.beginPath();ctx.arc(cx,cy,CS*.6,0,Math.PI*2);ctx.fill();
}

function roundRect(ctx,x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);
  ctx.closePath();
}

function drawPieces(t){
  // Build overlap counter
  const posMap={};
  players.forEach(pl=>{
    pieces[pl].forEach((pc,pi)=>{
      if(animPiece&&animPiece.player===pl&&animPiece.pi===pi) return;
      const pos=piecePixel(pl,pi);
      const key=Math.round(pos.x)+','+Math.round(pos.y);
      if(!posMap[key]) posMap[key]=[];
      posMap[key].push({pl,pi,pos});
    });
  });
  const OFFSETS=[[-7,-7],[7,-7],[-7,7],[7,7]];
  Object.values(posMap).forEach(arr=>{
    arr.forEach((item,slot)=>{
      const {pl,pi,pos}=item;
      const col=colorMap[pl];
      const hex=COLOR_HEX[col];
      const dark=COLOR_DARK[col];
      let x=pos.x, y=pos.y;
      if(arr.length>1){ x+=OFFSETS[slot%4][0]; y+=OFFSETS[slot%4][1]; }
      const isMovable=rolled&&movable.includes(pi)&&pl===players[curIdx];
      const R=isMovable?14:11;
      if(isMovable){
        // Pulsing glow
        const pulse=0.5+0.5*Math.sin(t/350);
        ctx.save();
        ctx.shadowColor=hex;ctx.shadowBlur=14+6*pulse;
        ctx.beginPath();ctx.arc(x,y,R+4,0,Math.PI*2);
        ctx.fillStyle=hex+'22';ctx.fill();
        ctx.restore();
        // Gold ring
        ctx.beginPath();ctx.arc(x,y,R+5,0,Math.PI*2);
        ctx.strokeStyle=`rgba(255,215,0,${.6+.35*pulse})`;
        ctx.lineWidth=2;ctx.stroke();
      }
      // Piece gradient
      const grad=ctx.createRadialGradient(x-3,y-3,2,x,y,R);
      grad.addColorStop(0,'#fff');
      grad.addColorStop(0.35,hex);
      grad.addColorStop(1,dark);
      ctx.beginPath();ctx.arc(x,y,R,0,Math.PI*2);
      ctx.fillStyle=grad;ctx.fill();
      ctx.strokeStyle=isMovable?'#FFD700':dark;
      ctx.lineWidth=isMovable?2:1.5;ctx.stroke();
      // Label
      ctx.fillStyle='white';
      ctx.font=`bold 10px Nunito,sans-serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pi+1,x,y);
    });
  });

  // Draw moving piece
  if(animPiece){
    animPiece.progress=Math.min(1,animPiece.progress+0.045);
    const p=animPiece.progress;
    // Ease in-out
    const ep=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
    const x=animPiece.fromX+(animPiece.toX-animPiece.fromX)*ep;
    const y=animPiece.fromY+(animPiece.toY-animPiece.fromY)*ep - Math.sin(p*Math.PI)*18;
    const hex=animPiece.col, dark=animPiece.dark;
    // Shadow
    ctx.save();ctx.shadowColor=hex;ctx.shadowBlur=16;
    const g2=ctx.createRadialGradient(x-3,y-3,2,x,y,15);
    g2.addColorStop(0,'#fff');g2.addColorStop(.35,hex);g2.addColorStop(1,dark);
    ctx.beginPath();ctx.arc(x,y,15,0,Math.PI*2);
    ctx.fillStyle=g2;ctx.fill();
    ctx.strokeStyle='#FFD700';ctx.lineWidth=2;ctx.stroke();
    ctx.restore();
  }
}

// ══════════════════════════════════════════════════════════════════════
// MAIN LOOP
// ══════════════════════════════════════════════════════════════════════
function loop(t){
  if(document.getElementById('game').style.display!=='none'){
    drawBoard();
    drawPieces(t);
  }
  requestAnimationFrame(loop);
}
</script>
</body>
</html>
"""

def run():
    init({"ld_started_flag": False})
    st.markdown("## 🎯 Ludo")
    st.caption("Self-contained — all game logic, animations, and CPU AI run in the browser!")
    st.components.v1.html(LUDO_GAME_HTML, height=820, scrolling=True)

