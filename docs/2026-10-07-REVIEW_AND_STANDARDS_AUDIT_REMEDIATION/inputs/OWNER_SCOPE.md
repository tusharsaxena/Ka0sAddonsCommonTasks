# Owner scope — 2026-10-07

Agreed in session on 2026-10-07, after the owner read `01_CONSOLIDATED_FINDINGS.md`.

1. **In scope:** every finding whose final verdict is `must`, `should` or `optional` (251 items).
   **Out of scope:** the 39 `no` verdicts (27 real-but-not-worth-it, 12 refuted). They stay recorded in
   `01_CONSOLIDATED_FINDINGS.md`; nothing is done for them.
2. **Overrides of the assessment:**
   - `MM-A-03` (one malformed `(architecture-4)` citation): `must` → `should`. Trivial; fix with the rest.
   - `DC-A-05` (audit agent misses WowAddonStandards' `docs/ARCHITECTURE.md` register): `must` → `should`.
   - `LH-R-03` (LootHistory LED-P2-01..24 in-client checks unrecorded): only the owner can run these. The
     plan lists them in `06_SMOKE_TESTS.md`; no agent records a result or marks them passed.
3. **Order:** upstream first (WowAddonStandards, LibKa0s, dev-copilot), then re-vendor LibKa0s into the
   addons, then the addon items.
4. **Execution guidelines (standing):** decide autonomously and ask only when absolutely necessary;
   resumable, checkpointed plan; one feature branch `feat/2026-10-07-review-audit-remediation` per repo
   with incremental commits; push feature branches at milestone checkpoints; never merge, push a tag, bump
   an addon version or cut a release without the owner's go-ahead; after the owner-approved merge, delete
   every branch, stash and worktree the run created; orchestrate with Workflow (ultracode).
5. **Derived rulings (session lead, under 4):**
   - The new LibKa0s release is `v1.71.0`, tagged **locally only** on the final LibKa0s item's commit;
     the tag is pushed only on the owner's go-ahead. Addons re-vendor from that local tag.
   - Re-vendoring is mechanical (copy both payloads whole, roll the provenance line, write the
     `docs/revendor/` bundle, including the consolidated span bundle for the unrecorded v1.69.0/v1.70.0
     re-vendors). Adoption candidates the plan does not already require are listed in the bundle as
     "not adopted in this run" — no interview and no GitHub issue filing.
   - Addons' standards reference (TOC X-Standard, README badge, CLAUDE.md) is rolled to the standard
     version this run produces, read from WowAddonStandards' feature branch; it lands with the merge.
   - No GitHub issue writes in this run except closing/commenting issues a finding names explicitly, and
     those are spaced out.
