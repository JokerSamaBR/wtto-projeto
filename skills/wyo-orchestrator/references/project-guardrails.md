# WYO project boundaries

Read only the subsections relevant to the current task. These are stable design constraints, **not** a replacement for inspecting the current code.

## Protected reference

- `JokerSamaBR/rathena-wyo-clean`: read-only code reference. A direct user request to edit its README is the sole exception, and must not change other files.
- Implement, compile and test in a separate development copy or working repository. Verify the Git remotes before any push.

## rAthena / Ragnarok

- Keep custom AutoAttack / `@afk`; do not reactivate/remove the older `@autofarm` clone casually.
- Preserve custom Population Engine, rate seasons and all already-approved systems. Don't assume simulated characters are real players.
- Yggdrasil Rifts: preserve implemented progression/registrations, Draco integration and approved scripts. Assess *actual* active loader paths before enabling anything.
- Do not duplicate Draco Forge NPCs or marketplace deliveries. Protect item rewards against duplication and lost-delivery flows.
- Preserve 4th classes, 275/70 balance and distinct character rate modes. Verify source/config rather than assuming historical values always match deployment.

## FluxCP and marketplace economy

- For **theme-only** work edit `themes/yggdrasil_atlan/` and installed addon theme views under `addons/.../themes/yggdrasil_atlan/`; don't modify `config/`, `modules/` or FluxCP core just for cosmetics. No SQL tables merely for visual behavior.
- ItemSell ↔ CharSell: active ItemSell listings prevent listing that character in CharSell; CharSell listing blocks item-market operations. Enforce in UI *and* backend.
- WYO Support rewards (cash/items/zeny) must never target a CharSell-listed character; server-side revalidation is mandatory.
- User-facing messages: English default, Portuguese (Brazil), Spanish. Do not auto-translate editorial content without explicit scope.
- Payment and reward changes require independent input validation, authorization, idempotency and regression review.

## WYO artwork

- Cutins and sprite sheets share a consistent Ragnarok-inspired WYO visual language. Do not substitute a different character or distort proportions.
- Sprite sheets have fixed 2×4 eight-direction slots. Do not swap, mirror or regenerate correct views while fixing one incorrect direction. Transparent PNG where requested.
- For image assets, user approval of the look does not mean each direction is correct: verify every individual view.

## Delivery

- Keep changes narrowly scoped, documented and testable. Show actual modified files and actual checks performed; no fictitious test claims.
