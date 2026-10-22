#!/usr/bin/env python3
"""Exportação reproduzível de PNG através do código real do navegador (offline)."""
import argparse
import base64
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="WYO Asset Studio v2 — PNG local")
    parser.add_argument("--project", type=Path, default=ROOT / "presets" / "cavaleiro_masculino_frontal.json")
    parser.add_argument("--output", type=Path, default=Path("WYO_cavaleiro.png"))
    parser.add_argument("--size", type=int, choices=[256,512,1024,2048])
    args = parser.parse_args()
    project = json.loads(args.project.read_text(encoding="utf-8"))
    if args.size:
        project["settings"]["size"] = args.size
    with sync_playwright() as pw:
        exe = os.environ.get('WYO_CHROMIUM')
        if not exe and not Path(pw.chromium.executable_path).exists():
            for candidate in ('/usr/bin/chromium', '/usr/bin/google-chrome'):
                if Path(candidate).exists():
                    exe = candidate
                    break
        browser = pw.chromium.launch(headless=True, executable_path=exe, args=['--no-sandbox'])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        html = (ROOT / 'index.html').read_text(encoding='utf-8')
        css = (ROOT / 'styles.css').read_text(encoding='utf-8')
        html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css}</style>')
        for path in ('scripts/template-data.js','scripts/engines/sprite.js', 'scripts/engines/logo.js','scripts/engines/fx.js','scripts/main.js'):
            src = (ROOT / path).read_text(encoding='utf-8')
            html = html.replace(f'<script src="{path}"></script>', f'<script>{src}</script>')
        page.set_content(html,wait_until='load')
        page.evaluate('async data => window.WYOStudioV2.loadProject(data)', project)
        uri = page.evaluate('async () => window.WYOStudioV2.renderPNG()')
        browser.close()
    if not uri.startswith('data:image/png;base64,'):
        raise RuntimeError('Exportação não retornou PNG')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(base64.b64decode(uri.partition(',')[2]))
    print('OK', args.output)

if __name__=='__main__':
    main()