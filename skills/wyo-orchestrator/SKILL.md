---
name: wyo-orchestrator
description: Coordinate cost-conscious Codex subagents for World Yggdrasil Online (rAthena, FluxCP), Ragnarok assets, web and game-development projects. Use for cross-system audits, scoped code investigations, integrations or complex changes; avoid delegation for tiny fixes.
---

# WYO Codex Orchestrator v1.0

Use Codex's native subagents, not a separate agent service. This skill is guidance, not a token quota or a permission boundary. The root agent owns architecture, user communication, integration, testing and final delivery.

## 1. Protect the source of truth

- `JokerSamaBR/rathena-wyo-clean` is a **protected reference**: no edits, commits or pushes. Only edit its README if the user explicitly requests that specific change.
- For code work, use a separate local clone / working branch. Never treat a protected reference as the write target.
- Do not silently replace established systems, schemas, rAthena sources, NPC behavior, marketplace rules, or player-facing translations.
- Read `references/project-guardrails.md` only for relevant WYO tasks. Do not send it wholesale to every subagent.
- Skills don't enforce filesystem protection: configure the parent session's permissions/sandbox accordingly.

## 2. Decide single agent vs delegation

Default to **one agent**. Delegate only if at least two independent workstreams have clear, non-overlapping inputs and outputs, or independent review materially reduces a high-impact risk.

Do not delegate:
- One small bug, one file, a simple design tweak or a quick lookup.
- Dependent tasks that need to modify the same files.
- Tasks where copying context costs more than the expected gain.
- A long-running command that can simply run as a command.

Default to **at most two subagents concurrently**. Additional agents only with a concrete case and the user's express preference. Do not chain-delegate by default. Reuse a subagent with relevant context instead of spawning duplicates.

## 3. Route by actual capability, not role titles

If available in the user's Codex:
- **Root:** `gpt-6.1-sol`, `medium` for architecture, integration, changes and final checks; `high` when warranted for security / severe regressions.
- **Scout:** `gpt-6-luna`, `low` for read-heavy searches and dependency mapping.
- **Review:** `gpt-6-luna`, `medium` for bounded regression checks; escalate critical ambiguities to root Sol.
- **Rare escalation:** Astra only if available and the task justifies the additional cost.

If a model is unavailable, select an actually offered model and disclose the substitution. Never claim to have confirmed a runtime model when only requesting its name. Higher reasoning is not a substitute for missing files.

Refer to `references/model-routing.md` for routing details and how to measure consumption.

## 4. Delegate one bounded outcome at a time

Before spawning, specify: role, intended model/effort or inherited setting, scope, exact file/path ownership, read/write permission, expected evidence, completion condition and maximum useful output.

Scouts and reviewers are **read-only by instruction**; the root implements edits. Their instructions alone do not establish a read-only sandbox.

Example:
- Scout: inspect active Rift loaders and item/instance IDs; return concrete paths + line references; no changes.
- Reviewer: inspect reward delivery and character eligibility; return reproducible risks with evidence; no changes.
- Root: resolve inconsistencies, patch **only in the development copy**, run checks and summarize the verified result.

Use evidence-oriented reports: `Finding | Path/line | Evidence | Risk | Recommended action`. Cap reports at roughly 8 meaningful findings, without dumping entire files or large logs.

## 5. Stop waste, verify meaningful work

- Read the smallest necessary file ranges; avoid repeated repository-wide scans.
- Stop/redirect agents that duplicate work or encounter a wrong assumption.
- Integrate returned findings; subagent statements are not proof.
- Run targeted validation for changed files (e.g. `php -l`, syntax/security checks, build/log checks for rAthena). Do not claim real runtime validation without running it.
- Preserve EN as default and PT-BR/ES choices in player-facing WYO surfaces. Keep existing approved behavior and economic protections.
- Never push or commit to GitHub unless the user's request calls for publication.
- Do not create tests, migrations, backup archives or formatting changes unrelated to the requested change.
- Report changed paths, what was checked, remaining uncertainties and any estimated tokens/credits **only when supported by measured usage**.

## Invocation

Say: `Use $wyo-orchestrator para auditar as Yggdrasil Rifts, no máximo dois subagentes econômicos. Não modifique rathena-wyo-clean.`

The provided `templates/.codex/` files are *optional examples* for a development copy, not auto-applied by installing the skill.
