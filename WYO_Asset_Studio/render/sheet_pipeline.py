#!/usr/bin/env python3
"""WYO Asset Studio v2 — Reference Sheet Processor.

Operates on an EXISTING image containing multiple authored directions.
It does NOT invent or redraw missing viewpoints. Deterministically segments,
normalizes and exports a pixel-clean PNG sheet with eight separate PNGs.
License of source artwork remains the user's responsibility.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from PIL import Image
import numpy as np

DIRECTIONS = [
    'frente', 'diagonal_frente_esquerda', 'lado_esquerdo',
    'diagonal_tras_esquerda', 'tras', 'diagonal_tras_direita',
    'lado_direito', 'diagonal_frente_direita',
]


def smooth_projection(x, radius=2):
    return np.convolve(x.astype(np.float64), np.ones(radius * 2 + 1), mode='same')


def find_cut(projection, estimated, search):
    a = max(2, estimated - search)
    b = min(len(projection) - 2, estimated + search)
    values = smooth_projection(projection)[a:b+1]
    lo = np.min(values)
    candidates = np.flatnonzero(values <= lo + 0.001)
    # In an empty corridor choose the middle of its zero run nearest the estimate.
    if len(candidates) == 0:
        return estimated
    runs = np.split(candidates, np.where(np.diff(candidates) != 1)[0] + 1)
    positions = [a + round((run[0] + run[-1]) / 2) for run in runs]
    return min(positions, key=lambda x: abs(x-estimated))


def source_mask(im: Image.Image, threshold=32):
    return np.asarray(im.getchannel('A')) > threshold


def split_from_source(image: Image.Image, cols=4, rows=2):
    """Prefer transparent corridors; computes each row's own column boundaries."""
    mask = source_mask(image)
    height, width = mask.shape
    ybounds = [0]
    for i in range(1, rows):
        est = round(i * height / rows)
        ybounds.append(find_cut(mask.sum(axis=1), est, int(height / (rows*5))))
    ybounds.append(height)
    frames, source_rects = [], []
    for row in range(rows):
        y0, y1 = ybounds[row:row+2]
        segment = mask[y0:y1]
        projection = segment.sum(axis=0)
        xbounds = [0]
        for col in range(1, cols):
            est = round(col * width / cols)
            xbounds.append(find_cut(projection, est, int(width/(cols*5))))
        xbounds.append(width)
        for col in range(cols):
            x0, x1 = xbounds[col:col+2]
            piece = image.crop((x0,y0,x1,y1))
            bbox = piece.getchannel('A').point(lambda n: 255 if n>12 else 0).getbbox()
            if not bbox:
                raise ValueError(f'Quadro vazio: linha={row+1}, coluna={col+1}')
            padding = 2
            bx0,by0,bx1,by1=bbox
            bbox = (max(0,bx0-padding),max(0,by0-padding),min(piece.width,bx1+padding),min(piece.height,by1+padding))
            frames.append(piece.crop(bbox))
            source_rects.append({'row':row, 'col':col, 'rect':[x0+bbox[0],y0+bbox[1],x0+bbox[2],y0+bbox[3]]})
    return frames,source_rects


def tidy_alpha(image: Image.Image) -> Image.Image:
    """Zero invisible RGB; preserve antialiased/partly transparent painted edges."""
    a=np.asarray(image.convert('RGBA')).copy()
    a[a[:,:,3] < 12] = [0,0,0,0]
    return Image.fromarray(a,'RGBA')


def render_sheet(source: Image.Image, outdir: Path, tile_w=224, tile_h=256, max_sprite_w=206, max_sprite_h=240, pixel_mode='original'):
    source=tidy_alpha(source)
    frames,rects=split_from_source(source)
    outdir.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGBA',(4*tile_w,2*tile_h),(0,0,0,0))
    records=[]
    for i,frame in enumerate(frames):
        fw,fh=frame.size
        ratio=min(max_sprite_w/fw,max_sprite_h/fh)
        outw=max(1,math.floor(fw*ratio))
        outh=max(1,math.floor(fh*ratio))
        if pixel_mode == 'pixel':
            # Pixel-art sampled on integer-sized low-resolution canvas.
            low=(max(1,outw//2),max(1,outh//2))
            frame=frame.resize(low,Image.Resampling.BOX).resize((low[0]*2,low[1]*2),Image.Resampling.NEAREST)
        else:
            frame=frame.resize((outw,outh),Image.Resampling.LANCZOS)
        frame=tidy_alpha(frame)
        x=i%4*tile_w+(tile_w-frame.width)//2
        y=i//4*tile_h+tile_h-8-frame.height
        sheet.alpha_composite(frame,(x,y))
        p=outdir/f'{i+1:02d}_{DIRECTIONS[i]}.png'
        cell=Image.new('RGBA',(tile_w,tile_h),(0,0,0,0))
        cell.alpha_composite(frame,((tile_w-frame.width)//2,tile_h-8-frame.height))
        cell.save(p,optimize=True)
        records.append({'index':i+1,'direction':DIRECTIONS[i],'source_bbox':rects[i]['rect'], 'sheet_cell':[i%4,i//4], 'png':p.name, 'final_size':[frame.width,frame.height]})
    outfile=outdir/'WYO_NPC_Cavaleiro_8_Direcoes.png'
    sheet.save(outfile,optimize=True)
    manifest={'format':'WYO-ASSET-STUDIO','version':2,'tool':'Reference Sheet Processor',
              'operation':'extract_normalize_existing_frames','directions':8,
              'layout':'2x4','columns':4,'rows':2,'cell_size':[tile_w,tile_h],
              'dimensions':list(sheet.size),'background':'transparent',
              'source_notice':'Pre-existing visual frames; processor does not create missing viewpoints.',
              'frames':records}
    (outdir/'project.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    check=sheet.getchannel('A').getextrema()
    if check[0] != 0 or check[1] < 250:
        raise RuntimeError('Validação de transparência falhou')
    if len(records)!=8:
        raise RuntimeError('Validação de frames falhou')
    return outfile,manifest


def main():
    p=argparse.ArgumentParser(description='WYO Studio: extrair e organizar 8 quadros de uma referência existente.')
    p.add_argument('--input',type=Path,required=True,help='PNG de referência com 8 direções já desenhadas em 2x4')
    p.add_argument('--output',type=Path,default=Path('exports/npc_cavaleiro'))
    p.add_argument('--tile-width',type=int,default=224)
    p.add_argument('--tile-height',type=int,default=256)
    p.add_argument('--pixel-mode',choices=['original','pixel'],default='original')
    args=p.parse_args()
    with Image.open(args.input) as src:
        path,meta=render_sheet(src.convert('RGBA'),args.output,tile_w=args.tile_width,tile_h=args.tile_height,pixel_mode=args.pixel_mode)
    print(f'WYO STUDIO EXPORT: {path} | {meta["dimensions"]} | 8 quadros | alfa RGBA OK')

if __name__=='__main__': main()