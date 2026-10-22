(function(){'use strict';
const themes={fantasy:['#f6ecd4','#e3be7b','#285d2e','#65d763'],celestial:['#e8f1ff','#e6c37d','#294a7b','#8ccbec'],silver:['#fafafa','#b6bdc9','#393f5d','#c4cad6']};
function fitFont(ctx,text,maxW,base){let size=base;while(size>16){ctx.font=`900 ${size}px Georgia,serif`;if(ctx.measureText(text).width<=maxW)break;size-=2}return size}
function mascot(c,x,y,scale,col){c.save();c.translate(x,y);c.scale(scale,scale);c.beginPath();c.moveTo(-30,19);c.bezierCurveTo(-37,-10,-24,-27,-1,-26);c.bezierCurveTo(14,-39,32,-15,31,12);c.bezierCurveTo(27,32,-25,33,-30,19);c.closePath();let g=c.createLinearGradient(-18,-30,19,28);g.addColorStop(0,'#f6ffe4');g.addColorStop(.27,'#d5f79d');g.addColorStop(.65,col);g.addColorStop(1,'#368e48');c.fillStyle=g;c.strokeStyle='#174522';c.lineWidth=4;c.fill();c.stroke();c.fillStyle='#122d1d';c.beginPath();c.ellipse(-10,3,3,5,0,0,7);c.ellipse(10,3,3,5,0,0,7);c.fill();c.strokeStyle='#2d653c';c.lineWidth=2;c.beginPath();c.arc(0,9,6,0,Math.PI);c.stroke();c.fillStyle='#fff';c.beginPath();c.arc(-13,-14,6,0,7);c.fill();c.restore()}
function wing(c,x,y,s,flip,color){c.save();c.translate(x,y);c.scale(s*flip,s);c.fillStyle='#fbefcc';c.strokeStyle=color;c.lineWidth=3;for(let i=0;i<3;i++){c.beginPath();c.moveTo(0,i*11);c.quadraticCurveTo(38-i*4,-25-i*9,67-i*5,-39-i*12);c.quadraticCurveTo(61-i*6,13-i*5,0,24+i*4);c.closePath();c.fill();c.stroke()}c.restore()}
async function render(c,p,w,h){const [light,gold,edge,glow]=themes[p.logoPreset]||themes.fantasy,cx=w/2,cy=h/2,scale=w/512;
 c.save();c.translate(cx,cy);c.scale(scale,scale);c.translate(-256,-256);
 if(p.logoWings){wing(c,115,171,1,1,edge);wing(c,396,171,1,-1,edge)}
 const title=(p.logoText||'WYO').trim(),sub=(p.logoSub||'ONLINE').trim(),fs=fitFont(c,title,452,65);c.textAlign='center';c.textBaseline='middle';c.font=`900 ${fs}px Georgia,serif`;
 c.shadowColor=glow;c.shadowBlur=22;c.lineJoin='round';c.strokeStyle=edge;c.lineWidth=18;c.strokeText(title,256,248);
 c.shadowBlur=0;c.strokeStyle='#192f22';c.lineWidth=12;c.strokeText(title,256,248);
 c.strokeStyle=gold;c.lineWidth=7;c.strokeText(title,256,248);
 const grad=c.createLinearGradient(0,180,0,280);grad.addColorStop(0,'#fffdf5');grad.addColorStop(.45,light);grad.addColorStop(1,'#b49a76');c.fillStyle=grad;c.fillText(title,256,248);
 c.font='900 43px Georgia,serif';c.shadowColor=glow;c.shadowBlur=10;c.strokeStyle=edge;c.lineWidth=11;c.strokeText(sub,256,316);c.shadowBlur=0;c.strokeStyle=gold;c.lineWidth=5;c.strokeText(sub,256,316);c.fillStyle=light;c.fillText(sub,256,316);
 if(p.logoMascot)mascot(c,256,164,.81,glow);c.restore();
}
window.WYOEngines=window.WYOEngines||{};window.WYOEngines.logo={render};})();