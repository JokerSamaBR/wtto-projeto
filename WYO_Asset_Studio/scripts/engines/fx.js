(function(){'use strict';
function prng(seed){let x=(Number(seed)||1)>>>0;return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296}}
async function render(c,p,w,h){const r=prng(p.seed),cx=w/2,cy=h/2,t=Math.min(w,h),level=(Number(p.fxIntensity)||70)/100;
 c.save();c.translate(cx,cy);c.globalCompositeOperation='screen';
 if(p.fxType==='rift'){
  for(let i=0;i<125;i++){const a=i*3.1/124,yy=(a-.5)*t*.78,x=Math.sin(a*13+2.4)*t*.035; c.beginPath();c.moveTo(x,yy);c.lineTo(x+(r()-.5)*t*.05,yy+r()*t*.08);c.lineWidth=(2+r()*9)*level;c.strokeStyle=`hsla(${162+i*.9},95%,${55+r()*26}%,${.1+.4*r()})`;c.shadowColor='#67fce9';c.shadowBlur=20;c.stroke()}
 }else{
  const count=p.fxType==='portal'?18:8;
  for(let j=0;j<count;j++){c.beginPath();let rr=t*(.1+j*.014);for(let i=0;i<=260;i++){let a=i/260*Math.PI*2,noise=p.fxType==='portal'?Math.sin(a*11+j*.37)*t*.004:0,rx=Math.cos(a)*(rr+noise),ry=Math.sin(a)*(rr+noise);i?c.lineTo(rx,ry):c.moveTo(rx,ry)}c.closePath();c.strokeStyle=`hsla(${130+j*6},95%,${46+j*2}%,${.12+level*.44})`;c.lineWidth=(1.5+j*.16)*level;c.shadowBlur=11;c.shadowColor='#66facc';c.stroke()}
  if(p.fxType==='rune'){c.shadowBlur=0;for(let i=0;i<24;i++){let a=i*Math.PI/12;c.save();c.rotate(a);c.fillStyle='#91ffd5';c.fillRect(-1,-t*.28,2,t*.025);c.restore()}}
 }
 for(let i=0;i<450*level;i++){let x=(r()-.5)*t*.9,y=(r()-.5)*t*.9;c.beginPath();c.arc(x,y,(r()*1.8+.2)*w/512,0,7);c.fillStyle=r()>.6?'#ffe5ad':'#86e9cc';c.globalAlpha=r()*.55;c.fill()}
 c.restore()}
window.WYOEngines=window.WYOEngines||{};window.WYOEngines.fx={render};})();