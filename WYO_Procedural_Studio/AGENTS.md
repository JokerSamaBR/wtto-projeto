# Instruções para o Codex — WYO Procedural Art Studio

O gerador principal é `gerador.html` (Canvas 2D puro). O renderer de automação `render_codex.py` usa Chromium com Playwright para produzir **a mesma renderização** a partir do arquivo JSON. Nunca substitua um projeto existente ou descarte camadas/refs do usuário sem autorização.

## Passos operacionais

1. Receba as imagens de referência originais; identifique o que deve ser preservado de forma literal e o que é passível de geração procedural.
2. Leia `settings` e `guidance` do JSON exportado. `settings.referenceData` tem a referência primária em data URI; `settings.additionalReferences` pode conter mais imagens `{name,data}`. Não compartilhar esses dados como log ou resposta bruta.
3. Para cenas abstratas, fundos de site, texturas, partículas, magia, runas, portais ou fendas: execute `python render_codex.py --project <arquivo>.json --out <arquivo>.png`.
4. Para composições com arte pronta: defina `refMode="composite"`; a imagem é preservada e efeitos são inseridos sobre ela. Trate separação em profundidade/oclusão com máscaras manuais quando necessário.
5. Para personagem/NPC/monstro/ilustração original: NÃO invente que o Canvas cria artes anatômicas a partir de referências; use ComfyUI + Krita AI Diffusion local com image-to-image/ControlNet/inpainting, conforme modelo instalado e licença. Use este projeto para paletas, overlays e componentes geométricos, não para reconstrução de pessoas.
6. Para sprite sheet 2×4: faça comparação frame a frame. Respeite 8 direções únicas sem flip automático, pivô constante, transparência e slot 1:1.
7. Para imagens de site: preserve layout e logos fornecidos e gere PNGs separados por componente sem inserir texto não solicitado.
8. Entregue PNG na resolução pedida + projeto JSON com seed, cores e referências. Se usar um modelo gerativo, registre o fluxo real; nunca afirme fidelidade perfeita sem validação.

## Comandos

```bash
python render_codex.py --help
python render_codex.py --project arte.json --out arte.png
python render_codex.py --reference exemplo.png --reference-mode composite --mode rift --size 1920x1080 --out arte.png
```

## Integração futura, separada da parte procedural

ComfyUI opera localmente; usar os workflows oficiais de image-to-image, inpainting e control guides. O projeto atual não depende de API, não instala checkpoints, não inicia ComfyUI e não transmite as referências a servidores. Não ligar API/cloud paga automaticamente.


## v1.1 — Observações para agentes

Use `spritebuilder` quando o usuário pedir sprites RO a partir de referência. Não prometa reconstrução perfeita pelo Canvas; o Canvas organiza a especificação, paleta, foco e exportação, enquanto a etapa fiel de sprite deve ser conduzida por image-to-image / pipeline controlado. Sempre que `spriteBg=transparent`, a saída final deve ser `.png` sem fundo.