## Plan critic: resolutions

**What I checked.** I read all 158 items against OWNER_SCOPE, the cluster table in 01_CONSOLIDATED_FINDINGS.md, the revendor command spec, `resume-state.sh` / `next_args.py`, and the live trees where a claim needed proof.

**Mechanical checks.** There were none to fix: no untraced or doubly-traced findings, no unknown dependencies, and no out-of-scope findings traced. After the patches all 251 in-scope findings are still traced exactly once. The plan has 164 items, every dependency resolves, and the graph has no cycles.

**Order checks.**
- WS-01 is the first WowAddonStandards item and WS-11 closes v2.77.0.
- LK-12 is still the last LibKa0s item.
- Every RV item depends on LK-12, and every STD item depends on WS-11.

### Fixes (25 patches)

**1. Cross-repo handoffs nobody owned (new DC-15; DC-06 split).**
- WS-01's handoff H-01 had no dev-copilot item. It says the harvest command (`wow-harvest-standards.md:152`) and the audit agent (`:108`) must follow the changelog to `standards/CHANGELOG.md`.
- WS-03 hands the dev-copilot copy of check (e) to "the dev-copilot planner", but DC-06 only mirrored it conditionally ("if it has landed").
- WS-10 says `check-standard.sh` runs "on demand and by sync-docs", but no item edited the sync-docs profile.
- dev-copilot's `README.md:3` still names standard v2.76.0.
- DC-06 was also an L item mixing two concerns: a new doc hub and the audit-agent prompt fixes.

DC-06 now covers the hub only (DC-A-01/02/03, effort M). The new DC-15 owns the agent and spec changes (DC-A-05, WAS-A-20, DC-A-10) plus the four handoffs above. It depends on WS-01, WS-03, WS-10 and WS-11, so it reads only the closed standard. DC-12, the US-English sweep, now also depends on DC-15.

**2. Missing M1 cross-repo dependencies.**
- DC-09 and LK-07 depend on WS-07, which defines the durable-citation form both of them write.
- LK-12 depends on WS-11, because its README standard pointer reads the WowAddonStandards branch and must cite the closed v2.77.0.

**3. Resumability holes.**
- LK-12 and LH-14 each made two commits starting with `<ID>: `. Resume-state would mark the item done after the first commit, before the release record or tag existed.
  - The first commit is now `ID (1/2): `, which fails the id regex, so only the final commit marks the item landed.
  - LK-12 gains recovery steps: create a missing tag, and finish LK-05's #43 close if it was interrupted.
- AM-STD now relabels #22 and writes its exceptions row before the commit, so a landed AM-STD implies the relabel happened.
- DC-14 (deleting `origin/main` on the owner's go-ahead) could have left M1 incomplete forever. It now writes an explicit "deferred to the owner-approved finalize" exceptions row at the M1 checkpoint.

**4. Inconsistent re-vendor items.**
- RV-KC allowed a red commit ("the M3 items clear them, KC-STD green at the latest"). That contradicts the revendor command, which fixes contract-change blockers in the re-vendor commit, and every other RV item. It now has to end green, and a behavioural red stops the item and becomes a KC-00 item.
- RV-PC contradicted itself on the span-bundle file set (2 files vs 4). RV-MM copied the shape of a per-tag bundle. Both now say the span bundle holds `01_DELTA.md` and `05_SUMMARY.md` only, as the command requires.

**5. A cluster fixed in only some addons (C27, dead bare-global `GetAddOnMetadata` rung).**
- LK-06, MM-07 and PM-09 remove the rung.
- BankLedger, ConsumableMaster, PartyFrameEnhanced and WhatGroup have the identical dead rung in `core/EnvSetup.lua`, confirmed by grep, but no finding names them.
- I added four small test-first items (BL-05, CM-09, PF-06, WG-07) with no finding ids, and moved each repo's STD item after its new item.
- **This is a small scope addition beyond the finding list.** I made it for consistency under the owner's standing autonomy; the owner can drop the four items without affecting any traced finding.

**6. Item too big for one review.**
- LH-08 (effort L) peeled two different files in one commit.
- It is now two pure-move items: LH-08 for BrowserTableGroup (keeps LH-R-02) and the new LH-18 for BrowserWidgets.
- LH-09 and LH-14 now chain through LH-18.

**7. A spec that contradicts another repo's fix.**
- PrettyChat `docs/ARCHITECTURE.md:202` says LootHistory "caches its loot and currency patterns once ... stops recording". LH-01 makes that false.
- PC-06 now depends on LH-01 and restates the sentence for the fixed state, citing it by symbol and `LootHistory@sha`. It no longer just re-cites the line.

**8. Wrong verify step.**
- LH-STD's verify expected a version in X-Standard, the README badge and CLAUDE.md.
- All eleven addons are version-free today, and the other STD items keep that form unless v2.77.0 requires a version. Aligned LH-STD with them.

### Changes needed outside the patches

- **Manifest order matters.** `next_args.py --order` runs M3 per repo in list order and drops `depends_on`. The new items must be inserted at these positions:
  - LH-18 immediately after LH-08.
  - BL-05, CM-09, PF-06 and WG-07 immediately before their repo's STD item.
  - DC-15 after DC-11 and before DC-12 (M1 runs on hard dependencies, so this one is safe either way).
- **One cross-repo M3 dependency: PC-06 on LH-01.** `--order` mode drops it. The M3 launch has to hold PC-06 until LH-01 has landed (PC-06's step 1 checks this), or run PrettyChat in items/deps mode. RESUME.md should say so.

### Reviewed and left alone

- **Smoke checks on re-vendor items are uneven.** Six RV items have one and five don't, but LK-12's collection-wide /reload smoke already covers loading on the new payload. The RV smokes that remain are harmless load checks.
- **Smoke checks on refactors or pure moves** (AM-06, BL-03, LH-12, MM-06) are kept. Each touches load-time or lifecycle paths, where in-client risk is real.
- **LH-11** (effort L) stays one item: six functions in two coupled files, with characterization tests first.
- **WS-07** (effort L) stays one item: it is one coherent citation conversion.
- **Behaviour items without smoke** (CM-04, PC-02, PM-07, WG-03, LH-03) are covered by headless tests and don't need an in-client check.
- **Docs ripples are covered.** Every LibKa0s item carries its CHANGELOG block, `docs/api` document and `test-cases.md` regeneration. Addon items regenerate `test-cases.md` and the README badge in the same commit. No version bumps anywhere, which matches OWNER_SCOPE.
