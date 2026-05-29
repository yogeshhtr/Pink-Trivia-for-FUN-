# -*- coding: utf-8 -*-
"""games/snake.py — TP Games: Snake"""
import streamlit as st

SNAKE_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#1A0A12;display:flex;flex-direction:column;align-items:center;
  font-family:'Nunito',sans-serif;padding:10px;color:#F8D7E8;}
#hud{display:flex;gap:24px;margin-bottom:10px;font-weight:700;font-size:15px;}
.hud-item{background:#2D1224;border:1px solid #8B2050;border-radius:8px;
  padding:6px 16px;text-align:center;}
.hud-label{font-size:10px;color:#8B3060;text-transform:uppercase;letter-spacing:1px;}
.hud-val{font-size:20px;color:#FF69B4;font-weight:800;}
canvas{border:2px solid #8B2050;border-radius:12px;background:#1A0A12;
  box-shadow:0 0 20px rgba(255,20,147,.3);display:block;}
#msg{font-size:16px;font-weight:700;color:#FF1493;margin:10px 0;min-height:22px;
  text-shadow:0 0 10px rgba(255,20,147,.5);}
.btns{display:flex;gap:10px;margin-top:8px;}
button{background:linear-gradient(135deg,#8B2050,#FF1493);color:white;border:none;
  border-radius:8px;padding:8px 22px;font-size:14px;font-weight:700;cursor:pointer;
  box-shadow:0 0 10px rgba(255,20,147,.35);text-transform:uppercase;letter-spacing:1px;}
button:hover{box-shadow:0 0 20px rgba(255,20,147,.6);}
.hint{font-size:11px;color:#8B3060;margin-top:8px;letter-spacing:1px;}
/* D-pad for mobile */
#dpad{display:none;margin-top:10px;user-select:none;}
.dp-row{display:flex;justify-content:center;gap:4px;margin:2px 0;}
.dp-btn{background:#2D1224;border:1px solid #8B2050;border-radius:6px;
  width:44px;height:44px;font-size:18px;cursor:pointer;color:#FF69B4;
  display:flex;align-items:center;justify-content:center;font-weight:700;}
.dp-btn:active{background:#8B2050;}
@media(max-width:500px){#dpad{display:block;}}
</style>
</head>
<body>
<div id="hud">
  <div class="hud-item"><div class="hud-label">Score</div><div class="hud-val" id="sc">0</div></div>
  <div class="hud-item"><div class="hud-label">Best</div><div class="hud-val" id="bs">0</div></div>
  <div class="hud-item"><div class="hud-label">Level</div><div class="hud-val" id="lv">1</div></div>
</div>
<canvas id="c" width="400" height="400"></canvas>
<div id="msg">Press START to play!</div>
<div class="btns">
  <button onclick="startGame()">START</button>
  <button onclick="pauseGame()">PAUSE</button>
</div>
<div id="dpad">
  <div class="dp-row"><div class="dp-btn" onclick="setDir(0,-1)">▲</div></div>
  <div class="dp-row">
    <div class="dp-btn" onclick="setDir(-1,0)">◀</div>
    <div class="dp-btn" style="opacity:.3">●</div>
    <div class="dp-btn" onclick="setDir(1,0)">▶</div>
  </div>
  <div class="dp-row"><div class="dp-btn" onclick="setDir(0,1)">▼</div></div>
</div>
<div class="hint">Arrow keys / WASD / D-pad to move</div>

<script>
const C=document.getElementById('c'),ctx=C.getContext('2d');
const SZ=20,COLS=20,ROWS=20;
let snake,dir,nextDir,food,score,best=0,running=false,paused=false,loop,speed,level;

function startGame(){
  snake=[{x:10,y:10},{x:9,y:10},{x:8,y:10}];
  dir={x:1,y:0};nextDir={x:1,y:0};
  score=0;level=1;speed=145;
  placeFood();running=true;paused=false;
  document.getElementById('msg').textContent='';
  clearInterval(loop);loop=setInterval(tick,speed);draw();
}

function pauseGame(){
  if(!running)return;paused=!paused;
  document.getElementById('msg').textContent=paused?'⏸ PAUSED':'';
  if(!paused){clearInterval(loop);loop=setInterval(tick,speed);}
  else clearInterval(loop);
}

function setDir(dx,dy){
  if(dx!==0&&dir.x!==0)return;
  if(dy!==0&&dir.y!==0)return;
  nextDir={x:dx,y:dy};
}

function placeFood(){
  do{food={x:Math.floor(Math.random()*COLS),y:Math.floor(Math.random()*ROWS)};
  }while(snake.some(s=>s.x===food.x&&s.y===food.y));
}

function tick(){
  if(!running||paused)return;
  dir=nextDir;
  const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
  if(head.x<0||head.x>=COLS||head.y<0||head.y>=ROWS){endGame();return;}
  if(snake.some(s=>s.x===head.x&&s.y===head.y)){endGame();return;}
  snake.unshift(head);
  if(head.x===food.x&&head.y===food.y){
    score++;
    document.getElementById('sc').textContent=score;
    if(score>best){best=score;document.getElementById('bs').textContent=best;}
    if(score%5===0&&speed>55){
      speed=Math.max(55,speed-18);level++;
      document.getElementById('lv').textContent=level;
      clearInterval(loop);loop=setInterval(tick,speed);
    }
    placeFood();
  }else snake.pop();
  draw();
}

function endGame(){
  running=false;clearInterval(loop);
  document.getElementById('msg').textContent='GAME OVER  Score:'+score+'  Press START to retry!';
}

function draw(){
  ctx.clearRect(0,0,400,400);
  // Grid
  ctx.strokeStyle='rgba(139,32,80,.25)';ctx.lineWidth=0.5;
  for(let i=0;i<=COLS;i++){ctx.beginPath();ctx.moveTo(i*SZ,0);ctx.lineTo(i*SZ,400);ctx.stroke();}
  for(let j=0;j<=ROWS;j++){ctx.beginPath();ctx.moveTo(0,j*SZ);ctx.lineTo(400,j*SZ);ctx.stroke();}

  // Food — glowing dot
  const fx=food.x*SZ+SZ/2, fy=food.y*SZ+SZ/2;
  const grd=ctx.createRadialGradient(fx,fy,2,fx,fy,9);
  grd.addColorStop(0,'#FF69B4');grd.addColorStop(1,'#8B2050');
  ctx.fillStyle=grd;
  ctx.beginPath();ctx.arc(fx,fy,8,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#FF1493';ctx.lineWidth=1.5;ctx.stroke();

  // Snake
  snake.forEach((seg,i)=>{
    const pct=i/Math.max(snake.length,1);
    const r=255, g=Math.floor(20+(1-pct)*80), b=Math.floor(147-(1-pct)*80);
    ctx.fillStyle='rgb('+r+','+g+','+b+')';
    ctx.beginPath();
    if(ctx.roundRect)ctx.roundRect(seg.x*SZ+1,seg.y*SZ+1,SZ-2,SZ-2,5);
    else ctx.rect(seg.x*SZ+1,seg.y*SZ+1,SZ-2,SZ-2);
    ctx.fill();
    if(i===0){
      // Eyes
      const ex=seg.x*SZ, ey=seg.y*SZ;
      ctx.fillStyle='white';
      ctx.beginPath();ctx.arc(ex+6,ey+7,3,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(ex+14,ey+7,3,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#1A0A12';
      ctx.beginPath();ctx.arc(ex+6+dir.x*2,ey+7+dir.y*2,1.5,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(ex+14+dir.x*2,ey+7+dir.y*2,1.5,0,Math.PI*2);ctx.fill();
    }
  });
}

document.addEventListener('keydown',e=>{
  const k=e.key;
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d'].includes(k))e.preventDefault();
  if((k==='ArrowUp'   ||k==='w')&&dir.y!==1) setDir(0,-1);
  if((k==='ArrowDown' ||k==='s')&&dir.y!==-1)setDir(0,1);
  if((k==='ArrowLeft' ||k==='a')&&dir.x!==1) setDir(-1,0);
  if((k==='ArrowRight'||k==='d')&&dir.x!==-1)setDir(1,0);
});

let tx=0,ty=0;
C.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY;},{passive:true});
C.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-tx, dy=e.changedTouches[0].clientY-ty;
  if(Math.abs(dx)>Math.abs(dy)){
    if(dx>0&&dir.x!==-1)setDir(1,0);else if(dx<0&&dir.x!==1)setDir(-1,0);
  }else{
    if(dy>0&&dir.y!==-1)setDir(0,1);else if(dy<0&&dir.y!==1)setDir(0,-1);
  }
},{passive:true});

draw();
</script>
</body>
</html>"""

def run():
    st.markdown("## 🐍 Snake")
    st.caption("Arrow keys / WASD to move. Eat the glowing food. Don't crash!")
    st.components.v1.html(SNAKE_HTML, height=580, scrolling=False)
