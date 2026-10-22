# WYO Procedural Art Studio 1.0

Gerador **gratuito, offline e sem dependências para uso visual**, com upload local de até cinco referências, análise de paleta, centro visual aproximado, posicionamento manual, seis estilos matemáticos, transparência e renderização do PNG final na resolução selecionada.

## Abrir sem instalar nada

1. Extraia o ZIP e abra `gerador.html` em Chrome, Firefox ou Edge.
2. Insira uma ou até cinco imagens PNG/JPG/WebP em **Imagem de referência**.
3. Defina o **tipo de asset**, explique quais detalhes precisam permanecer intactos, escolha um efeito e uma paleta.
4. Em **Como usar referência**, selecione:
   - **Extrair cores + foco visual:** não exibe a referência no PNG; adapta o efeito à paleta e à localização aproximada do assunto.
   - **Preservar imagem + adicionar efeito:** usa a referência principal como camada intacta e sobrepõe o efeito procedural.
   - **Ignorar imagem:** usa a configuração de cores manual.
5. Clique no canvas para determinar o centro do efeito; ajuste intensidade, detalhes, brilho, rotação, transparência e dimensão.
6. Exporte o **PNG** e o **Projeto JSON**. O JSON contém os parâmetros e as referências embutidas; pode ficar grande.

## Para usar com Codex ou automatização Python

O arquivo `AGENTS.md` contém as instruções que o Codex pode ler quando o diretório é usado como projeto. Requer apenas para automação (não para abrir o HTML):

```bash
pip install playwright
python -m playwright install chromium

# Reproduzir arquivo .json criado na interface
python render_codex.py --project "WYO_rift_27570.json" --out "minha_arte.png"

# Criar imagem de fundo PNG, adaptando as cores da imagem de referência
python render_codex.py --reference "exemplo.png" --mode celestial --size 1920x1080 --out "loading.png"

# Preservar personagem da referência e adicionar portal atrás/sobre o arquivo, sem gerar um personagem novo
python render_codex.py --reference "personagem.png" --mode portal --size 2048x2048 --reference-mode composite --background transparent --out "portal_personagem.png"

# Gerar 10 variações determinísticas
python render_codex.py --mode rune --size 512x512 --seed 27570 --batch 10 --out "runa.png"
```

Ao aplicar efeitos com o modo `composite`, a imagem de referência é posicionada como camada e o efeito é desenhado por cima; se o efeito não deve cruzar o personagem, faça mascaramento no Krita. Não há detecção automática de camadas anatômicas.

## Para personagens, MVPs, sprites e logos

Canvas procedural **não é um modelo de geração de imagens** e não consegue reproduzir sozinho, com fidelidade fotográfica/artística, personagens anime ou reconstruir sprites de oito direções apenas de uma imagem. Nesses casos, use as imagens como referência junto a **ComfyUI local + Krita AI Diffusion**, mantendo o HTML como compositor de efeitos e gerador de paletas.

- **ComfyUI:** https://github.com/comfy-org/ComfyUI
- **Krita AI Diffusion:** https://github.com/Acly/krita-ai-diffusion
- **Krita:** https://krita.org/
- **LibreSprite** (pixel art): https://libresprite.github.io/

Esses softwares têm versões gratuitas/open-source. A geração por IA depende do modelo instalado, cuja licença comercial precisa ser verificada, e do hardware local. Nenhum desses motores de IA está embutido ou automaticamente instalado no `gerador.html`.

## Regras WYO fixas para Codex

- Identidade WYO: estilo Ragnarok Online anime/fantasia, nitidez, contornos limpos, paleta coerente; manter o logo original quando enviado.
- Personagens: preservar anatomia, mãos, contato físico, vestuário, silhueta e outros detalhes que o usuário marcar como invariáveis.
- Sprites: 8 direções independentes em grade 2×4, sem espelhar frames, trocar slots, girar sem autorização ou deslocar o pivô.
- Banner/arte de site: produzir assets separados sem texto quando solicitado; dimensões e transparência exatas.
- Efeitos: registrar `seed`, dimensões, máscara/fundo, paleta e arquivo de referência; salvar sempre PNG e projeto JSON.
- Não criar falsas promessas de identidade 1:1 quando houver uma fase generativa por IA. Comparar visualmente a saída com a referência original.


## Novidade na v1.1

Agora o estúdio inclui o modo **RO Sprite Builder**, pensado para quando você enviar imagens de referência e quiser orientar o Codex a gerar sprites no estilo Ragnarok Online.

### Fluxo recomendado
1. Abra `gerador.html`.
2. Carregue a imagem de referência.
3. Ative **RO Sprite Builder**.
4. Escolha `Formato do sprite`, `Alvo da referência` e `Saída do sprite`.
5. Para sprites, use **PNG sem fundo**.
6. Exporte o **Projeto JSON** ou copie a especificação para o Codex.