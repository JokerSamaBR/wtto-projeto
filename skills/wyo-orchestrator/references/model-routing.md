# Model routing and usage measurement

_Last verified against OpenAI public model/ Codex documentation: 2026-10-24. Recheck availability, pricing and config when installing._

| Task | Suggested if available | Reasoning | Delegate? |
|---|---|---|---|
| One-line fix / narrow request | Luna or Sol already active | low | No |
| Search, file inventory, dependency map | GPT-6 Luna | low | Yes, if separate from another useful stream |
| Bounded tests / regression review | GPT-6 Luna | medium | Yes, if independent |
| Architecture and implementation | GPT-6.1 Sol | medium | Root |
| Cross-system security / subtle economy invariants | GPT-6.1 Sol | high | Root; optional separate review |
| Unusually hard unknown issue | GPT-6 Astra, if offered | task-specific | Only explicit cost/quality justification |

## What the skill can and cannot control

- The Codex parent config and project-scoped agent TOML templates request a model and effort. Availability depends on account and rollout.
- Child agents consume additional context and tokens. Two agents are a **ceiling**, not an instruction to always spawn two.
- API dollars, ChatGPT-included limits and purchased Codex credits **are different meters**. Don't convert between them without official current rates.
- For a controlled comparison, track: task, parent/child model, input tokens, cached input tokens, output tokens, wall time, quality and retries. Compare one-agent against two-agent runs with the *same* work and acceptance criteria.
- Abort delegation when context duplication, unfinished work or lack of clear boundaries overtakes the benefit.

Official references:
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://developers.openai.com/api/docs/guides/model-selection
- https://developers.openai.com/api/docs/models

If a model isn't in the runtime selector, **do not pretend** it is usable. Pick from the actual models available.
