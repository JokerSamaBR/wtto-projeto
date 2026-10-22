# Regras para Codex — WYO Asset Studio v2

- Tratar o render do browser como fonte de verdade. Reproduzir PNG pelo `render/render_codex.py`.
- Código offline e gratuito. Nunca usar APIs pagas como dependência obrigatória.
- Preservar os três engines independentes e esquema `WYO-ASSET-STUDIO` versão 2.
- Nunca declarar que o motor de vetores reproduz automaticamente imagens enviadas.
- Nunca gerar direções por espelhamento; sheets só com frames distintos.
- Para sprites PNG, manter canal alfa verdadeiro, enquadramento e grade.
- Não publicar imagens privadas/referências em GitHub sem indicação do usuário.
- As templates existentes em v1 devem continuar acessíveis; publicar v2 em pasta separada.
- Validação: JS sem erros, export PNG, alfa, viewport, e teste do projeto JSON.

## v2.1 — Sprite Sheet Lab
Usar `render/sheet_pipeline.py` em sprites que já contenham 8 direções. Renderizar PNG RGBA transparente, 4 colunas × 2 linhas, separar oito quadros sem espelhar nem repetir, gerar manifesto. Nunca afirmar que este pipeline cria novas vistas a partir de imagem frontal única.