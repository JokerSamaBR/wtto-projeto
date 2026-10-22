# WYO Asset Studio v2.0

Estúdio de assets **gratuito e local**: Sprite Forge, Logo Forge, FX Studio e Reference Lab.

## Uso

Abra `index.html` no navegador. Sem builds, APIs, contas ou dependências JS. Tudo opera localmente.

**Sprite Forge:** o cavaleiro frontal é um template vetorial próprio (em `assets/templates/knight-front.svg`) que o navegador rasteriza no Canvas em PNG transparente. Estilo de pixels configurável. Também permite importar um PNG com transparência ou fundo branco/preto e compor sheets com 4/8 arquivos únicos fornecidos pelo usuário, sem gerar frames falsos.

**Logo Forge:** tipografia com bordas e relevo por Canvas, mascote e ornamentos opcionais. Logo procedural novo; não copia fontes/curvas personalizadas de logotipos de referência.

**FX Studio:** fenda, portal e runas determinísticos por seed.

**Reference Lab:** importar até 5 arquivos, obter paleta e fazer recorte/chroma key simples. **Não é uma IA**: não identifica automaticamente personagens ocultos, não reconstrói direções inexistentes, não reproduz com fidelidade qualquer logo.

### Exportação por código para Codex

```bash
pip install playwright
python -m playwright install chromium
python render/render_codex.py --project presets/cavaleiro_masculino_frontal.json --output cavaleiro.png
```

JSON v2 mantém a descrição completa e pode incluir referências locais (data URLs). Caso envie um JSON com imagens embutidas ao Codex, evite colocá-lo em repositórios públicos sem conferir licenças.

## Roteiro

Para replicar livremente personagens complexos e ângulos inéditos, próximo módulo recomendado: integração local com **ComfyUI** e modelo open-weight licenciado adequadamente, com img2img/controle de estrutura, treinamento opcional de LoRA, máscaras e validação por direção. Essa integração **não está implementada** nesta versão.

## v2.1 — Sprite Sheet Lab (8 direções reais)

- Abra `sprite-sheet-lab.html` ou o link **Sprite Sheet Lab** no menu do Studio.
- Importe uma **imagem que já contenha oito vistas** (4 colunas × 2 linhas).
- O Studio localiza espaços transparentes, recorta cada direção, ajusta escala e alinhamento e exporta sheet PNG transparente de forma reproduzível.
- Também exporta oito PNGs individuais e manifesto JSON. Não inverte nem duplica direções.
- Por código, instale `pip install pillow numpy` e rode:

```bash
python render/sheet_pipeline.py --input sua_sheet_de_referencia.png --output exports/npc_cavaleiro
```

**Limite:** esta função processa frames fornecidos. Não cria vistas inéditas a partir de um único personagem frontal. A demonstração foi processada de uma sheet de oito desenhos pré-existentes; não foi desenhada inteiramente pelo motor procedural.