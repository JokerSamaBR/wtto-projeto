# WYO Codex Orchestrator v1.0

Skill pessoal gratuita para organizar subagentes do Codex nos projetos **World Yggdrasil Online (rAthena/FluxCP)**, Web, Blender e jogos.

**Recomendação:** `gpt-6.1-sol` para o agente principal (Medium) + `gpt-6-luna` para investigação (Low) e revisão (Medium), **somente se disponíveis na sua conta Codex**. Usar no máximo 2 subagentes paralelos, e nenhum para correções simples.

## Instalar no Codex

O comando a seguir instala a skill neste ambiente Codex, se sua versão do CLI `skills` aceitar o repositório e encontrar `skills/wyo-orchestrator`:

```bash
npx skills@latest add JokerSamaBR/wtto-projeto --skill wyo-orchestrator --agent codex --global
```

Para **testar antes de instalar globalmente**, retire `--global` e execute no projeto de desenvolvimento. O comando instala instruções; **não configura automaticamente os modelos e agentes customizados**.

> Antes de executar `npx`, revise as dependências/comandos do instalador externo. A skill publicada aqui contém arquivos de instrução (Markdown/YAML/TOML) e não executa scripts próprios.

## Configuração opcional para projetos grandes

Copie os modelos de configuração apenas para a **cópia de desenvolvimento** (não para `rathena-wyo-clean`):

- [Configuração principal](skills/wyo-orchestrator/templates/.codex/config.toml) → `.codex/config.toml`
- [Agente de leitura](skills/wyo-orchestrator/templates/.codex/agents/wyo_scout.toml) → `.codex/agents/wyo_scout.toml`
- [Agente de revisão](skills/wyo-orchestrator/templates/.codex/agents/wyo_reviewer.toml) → `.codex/agents/wyo_reviewer.toml`
- [AGENTS.md de exemplo](skills/wyo-orchestrator/templates/AGENTS.example.md) — incorpore apenas as regras necessárias ao projeto, sem sobrescrever o seu `AGENTS.md` existente.

Esses arquivos configuram um modelo principal, padrões econômicos de subagentes e no máximo dois subagentes. Se `gpt-6.1-sol` ou `gpt-6-luna` não estiverem no seletor do Codex, altere os nomes para os modelos **realmente disponíveis**.

## Usar

Na conversa com o Codex:

```text
Use $wyo-orchestrator para auditar WYO Yggdrasil Rifts.
Use no máximo 2 subagentes para investigações independentes e delimitadas.
Preserve rathena-wyo-clean (nenhuma edição). Não faça commits nem push nesta tarefa.
Entregue evidências por caminho/linha e um plano de correção verificável.
```

Em tarefas curtas basta pedir a correção normalmente: **não é necessário convocar vários agentes**.

## O que esta skill faz (e não faz)

- Instrui o Codex a delegar com escopo, escolher modelos econômicos e validar resultados.
- Mantém instruções WYO e limites por projeto sem injetar todo o histórico em cada execução.
- **Não** ativa modelos ausentes do seu plano nem garante economia fixa de créditos.
- **Não** protege permissões por si só: configure sandbox/autorizações no Codex.
- **Não** modifica os projetos e não instala mem0 nem outros serviços.

## Arquivos

- [Skill principal](skills/wyo-orchestrator/SKILL.md)
- [Regras WYO](skills/wyo-orchestrator/references/project-guardrails.md)
- [Modelos e custos](skills/wyo-orchestrator/references/model-routing.md)
- [Metadados Codex](skills/wyo-orchestrator/agents/openai.yaml)

### Créditos

Inspirado no conceito de delegação econômica da [Orchestrate de Rafael Quintanilha](https://github.com/rafaelquintanilha/skills/blob/master/skills/orchestrate/SKILL.md), com conteúdo e restrições próprias WYO.

Documentação oficial: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Config Reference](https://learn.chatgpt.com/docs/config-file/config-reference), [Model selection](https://developers.openai.com/api/docs/guides/model-selection).
