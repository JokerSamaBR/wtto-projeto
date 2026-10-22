#!/usr/bin/env python3
"""WYO Procedural Art Studio: renderiza PNG no Chromium via Canvas local."""
from __future__ import annotations
import argparse
import base64
import copy
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
MODES = ('rift', 'portal', 'rune', 'magic', 'celestial', 'texture', 'spritebuilder')

def main():
    a = argparse.ArgumentParser(description="Exportar arte procedural WYO como PNG.")
    a.add_argument('--project', type=Path, help='JSON exportado pelo gerador.html')
    a.add_argument('--out', type=Path, default=Path('WYO_sprite.png'))
    a.add_argument('--mode', choices=MODES)
    a.add_argument('--size', default=None, help='Ex.: 512x512')
    a.add_argument('--background', choices=('transparent', 'dark', 'light'))
    a.add_argument('--seed', type=int)
    a.add_argument('--batch', type=int, default=1)
    args = a.parse_args()

    if not 1 <= args.batch <= 30:
        a.error('--batch deve ser entre 1 e 30')
    project = json.loads(args.project.read_text(encoding='utf-8')) if args.project else None
    if project is not None and project.get('format') != 'WYO-PROCEDURAL-STUDIO':
        a.error('O arquivo não é um projeto WYO.')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.set_content((HERE / 'gerador.html').read_text(encoding='utf-8'))
        if project:
            page.evaluate('async x => await window.WYOStudio.loadProject(x)', project)
        project = page.evaluate('window.WYOStudio.getProject()')
        st = project['settings']
        for flag, key in [('mode','mode'),('size','size'),('background','bg'),('seed','seed')]:
            val = getattr(args, flag)
            if val is not None:
                st[key] = val
        if st['mode'] not in MODES:
            a.error('Modo inválido.')
        w, h = map(int, st['size'].split('x'))
        if not 1 <= w <= 4096 or not 1 <= h <= 4096:
            a.error('Resolução inválida.')
        args.out.parent.mkdir(parents=True, exist_ok=True)
        for i in range(args.batch):
            obj = copy.deepcopy(project)
            obj['settings']['seed'] = (int(st['seed']) + i) % 4294967295 or 1
            page.evaluate('async x => await window.WYOStudio.loadProject(x)', obj)
            uri = page.evaluate('async () => await window.WYOStudio.renderPNG()')
            if not uri.startswith('data:image/png;base64,'):
                raise RuntimeError('Renderização PNG falhou.')
            dest = args.out if args.batch == 1 else args.out.with_name(f'{args.out.stem}_{i+1:02d}.png')
            dest.write_bytes(base64.b64decode(uri.partition(',')[2]))
            print(f'OK {dest} | {w}x{h} | seed {obj["settings"]["seed"]}')
        browser.close()

if __name__ == '__main__':
    main()
