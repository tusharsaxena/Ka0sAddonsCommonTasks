# Open questions for the owner

**All questions are ruled (2026-09-26, `OWNER_RULINGS.md`).** Each question keeps its original options and
recommendation for the record, with the ruling in one line under its heading. Where a ruling differs from the
recommendation (Q1, Q11, the README wording) the spec, the plan and `items.tsv` have been amended to match.
Q1 is committed as DR-OW-03; the Q2 measurement itself stays the owner gate DR-OW-02.

---

### Q1. What does X do in each DragHandle host?

**Ruled (see OWNER_RULINGS.md):** ConsumableMaster X sets `macroBar.enabled = false`; AbsorbTracker X sets `units.<unit>.enabled = false` on every bar, the player bar included (no player-bar exception); KickCD gets no X and does not adopt the close option.

| Host | Options | Recommendation |
|---|---|---|
| ConsumableMaster (macro bar) | (a) `macroBar.enabled = false`; (b) `macroBar.locked = true` (hides the strip only); (c) addon-wide `enabled = false` | **(a)**. It matches AuraMaster's "turn this element off", uses the `/cm bar off` path, and leaves macro writes running. (c) stops the macros the player relies on. |
| KickCD castbar strips | (a) `units.<unit>.castbar.enabled = false`; (b) `locked = true`; (c) no X | **(a)** |
| KickCD focus castbar while `units.focus.link = true` | (a) no X while linked; (b) X writes `units.focus.enabled = false` while linked; (c) make `castbar.enabled` a per-unit key that stays per-unit under a link | **(a)**. (b) hides more than the strip suggests; (c) is a schema change for a corner case. |
| KickCD icon-grid strips | (a) `units.<unit>.enabled = false` (grid, cast bar and label); (b) new `units.<unit>.icons.enabled` row (L: schema, default, migration); (c) `locked = true` | **(a)** now; (b) only if you want per-widget symmetry, as its own later change. |
| AbsorbTracker bars | (a) `units.<unit>.enabled = false` per bar; (b) `locked = true` (all three strips); (c) addon-wide disable | **(a)** |
| AbsorbTracker player strip | (a) no X on the player strip; (b) X like the others | **(a)**. Player is the only default-on bar, and it is the most-clicked strip; a misclick leaves the player seeing nothing. |

All options keep positions and write through the existing schema seam (X-01).

### Q2. Buffer: 5000 or 3000, and how it is measured

**Ruled (see OWNER_RULINGS.md):** Recommendation accepted: 5000 if the DR-OW-02 measurement passes, else 3000, with the thresholds as proposed; the measurement stays an owner gate.

- **Options:** (a) 5000; (b) 3000; (c) keep 1500 and raise only the report's trace room some other way.
- **Procedure:** `03_EXECUTION_PLAN.md` §5 (bench at N = 0/1500/3000/5000, width 120 and 200, JetBrains
  Mono, three runs each, median, minus the baseline frame; plus select-all, Ctrl+C, scroll by hand).
- **Proposed thresholds:** copy-open + next-frame ≤ 250 ms at width 120 and ≤ 1 s at width 200.
- **Recommendation:** **5000 if it passes, else 3000.** At 1500 the report (up to 1200 lines) leaves only
  300 lines of trace, so "one copy carries both" is not really true until the buffer rises. Also ship the
  `TIME_COPY` flag (BUF-06b) so the number can be re-checked after a client patch. Please also confirm or
  change the thresholds.

### Q3. Does AuraMaster move onto the shared helper now or later?

**Ruled (see OWNER_RULINGS.md):** (a) Now: AuraMaster moves onto the shared helper in this pass.

- **(a) Now,** in this pass, after its batch branch merges: drop about 110 lines of plumbing, markers per
  STD-08, cap from the library.
- **(b) Later:** re-vendor only; record an accepted deviation from STD-16 until a later AuraMaster batch.
- **Recommendation: (a),** because the re-vendor already happens here, the rule is a MUST, and the
  reference implementation should not be the one that breaks it. If its batch branch is still open when
  every other addon is done, fall back to (b) and file an issue on AuraMaster.

### Q4. What does "works while disabled" require?

**Ruled (see OWNER_RULINGS.md):** (a), and `diagnostics` goes into `LibKa0s-Slash` `LIVE_VERBS`.

- **(a)** The verb is live while disabled, and the report runs **every** section. Sections whose runtime
  state is released print "stood down" instead of empty data; stored config is printed as normal.
- **(b)** While disabled, only identity, lifecycle and settings run.
- **(c)** Only `/<slash> debug diagnostics` must be live (it already is, through `debug`); the top-level
  verb may be refused.
- Separately: should `diagnostics` be the only verb added to the collection-wide live list, via the
  library, or should each host add it?
- **Recommendation: (a), and add it to `LibKa0s-Slash` `LIVE_VERBS`** (thirteenth reserved verb). (a)
  gives a maintainer the most on a "nothing happens" report, which is often a disabled addon. (c) would
  leave the README's step 2 broken for a disabled addon. The library route fixes ten addons in one change
  (see `01_FINDINGS.md` §1, the live-verb table).

### Q5. Does the standard bump minor or major?

**Ruled (see OWNER_RULINGS.md):** (a) Minor, v2.68.0.

- **(a) Minor, v2.68.0.** Precedents: v2.42.0 and v2.52.0 each added a MUST that addons failed until they
  adopted it.
- **(b) Major, v3.0.0.**
- **Recommendation: (a).** Nothing existing is removed or reversed; the change adds one MUST and widens
  the reserved-verb list. A major would also force every addon's X-Standard pointer across a major line
  for a small change.

### Q6. Does the report trigger the Tier-2 `docs/debug.md` requirement?

**Ruled (see OWNER_RULINGS.md):** (a) Every addon ships `docs/debug.md`.

- **(a)** Yes: the report is a debug surface, so every addon ships `docs/debug.md` (AT, PC and WG gain
  new ones; the others extend theirs).
- **(b)** Amend the trigger to exclude the standard report; document it in the README section only.
- **Recommendation: (a).** Each addon's report has different sections and different "never printed"
  rules (secret values, protected APIs); a maintainer reading a pasted report needs that page.

### Q7. What happens to existing dump verbs?

**Ruled (see OWNER_RULINGS.md):** (a) Retire MM `debug diag` and PM `debug dump` as unknown words, no hint; keep the topic dumps.

| Verb | Options | Recommendation |
|---|---|---|
| MM `/mm debug diag` (the same report) | (a) retire, unknown word; (b) retire with a one-line localized hint "use `/mm diagnostics`" that does not run anything; (c) keep as alias | **(a)**. You ruled out any short alias "such as `diag`" by name. A hint keeps `diag` as a recognized word, one edit away from an alias, and it needs its own locale key and test. (b) remains available if you want to help players who were told `diag` in issue threads. (c) contradicts your ruling. |
| PM `/pm debug dump` (the same report) | (a) retire; (b) hint as above; (c) keep | **(a)**: it was never documented in the README. |
| BL `debug scan`, `debug panel`; KC `debug spells/castbar/interrupt/events`; AT/LH `debug events`; MM `recap/identity/feign/tooltip`; CM `/cm dump <target>`; PF `/pfe status` | keep as topics, or fold and retire | **Keep** all of them (debug-logging-§4 MAY), and fold their content into the report as sections where it helps. They are separate topics, not other names for the report. |

### Q8. Should the report cap scale with the buffer?

**Ruled (see OWNER_RULINGS.md):** (a) Fixed cap, `lib.DIAG_MAX_LINES = 1200`.

- **(a)** Keep AuraMaster's formula: `min(1200, MAX_BUFFER - 100)`, as `lib.DIAG_MAX_LINES = 1200`.
- **(b)** Scale: for example `min(MAX_BUFFER / 2, MAX_BUFFER - 100)`.
- **Recommendation: (a).** No survey expects more than about 600 lines (CM, MM worst case), and a fixed cap
  means a larger buffer goes to trace. AuraMaster's `MAX_LINES ≤ 1200` pin stays true.

### Q9. Marker format

**Ruled (see OWNER_RULINGS.md):** (a) Full brand in both markers.

- **(a)** `[Diag] ==== <BrandName> diagnostics begin ====` … `[Diag] ==== <BrandName> diagnostics end: N line(s) ====`
- **(b)** AuraMaster's current text (brand only in the begin marker, short brand).
- **Recommendation: (a),** so a paste that holds reports from several addons can be split, and so the end
  marker proves which report finished.

### Q10. Unknown `debug` words

**Ruled (see OWNER_RULINGS.md):** (a) Each addon keeps its own fallback for unknown words.

- **(a)** Leave each addon's current fallback (toggle, usage, or error-and-list).
- **(b)** Standardize on one.
- **Recommendation: (a).** The rule only needs `diagnostics` checked first and no other word running the
  report. Standardizing touches pinned tests in PC, WG and KC for no user gain.

### Q11. Privacy in a public issue

**Ruled (see OWNER_RULINGS.md):** No privacy rules. Nothing is redacted, because users send the report to the owner privately; no BankLedger README note.

- Other players' names (target, party, group leader, whisper target), and group titles and voice-chat
  text: **never printed** (present/absent or set/unset instead). Recommend yes.
- The player's own characters (LootHistory alts): count, or `char#N` labels. Recommend `char#N`, which
  keeps "rows from different characters" visible.
- WhatGroup's group title (another player's text): print it or not? **Recommend not** (length only).
- BankLedger gold balances and guild-bank contents: print them, with a one-line note under the README
  section saying the report includes balances and can be trimmed. **Recommend print with the note**, since
  "wrong amount" bugs need them. This adds one sentence to BankLedger's README beyond the owner's wording;
  please confirm that is acceptable, or say the note goes in `docs/debug.md` only.

### Q12. Escapes: strip, or double `|`?

**Ruled (see OWNER_RULINGS.md):** Strip by default; PrettyChat format values use `out:escape`.

- **Recommendation:** strip by default (clean Copy text); PrettyChat's format values use `out:escape`
  (`|` → `||`), because the escapes are what is being reported and `||` pastes back into `/pc set`.

### Q13. Library-absent behavior

**Ruled (see OWNER_RULINGS.md):** (a) One localized chat line, nothing written.

- **(a)** One localized chat line (the existing placeholder), nothing written. **(b)** Print the report to
  chat.
- **Recommendation: (a).** A report of hundreds of lines in chat is worse than none, and ConsumableMaster's
  chat fallback would otherwise flood.

### Q14. Does the report show the console itself?

**Ruled (see OWNER_RULINGS.md):** Yes, the report shows the console.

- **Recommendation: yes** (AuraMaster already does). The README's step 3 stays exactly as you wrote it; it
  still covers a player who closed the window afterwards.

### Q15. Where does the helper live, and do hosts have to use `DebugVerb`?

**Ruled (see OWNER_RULINGS.md):** Secondary file `DebugLogDiagnostics.lua`; `DebugVerb` optional.

- Helper: **a secondary file `DebugLogDiagnostics.lua`** (recommended; `DebugLog.lua` would otherwise pass
  1000 lines) vs inline in `DebugLog.lua`.
- `DebugVerb`: **optional** (recommended). The standard requires the behavior; hosts with topic words
  (KC, BL, MM) keep their own dispatch.

### Q16. AuraMaster sequencing

**Ruled (see OWNER_RULINGS.md):** (a) Wait for the batch-8/9/10 branch to merge.

- **(a)** Wait until batch-8/9/10 merges into master, then branch.
- **(b)** Stack on the batch branch tip now, at a recorded commit.
- **Recommendation: (a).** The batch branch is live, and batch 10 is now committed on it (tip `d3e0118`, `B10-R2`, as of 2026-09-26); stacking would
  couple this plan to another workflow's rebases. AuraMaster already complies apart from the re-vendor and
  migration, so waiting costs little.

### Q17. LibKa0s release shape

**Ruled (see OWNER_RULINGS.md):** (a) v1.60.0 stacked on v1.59.0; `--no-ff` or fast-forward, never squash; both tags pushed together.

- **(a)** v1.60.0 stacked on the local v1.59.0 (recommended; AuraMaster's batch-8 branch already
  vendors v1.59.0).
- **(b)** Re-cut v1.59.0 with everything. Rejected: it moves a tag a consumer already vendors.
- Please also confirm: merge `--no-ff` or fast-forward, never squash, and push both tags together.

### Q18. Push authorization

**Ruled (see OWNER_RULINGS.md):** Push the feature branches at checkpoints (DR-OW-04 authorized).

- Authorize pushing `feat/2026-09-25-diagnostics-rollout` at checkpoints (DR-OW-04)? Until you do, all work
  stays local.

### Q19. README note beyond the three steps

**Ruled (see OWNER_RULINGS.md):** No extra README note.

- Should the section also mention "run it out of combat for the fullest report" (AuraMaster, KickCD,
  MultiMeters, PartyFrameEnhanced read less in combat)?
- **Recommendation: no.** Keep your wording exactly; the report itself says "unreadable in combat" where it
  applies, and `docs/debug.md` explains it.

### Q20. A shared conformance case in the test kit?

**Ruled (see OWNER_RULINGS.md):** (b) Shared `test_diagnostics_contract.lua` in the kit, with the kit revision bump in v1.60.0.

- **(a)** Each addon writes its own STD-19 cases (the plan as drafted: eleven copies of the same eight
  assertions).
- **(b)** LibKa0s `testkit/` ships one `test_diagnostics_contract.lua` that every consumer runs against its
  own dispatcher: both forms, while disabled, append, ungated, markers, `diag` not running it. Addons keep
  only their domain cases.
- **Recommendation: (b), if you accept a kit revision bump in v1.60.0.** It is the kit's existing pattern
  (`test_layout_cap.lua`, `test_eol.lua`), and eleven hand copies of one contract drift. Cost: `Kit.VERSION`
  moves, so every `-01` re-vendors the kit too, which it does anyway.

### Q21. Publish the standard before the addons comply?

**Ruled (see OWNER_RULINGS.md):** (a) Publish at DR-OW-07, and the owner is asked before WowAddonStandards or wow-addon is merged.

- `/wow-addon:revendor-standards` and `/wow-addon:standards-audit` read the standard from GitHub `master`,
  not from the local branch. The `-07` items therefore need WowAddonStandards v2.68.0 (and the wow-addon
  text) merged and pushed first (DR-OW-07), while some addons are still on the rollout branch.
- **(a)** Publish at DR-OW-07, after M3 and before M4 (recommended). For a short window the published
  standard has a MUST that the released addons do not meet yet. v2.42.0 and v2.52.0 had the same window.
- **(b)** Publish everything together at DR-OW-06, and do the `-07` pointer edits by hand against the
  local branch without the two skills.
- **Recommendation: (a).**

