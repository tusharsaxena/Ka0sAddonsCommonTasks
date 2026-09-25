# Execution plan

`items.tsv` is the manifest and the single source of truth for ids, dependencies and effort. The tables
below explain it; if the two disagree, `items.tsv` wins and this file is corrected before execution
starts (never after: see "frozen" in `../../CLAUDE.md`).

## 1. Rules

### Branch

**`feat/2026-09-25-diagnostics-rollout`** in every repo this plan touches:

| Repo | Branch point |
|---|---|
| WowAddonStandards, wow-addon | `master` |
| LibKa0s | **`53c141a`** (the local `v1.59.0`, tip of `feat/2026-09-25-draghandle-close`). The new branch stacks on it; v1.59.0 is never rebased or re-cut. **Before DR-LK-01:** the LibKa0s working tree is checked out on `feat/2026-09-25-draghandle-close` today, and AuraMaster's batch workflow may still need it. Confirm no other workflow is using the tree (or work in a `git worktree`), and confirm the branch tip is still `53c141a`. If that branch gained commits (a v1.59.x for batch 9/10), stack on its new tip, and record that commit and any new tag in `OWNER_RULINGS.md`. |
| AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup | `master` |
| AuraMaster | `master` **after** its batch-8/9/10 branch merges (DR-OW-05). If the owner instead approves stacking, branch from the recorded tip of that branch, and record the commit in `OWNER_RULINGS.md`. Never check out or write in AuraMaster while another workflow owns its tree. |
| Ka0sAddonsCommonTasks | `main` (this bundle, `OWNER_RULINGS.md`, `checkpoints.tsv`, `99_REPORT.md`) |

### Commits

- One item per commit, subject `<ID>: <summary>`. Every id carries the `DR-` prefix (`DR-AT-03`), because the 2026-09-23 plan already used bare `WS-01`, `LK-01`, `AT-01` and so on in the same repos, and `resume-state.sh` would count those old commits as done. Several ids may share a commit when they must land
  together to keep a suite green (`DR-AT-01 + DR-AT-02: ...`).
- Each commit ends with the session's attribution trailers.
- Each repo's green gate (its own `CLAUDE.md`) passes at every commit, run through
  `/home/tushar/.claude/wow-addon/bin/ka0s-bounded`: `luacheck .` 0/0, `lua tests/run.lua`, lizard CCN ≤ 15,
  and the 1500-line **file** cap. No red-carrying commits are planned: a re-vendor commit (`-01`) carries
  every edit its own suite needs to stay green (stub member, host live-verb copies, buffer pins), which is
  why those sit in `-01` and not later.
- README edits go through the de-AI pass (`humanize` skill) before commit, as documentation-§1 requires.
- Never sed the literal `1500` (C3). Every buffer edit is at a listed site.

### Push policy

- **Feature branches only**, pushed at each milestone checkpoint. The owner authorized this (Q18,
  DR-OW-04).
- **Ask the owner before** merging WowAddonStandards or wow-addon to `master` (DR-OW-07, Q21).
- Otherwise **never** merge into `master`/`main`, push a tag (`v1.59.0`, `v1.60.0`), bump an addon version or cut a
  release. Those are DR-OW-06.
- **A tag is never re-cut.** v1.60.0 is vendored by up to eleven addons as soon as M3 starts, and each addon's `tests/test_vendor_sync.lua` pins the bytes at that tag. A library defect found during M3 or M4 ships as **v1.60.1** (new commit and new local tag) and is re-vendored with `/wow-addon:revendor-libka0s --tag v1.60.1` into the addons already done. The same rule protects v1.59.0.
- **One standard version for one rule change.** DR-WS-05 amends v2.68.0's changelog entry when v2.68.0 is still unpublished. If DR-OW-07 has already published it, DR-WS-05 becomes a v2.68.1 patch with its own entry (STD-24).
- When the owner merges LibKa0s: `--no-ff` or fast-forward only. **No squash, no rebase**, or the local
  `v1.59.0` and `v1.60.0` tags point at orphaned commits. Push `master` and both tags together.
- Independent reviews are recorded as `refs/notes/ka0s-review` notes on the item's commit and pushed with
  the branch.

## 2. Milestones and gates

| Milestone | Starts when | Items | Checkpoint |
|---|---|---|---|
| **M0** | now | DR-OW-01 | `OWNER_RULINGS.md` committed in this repo with a ruling per question |
| **M1** | DR-OW-01 | DR-WS-01..DR-WS-04, DR-WS-06, DR-WA-01; then DR-WS-05 once DR-OW-02 lands | WowAddonStandards: its own checks (link check, section-number check, the standard's CLAUDE.md gates). M1 closes in two steps: **M1a** without DR-WS-05, **M1b** with it |
| **M2** | DR-LK-01 any time after the LibKa0s pre-check (it is the measurement aid). DR-LK-03 and DR-LK-04 after DR-OW-01, because they build Q4, Q8, Q9, Q12, Q13 and Q15 into code. DR-LK-05 needs DR-WS-05; DR-LK-06 needs the standard on the rollout branch | DR-LK-01..DR-LK-06, DR-OW-02 | Release battery green (`tests/_kit/run-automated-tests.sh --release 1.60.0`), `ANALYSIS.md` written, local tag `v1.60.0` on DR-LK-06's final commit, `DebugLog.lua` < 1000 lines |
| **M3** | DR-LK-06 (every `-01` depends on it) | per addon `-01`..`-06`; CM/AT `-06` also wait on DR-OW-03 (KickCD has no `-06`); AM items wait on DR-OW-05 | Per addon, after its last M3 item: full green gate, `git status` clean |
| **M4** | that addon's M3 items, DR-WS-05 and **DR-OW-07** | DR-OW-07; per addon `-07`; DR-REC-01 | AUD-01 passes in every addon; smoke results recorded by the owner in `99_REPORT.md` |

### Gates that need the owner

| Gate | What the owner does | Unblocks |
|---|---|---|
| DR-OW-01 | Answers `04_OPEN_QUESTIONS.md`. The executor writes `OWNER_RULINGS.md` from the answers and commits `DR-OW-01: ...` | DR-WS-01 |
| **DR-OW-02** | Runs the bench (§5) and records figures; picks 5000 or 3000 against BUF-02 | DR-LK-02, DR-WS-05, and therefore every re-vendor |
| **DR-OW-03** | Ruled (Q1): X-02 and X-04 as written; KickCD gets no X (X-03). Recorded as a commit | DR-AT-06, DR-CM-06 |
| DR-OW-04 | Feature-branch pushes at checkpoints: authorized (Q18) | Nothing now |
| DR-OW-05 | Merges AuraMaster's batch branch, or approves stacking. Merging that branch to AuraMaster `master` requires LibKa0s `feat/2026-09-25-draghandle-close` merged and the `v1.59.0` tag pushed **first**, because AuraMaster's `CLAUDE.md` provenance line names v1.59.0 | DR-AM-01 |
| **DR-OW-07** | The executor asks the owner first (Q21). The owner merges and pushes WowAddonStandards v2.68.0 (and wow-addon) to `master`. `/wow-addon:revendor-standards` and `/wow-addon:standards-audit` fetch the standard from `raw.githubusercontent.com/.../WowAddonStandards/master` (`wow-addon/commands/revendor-standards.md:28`), so an unpublished v2.68.0 cannot be revendored or audited against | every `-07` |
| DR-OW-06 | Merges and pushes branches and tags, in this order: LibKa0s (`master`, `v1.59.0`, `v1.60.0`, and any `v1.60.x`, together), then AuraMaster's batch branch if not already merged, then the addons. The standard and wow-addon went first, in DR-OW-07 | End state, outside the plan |

## 3. Tasks

Effort: S ≤ 2 h, M ≤ 1 day, L > 1 day. Smoke ids refer to §6.

### M0 and M1: the standard

| ID | Repo | Task | Depends | Effort | Spec |
|---|---|---|---|---|---|
| DR-OW-01 | this repo | Record owner rulings | — | S | Q1–Q21 (Q1 recorded as DR-OW-03; the Q2 measurement stays DR-OW-02) |
| DR-WS-01 | WowAddonStandards | v2.68.0 header, changelog, footer fix; append debug-logging-§14; §4/§5/§7 and adoption-line edits | DR-OW-01 | M | STD-01..16, 19..21 |
| DR-WS-02 | WowAddonStandards | slash-commands-§2/§3/§7, thirteen reserved verbs | DR-WS-01 | S | STD-22 |
| DR-WS-03 | WowAddonStandards | documentation-§1 item 9 and renumber; §3 Tier-2 trigger | DR-WS-01 | S | STD-17, 18, 23 |
| DR-WS-04 | WowAddonStandards | Anti-pattern #90; AUDIT.md check and counts | DR-WS-02, DR-WS-03 | S | AP-01, AUD-01 |
| DR-WS-06 | WowAddonStandards | EXECUTIVE_SUMMARY, NEW_ADDON_CONTEXT, the NEW_ADDON.md playbook, library-stack (`:82` recount, `:93`, `:256`), STANDARDS.md `:57`, open-evolutions `:13` | DR-WS-04 | M | STD-24 |
| DR-WA-01 | wow-addon | README item citations, live-verb enumerations in both agents, new-addon and sync-docs README rules, plugin version bump | DR-WS-02, DR-WS-03 | S | STD-25 |
| DR-WS-05 | WowAddonStandards | The measured number in §1/§9/§11 and the ripple | DR-WS-06, DR-OW-02 | S | BUF-07 |

### M2: LibKa0s v1.60.0

| ID | Task | Depends | Effort | Spec |
|---|---|---|---|---|
| DR-LK-01 | LibKa0s pre-check (§1 Branch). DebugLog minor 14 opens: `lib.TIME_COPY` flag in `ShowCopy`, `lib.BUFFER_SLACK` published (still 64); mocked-clock tests | — | S | BUF-06b, BUF-03 |
| DR-OW-02 | **Owner measurement** (§5), figures and the chosen number recorded | — (DR-LK-01 makes it easier) | S | BUF-02 |
| DR-LK-02 | `MAX_BUFFER` and `BUFFER_SLACK` values; rationale comment; characterization cases rewritten on the constants; suite runtime checked against the kit bounds | DR-LK-01, DR-OW-02 | M | BUF-01, 03..05 |
| DR-LK-03 | `DebugLogDiagnostics.lua` helper, install hook, `DebugVerb`, suite, `majors.lua`, `LibKa0s.xml` | DR-LK-01, DR-OW-01 | L | LIB-01..09 |
| DR-LK-04 | Slash minor 16 `LIVE_VERBS` | DR-OW-01 | S | LIB-10 |
| DR-LK-05 | Version docs, api manifests, README table (DebugLog 14.1, Slash 16, file count 22), `releasing.md` lines 7 and 250, `CHANGELOG.md` v1.60.0 ("Built to v2.68.0"), `test-cases.md` | DR-LK-02, DR-LK-03, DR-LK-04, DR-WS-05 | M | — |
| DR-LK-06 | Release run, `ANALYSIS.md`, release-notes line, **local** tag `v1.60.0`. WowAddonStandards must be checked out on the rollout branch so the standards-pointer check reads v2.68.0 | DR-LK-05 | S | — |

### M3: per addon

Every addon follows the same shape. `-01` re-vendors with `/wow-addon:revendor-libka0s --tag v1.60.0` and keeps the suite green. That skill interviews per new surface, files declines as GitHub issues and writes a `docs/revendor/<date>/` bundle. This plan has already decided the candidates, so answer its interview from the plan: the diagnostics helper and Slash 16 are adopted in `-03`; the WidgetsDragHandle close mark is adopted in `-06` on ConsumableMaster and AbsorbTracker, KickCD does not adopt it (owner ruling, Q1), and it is not a candidate elsewhere (no DragHandle); the buffer change is not an adoption. **File no decline issues for these.** `-02` adds read-only
seams (only where needed; the id is skipped otherwise); `-03` is the report; `-04` the README; `-05` the
docs; `-06` the X (ConsumableMaster and AbsorbTracker only). Addons are independent of each other and can run in any order, one
item at a time per repo.

| Addon | -01 re-vendor | -02 seams | -03 report | -04 README | -05 docs | -06 X | Effort total |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | liveVerbs builder | 4 seams | DX-AT; 18 → 19 verbs | ✓ | new `debug.md`, Tier-2 row flip, LibKa0s file count (three docs) | every bar: player, target, focus (X-04) | M |
| BankLedger | degraded list `:404` | — | DX-BL; scan folded; 17 → 18 | ✓ | ✓ | — | M |
| ConsumableMaster | `test_debuglog.lua:281` | 3 accessors | DX-CM; order pin | ✓ + fix `:117`, `:120` | ✓ | macro bar (X-02) | M |
| KickCD | live union test | dumps take `emit` | DX-KC | ✓ | ✓ | none: KickCD does not adopt the close option (Q1, X-03) | M |
| LootHistory | `Schema.lua:858` + 2 test copies | — | DX-LH; degraded dispatcher; 16 → 17 | ✓ | ✓ | — | M |
| MultiMeters | — | re-host `diag` report, retire `diag` | DX-MM missing sections | ✓ | ✓ | — | M |
| PanelMaster | degraded list `:447-455` | unlock queue | DX-PM; retire `dump` | ✓ | ✓ | — | M |
| PartyFrameEnhanced | `LIVE_WHILE_DISABLED` | 3 accessors | DX-PF; TOC, loadorder, locale | ✓ | ✓ | — | M |
| PrettyChat | `test_debuglog`, `test_libka0s`, `test_disabled`, comment | — | DX-PC with `||` escape | ✓ | new `debug.md` | — | M |
| WhatGroup | `test_slash.lua:473-475` | 2 snapshot accessors | DX-WG; usage line | ✓ | new `debug.md`, `debug-content.md` | — | M |
| AuraMaster | from v1.59.0 | — | DR-AM-02 migrate onto the helper (Q3) | DR-AM-04: step 3 corrected (drop "paste it into a GitHub issue" and the link) | buffer sites | already done | S–M |

Each `-03` item's tests implement STD-19 in full: the shared kit case `test_diagnostics_contract.lua` (Q20 (b)) run against the addon's dispatcher, plus its domain cases. Each addon's `-03` also updates its own verb and
live-set count claims (C10).

### M4: docs and audits

| ID | Task | Depends |
|---|---|---|
| DR-OW-07 | Owner publishes the standard and the plugin (see §2) | DR-WS-05, DR-WA-01 |
| `DR-<P>-07` (each addon) | `/wow-addon:revendor-standards` to v2.68.0 (TOC `X-Standard`, README badge, CLAUDE.md), `/wow-addon:sync-docs`, then run AUD-01 by hand and record the result in the commit body | that addon's M3 items, DR-WS-05, DR-OW-07 |
| DR-REC-01 | `99_REPORT.md`: per-repo heads, battery totals, the AUD-01 results, deviations, and the smoke table for the owner to fill | every `-07` |

## 4. Verification per item

- Every item: its repo's green gate at the commit (§1).
- `-01`: `tests/test_vendor_sync.lua` (or the repo's equivalent) passes with the new provenance line; the
  DebugLog parity case is green only because the stub gained `RunDiagnostics`; `grep -n MAX_BUFFER` in
  the addon's own tests shows no literal.
- `-03`: STD-19 cases present; `grep -rniE '"(diag|dump|dx)"' settings core modules` shows no report
  alias; a disabled-state test dispatches both forms.
- `-04`: the section text diffs clean against STD-17 apart from the slash; step 3 reads "include it with your bug report" and there is no GitHub link.
- `-06`: X-05 case; `tests/test_draghandle*` Measure pins re-checked.
- DR-LK-02: the three rewritten cases fail when `MAX_BUFFER` or `BUFFER_SLACK` is changed by one (a
  falsification run, recorded in the commit body, then reverted).

## 5. The buffer measurement (DR-OW-02)

The owner runs this in the live client. The executor never marks it done.

**Option A: zero-code, on today's build.** `lib.MAX_BUFFER` is read at call time everywhere except
`SetMaxLines` (read at frame build), so a scratch instance built after overriding it measures any N.
Chat `/run` is limited to 255 characters; run it through WowLua or DevTool, or a throwaway
`Interface/AddOns/Ka0sCopyBench/` addon that is never committed.

```lua
local lib = LibStub("LibKa0s-DebugLog-1.0")
local function bench(N, W, font)
  local old = lib.MAX_BUFFER; lib.MAX_BUFFER = N
  local D = lib:New({ name = "Ka0sCopyBench"..N..W, title = "Copy bench", addonName = "Ka0sCopyBench",
    font = font or STANDARD_TEXT_FONT, isEnabled = function() return true end,
    setEnabled = function() end, print = print })
  local pad = string.rep("x", W - 20)
  local t0 = debugprofilestop()
  for i = 1, N do D:Add("Bench", ("line %05d %s"):format(i, pad)) end
  local t1 = debugprofilestop(); D:Show()
  local t2 = debugprofilestop(); local text = D:CopyText()
  local t3 = debugprofilestop(); D:ShowCopy()
  local t4 = debugprofilestop()
  C_Timer.After(0, function()
    local t5 = debugprofilestop()
    print(("N=%d W=%d bytes=%d fill %.0fms show %.0fms concat %.1fms copy-open %.0fms next-frame %.0fms")
      :format(N, W, #text, t1-t0, t2-t1, t3-t2, t4-t3, t5-t4))
    lib.MAX_BUFFER = old
  end)
end
-- bench(0,120) baseline; bench(1500,120); bench(3000,120); bench(5000,120); then W = 200
```

**Option B: on the branch build, after DR-LK-01.** Copy the branch-head `LibKa0s/` into **one** addon's
`libs/` in the live AddOns folder (not a re-vendor commit; LibStub's highest-minor rule makes it the
live copy), run `/run LibStub("LibKa0s-DebugLog-1.0").TIME_COPY=true`, fill a console, press Copy.
Restore the folder afterwards.

**Procedure.** Pass the JetBrains Mono path from any Ka0s addon's `libs/LibKa0s/media/fonts/` as `font`.
Three runs per (N, W), take the median, subtract the `bench(0, W)` next-frame figure. By hand: select all,
`Ctrl+C`, drag-select and scroll in the copy box at 5000. A good place for a real-data run is PrettyChat
after several `/pc test all` (long, wide lines).

**Decision (BUF-02).** 5000 if copy-open + next-frame ≤ 250 ms at W = 120 and ≤ 1 s at W = 200 and the
box stays responsive; otherwise 3000 against the same thresholds; otherwise stay at 1500 and revisit Q2.
Record all figures, the client build and the machine in `OWNER_RULINGS.md` under DR-OW-02.

## 6. Smoke checks (the owner runs these after M3; results go in `99_REPORT.md`)

| ID | Check | Pass when |
|---|---|---|
| S1 | Disable the addon, run `/<slash> diagnostics`, then `/<slash> debug diagnostics` | Both write a full report; the header shows enabled=false, stood down |
| S2 | `/<slash> debug on`, reproduce something, `/<slash> diagnostics` | Trace lines remain above the begin marker; nothing was cleared |
| S3 | Run the report in combat (and for AM/KC/MM/PF, inside a restricted instance) | No Lua error; unreadable values show `<secret>`/`?`/"unreadable in combat" |
| S4 | Press Copy after S2, paste into a text editor | Paste has the trace, the begin marker and the end marker with the brand, no `|c` escapes (PC: `||`) |
| S5 | `/<slash> debug off`, then `/<slash> diagnostics` | The report lands in full; afterwards the console header still reads `Debug: OFF` and the next traced action writes nothing (ungated sink, flag untouched) |
| S6 | Unlock, click X on each strip that has one (AuraMaster included, as a regression check after its re-vendor) | Only that element goes; the chat line names the way back; the way back restores it in place (CM: in combat, the bar hides when combat ends; AT: the player bar has an X too). KickCD's strips show no X |
| S7 | Fill the console past the new cap | Counter reads `N / 5000 lines` (or 3000) and pins at the cap; Copy opens without a noticeable hitch |
| S8 | `/<slash> debug diag` and `/<slash> diag` (MM: `/mm debug diag`; PM: `/pm debug dump`) | Neither runs the report; each behaves as that addon's ordinary unknown word (Q7(a)) |
| S9 | Starting from a fresh `/reload` with the console closed, follow the README's `## Reporting a bug` steps word for word | Every step works as written; the paste holds the trace and the whole report |
| S10 | Mixed install: one Ka0s addon still on a v1.58.0 build (its CurseForge release) beside v1.60.0 addons, then `/reload` | No Lua error; the old addon's console counter reads the new cap (LibStub runs the highest minor); `/<old-slash> diagnostics` while that addon is disabled gives its normal unknown-verb answer and raises nothing |
| S11 | The long alias with both forms, for example `/auramaster diagnostics` and `/auramaster debug diagnostics` | Same report as the short slash |

## 7. Resume procedure

**Git is the only state.** An item is done when a commit whose subject starts `<ID>: ` exists in the repo
`items.tsv` names, on `feat/2026-09-25-diagnostics-rollout` or the default branch. Owner gates (`OW-*`)
are commits in this repo. Items that legitimately land with no commit go in `exceptions.tsv`
(`<ID>\t<reason with a command that proves it>`).

1. **Where are we?** `./resume-state.sh` (per-milestone counts, the next ready items, dirty trees, branch
   check); `./resume-state.sh -v` lists every remaining id; `./resume-state.sh M3` one milestone.
2. **Clean up an interrupted item.** Items run one at a time per repo, so a dirty tree is one interrupted
   item. Read the diff. Continue it if it is that item's work; otherwise `git stash push -m "<ID> partial"`.
   Never `reset --hard` or `checkout .` work you have not read. **AuraMaster:** if another workflow owns
   its tree, do not touch it at all.
3. **Relaunch.** Take the ready items `resume-state.sh` prints (dependencies landed, owner gates
   recorded), in manifest order per repo. Different repos may run in parallel; one repo never runs two
   items at once.
4. **Checkpoint** after each milestone (and after each addon's M3 items): the gate in §2, then push the
   feature branch (Q18), then append a row to `checkpoints.tsv` (date, checkpoint, evidence: test totals,
   heads) and commit it here.
5. **Files to create on first execution:** `OWNER_RULINGS.md` (DR-OW-01), `checkpoints.tsv` (header
   `when\tcheckpoint\tevidence`), `RESUME.md` (a copy of this section plus anything learned), and
   `exceptions.tsv` only when needed. Once execution starts, this plan is frozen; later developments go in
   `RESUME.md`, `checkpoints.tsv` or `99_REPORT.md`.
