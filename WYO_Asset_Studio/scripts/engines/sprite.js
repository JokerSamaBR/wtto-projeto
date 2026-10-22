(function(){'use strict';
 const cache={};
 function imgFromData(data){if(!data) return Promise.reject(Error('Imagem ausente'));if(!cache[data])cache[data]=new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>reject(Error('Imagem inválida'));img.src=data;});return cache[data]}
 function fit(ctx,img,x,y,w,h,quality=true){const s=Math.min(w/img.width,h/img.height),ww=img.width*s,hh=img.height*s;ctx.imageSmoothingEnabled=quality;ctx.imageSmoothingQuality='high';ctx.drawImage(img,x+(w-ww)/2,y+(h-hh)/2,ww,hh)}
 function chroma(canvas,kind){if(!['white','black'].includes(kind))return;const ctx=canvas.getContext('2d',{willReadFrequently:true});const {width:w,height:h}=canvas;const im=ctx.getImageData(0,0,w,h),d=im.data;for(let i=0;i<d.length;i+=4){if(d[i+3]===0)continue;const r=d[i],g=d[i+1],b=d[i+2];const v=kind==='white'?Math.min(r,g,b):255-Math.max(r,g,b);const t=Math.max(0,Math.min(1,(v-190)/45));d[i+3]=Math.round(d[i+3]*(1-t));}ctx.putImageData(im,0,0)}
 async function drawTemplate(ctx,project,w,h){const svg=window.WYO_ASSETS.knightFront;
   let data='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);
   const img=await imgFromData(data);
   const pix=project.spriteStyle==='vector'?1:Number(project.pixelSize)||2;
   const nativeW=Math.max(65,Math.round(256/(pix===1?1:pix/1.55))),nativeH=Math.max(80,Math.round(320/(pix===1?1:pix/1.55)));
   const buffer=document.createElement('canvas');buffer.width=nativeW;buffer.height=nativeH;
   const b=buffer.getContext('2d');b.imageSmoothingEnabled=true;b.imageSmoothingQuality='high';b.drawImage(img,0,0,nativeW,nativeH);
   const tw=w*.70,th=h*.88,k=Math.min(tw/nativeW,th/nativeH),dw=nativeW*k,dh=nativeH*k;
   ctx.imageSmoothingEnabled=project.spriteStyle==='vector';ctx.imageSmoothingQuality='high';ctx.drawImage(buffer,(w-dw)/2,(h-dh)/2,dw,dh);
 }
 async function drawReference(ctx,project,w,h){if(!project.references?.[0])throw Error('Importe uma imagem antes de usar Referência.');const img=await imgFromData(project.references[0].data);
   const crop=Number(project.crop)||0,x0=crop===1?0:crop===2?img.width/2:0,cw=crop===0?img.width:img.width/2;
   const buffer=document.createElement('canvas');buffer.width=Math.round(cw);buffer.height=img.height;
   const b=buffer.getContext('2d');b.drawImage(img,x0,0,cw,img.height,0,0,buffer.width,buffer.height);
   chroma(buffer,project.removeBg);
   let target=buffer;if(project.spriteStyle!=='vector'){
     const q=Math.max(1,Number(project.pixelSize)||2),ds=document.createElement('canvas');ds.width=Math.min(384,Math.round(buffer.width/q));ds.height=Math.min(384,Math.round(buffer.height/q));
     ds.getContext('2d').drawImage(buffer,0,0,ds.width,ds.height);target=ds;
   }
   fit(ctx,target,w*.09,h*.08,w*.82,h*.84,false)
 }
 async function drawSheet(ctx,project,w,h){const n=Number(project.directions)||1,frames=project.frames||[];
   if(n===1&&frames.length!==1)throw Error('Selecione exatamente 1 frame PNG.');
   if(n>1&&frames.length!==n)throw Error(`Sheet de ${n} direções precisa de ${n} imagens diferentes. Foram carregadas ${frames.length}.`);
   const columns=n===8?4:n===4?2:1,rows=Math.ceil(n/columns),cellW=w/columns,cellH=h/rows;
   for(let i=0;i<n;i++){const img=await imgFromData(frames[i].data);fit(ctx,img,i%columns*cellW+cellW*.08,Math.floor(i/columns)*cellH+cellH*.07,cellW*.84,cellH*.86,false)}
 }
 async function render(ctx,project,w,h){if(project.spriteSource==='image')await drawReference(ctx,project,w,h);else if(project.spriteSource==='sheet')await drawSheet(ctx,project,w,h);else{
   if(Number(project.directions)>1)throw Error('O template frontal não contém vistas laterais/traseiras. Importe frames reais em "Montar sheet".');
   await drawTemplate(ctx,project,w,h)
 }}
 window.WYOEngines=window.WYOEngines||{};window.WYOEngines.sprite={render};
})();