# R3-debuglog-report: LibKa0s#79, the DebugLog report seam

Read-only research, 2026-11-16. LibKa0s `master` = `v1.104.0` (`9bc9cc51`), standard `v2.112.2`.
All addon reads were from the default branch (`master`; SkillMaster and CombatTrail are `main`).

## 1. What exists today

### LibKa0s-DebugLog-1.0 (shell minor 22; Diagnostics 10, Gates 1, Window 4; version key `22.10.1.4`)

- **The buffer is already plain on its frame and colored on its view, but the message is not.**
  `append` (`LibKa0s/DebugLog.lua:413-440`) writes `lib.FormatColored(ts, tag, msg)` (or the skin
  owner's `f.__logLine`) to the view and `lib.FormatPlain(ts, tag, msg)` to `D.buffer`
  (`DebugLog.lua:430`). Both carry `msg` verbatim, so any `|cff…|r`, `|T…|t`, `|H…|h` inside the
  message reaches Copy. The issue's wording ("D:Add stores one string for both") is slightly off:
  the timestamp/tag coloring is already split; only the **message's own escapes** leak.
- `D:CopyText()` = `table.concat(D.buffer, "\n", firstKept(), #D.buffer)` (`DebugLog.lua:539`);
  `FindLine`, `LastLine`, `BufferSize` and the status line all read `D.buffer` (`:487-500`, `:532`).
- **A second reader of `D.buffer`: the skin-switch rebuild.** `rebuildLog`
  (`LibKa0s/DebugLogWindow.lua:362-377`) clears the view and re-renders every buffered line from
  `D.buffer`, parsing `"<ts> | [<tag>] <msg>"`. If the buffer is stripped and nothing else changes, a
  skin switch silently drops every message color from the view. This is the one non-obvious ripple of
  the plain-Copy change.
- **The strip already exists, privately**: `strip(s)` in `DebugLogDiagnostics.lua:100-109` (protects
  `||`, removes `|cAARRGGBB`, `|r`, unwraps `|H…|h…|h`, removes `|T|t`, `|A|a`, `|K|k`, turns `|n`
  and newlines into spaces). Diagnostics' `Out:str`, `Out:plain`, `Out:add` all run through it
  (`:140-170`), which is the issue's "`Out:plain`".
- **The report pattern already exists, privately**, as `D:RunDiagnostics` (`DebugLogDiagnostics.lua:402-411`):
  build lines, append each via `ctx.append` (ungated, no repaint), one `ctx.repaint()`, `D:Show()` if
  hidden, one `ctx.emit(D:Text("DIAG_WRITTEN"):format(n))`. `ctx.emit` is the descriptor's `print`
  (`DebugLog.lua:260`, default the chat frame). The localizable pointer string is
  `lib.STRINGS.DIAG_WRITTEN` (`DebugLog.lua:145`) with a file-local English fallback
  (`DebugLogDiagnostics.lua:90`). The cap logic (`capOf`, `DIAG_MAX_LINES` clamped to
  `MAX_BUFFER - 100`, the `truncated` line) is at `:65-69`, `:329-333`, `:358-368`.
- Secondary-file pairing: Diagnostics installs itself only when `lib.__diagShellMinor == lib.MINOR`
  (`DebugLogDiagnostics.lua:53-56`), and `lib:New` calls `lib.__installDiagnostics(D, ctx)` handing
  `d, emit, safeToString, append, repaint` (`DebugLog.lua:655-662`). Any shell bump re-pairs it.

### Secret handling in LibKa0s

- `Core.SafeToString` (`LibKa0s/Core.lua:79-84`): nil → `"nil"`, boolean → tostring, otherwise a
  `table.concat` probe (`Core.IsConcatSafe`, `:66-70`), secret → `Core.SECRET = "<secret>"` (`:49`).
  Its own comment notes a bare table also probes unsafe and renders as the sentinel, which is why a
  serializer must walk tables itself and never hand one to SafeToString.
- `Compat.IsSecret` (`LibKa0s/Compat.lua:190`) wraps `issecretvalue` (false before 12.0). DebugLog
  depends on Core and Widgets only (`DebugLog.lua:23-35`), not on Compat, so a serializer inside
  DebugLog should probe `issecretvalue` locally (the three-line body Compat itself uses, `:176-180`)
  rather than add a Compat dependency.
- The instance's `safeToString` is the descriptor's (`DebugLog.lua:257`), so a host's own seam is
  honoured; a serializer built on the instance should use it, not `core.SafeToString` directly.

### Kit.assertSurfaceParity and the stubs

- `Kit.assertSurfaceParity(stub, "LibKa0s-DebugLog-1.0", ignore)` (`testkit/asserts.lua:290-330`)
  compares `Kit.publicMembers` of the registered live surface (the host's **instance**, registered in
  each `tests/run.lua`, e.g. AbsorbTracker `tests/run.lua:55`) against the stub; `__`-prefixed members
  are filtered.
- Every addon checked registers `NS.DebugLog` (the instance) and asserts its degradation stub against
  it: AbsorbTracker `tests/test_surface_parity.lua:79`, AuraMaster `:29`, BankLedger (run.lua:92),
  KickCD `:111`, PrettyChat `:128`, WhatGroup `:98`, DropWatcher `:37`, ConsumableMaster `:199` (a
  projected seam). **Consequence: adding any public member to the instance (`Report`, `Serialize`)
  turns every one of those parity cases red at re-vendor until the addon's stub carries it.** So the
  re-vendor phase cannot be a pure copy for this issue; each addon needs a one-member stub addition
  (or an ignore entry). This is the main planning fact for phase [2].
- Example stub shape: DropWatcher `core/DebugLogSetup.lua:55-80` (`RunDiagnostics` prints the
  collection's library-absent line and returns 0).

### The ConsumableMaster reference implementation

- Commit `9d2b26e` ("CM-F10: Reports go to the debug console…") **is merged into ConsumableMaster
  `master`** (`git merge-base --is-ancestor 9d2b26e master` true; the `feat/2026-11-08-forever-port`
  branch no longer exists locally).
- `DL.Report(tag, title, fn)` live arm, `core/DebugLogSetup.lua:310-349` (master):
  collect `fn(function(line) lines[#lines+1] = line end)`; 0 lines → return 0 (no report, no pointer);
  `D:Add(tag, "/cm " .. title)`; each body line through `D:Add` (ungated, one repaint **per line**);
  `D:Show()` if hidden; `KCM.Say(REPORT_POINTER:format(title, n))` with
  `REPORT_POINTER = "%s: %d lines written to the debug console. Use Copy to share it."`; `n` counts the
  header. Its comment at `:330-335` already names the lift: "this body becomes
  `return D:Report(tag, title, fn)`, the degraded arm above goes, and no caller changes."
- Degraded arm, `core/DebugLogSetup.lua:124-136`: streams each line to `KCM.Say`, no pointer, returns n.
- Serializer, `core/SlashDump.lua:27-140` (master): `SERIAL_MAX_LINES = 400`, `SERIAL_MAX_DEPTH = 6`;
  keys sorted numbers → strings → other (tostring); identifier keys bare, others `[%q]`/`[n]`; strings
  `%q` with the newline escape kept on one line; functions/userdata/threads as `<type>`; secrets via
  `KCM.Compat.IsSecret` then `SafeToString`; cycle detection on the **current path only** (`<cycle>`,
  a shared subtable renders under both parents); empty `{}`; depth overflow `{...}`; overflow line
  `... truncated at 400 lines`. Signature `serialize(out, value, indent) -> written`.
- Tests: `tests/test_slash_report.lua` (master), 8 cases: every report verb lands with logging off and
  one pointer (`:53`), reveal (`:73`), no `DevTools_Dump` (`:83`), usage/refusal writes no report
  (`:106`, `:117`), help/list/bare dump stay in chat (`:128`), degraded fallback (`:138`), serializer
  sorting/indent/bounds (`:150`).
- CM docs: `docs/debug.md` "Reports, chat or console" section and `docs/module-map.md:872`.

### DevTools_Dump across the collection

`git grep DevTools_Dump` on every roster addon + CombatTrail (excluding `libs/`, `tests/_kit/`):
**no live call anywhere.** Remaining hits are prose only: ConsumableMaster docs/comments/the
negative test, and DpsRace `docs/smoke-tests.md:412`, an owner `/run` smoke line (not addon code;
leave it). The acceptance line "no addon calls DevTools_Dump" is already true of code; the rollout
is about routing report verbs, not removing DevTools_Dump.

### The standard

No rule for general reports exists in `v2.112.2`. What exists:
- debug-logging-§4 (`standards/debug-logging.md:72`): diagnostics MUST; further topic dumps MAY.
- debug-logging-§12 (`:295-296`): an explicit user-initiated run writes ungated; revealing the console
  is the host's call "at the few moments that warrant it (a run starting, a report or dump being asked
  for)". This is the closest existing text and is compatible with the ruling.
- debug-logging-§14 (`:317-475`): the diagnostics report, its "Reveal, then one chat line" (`:423`) and
  its library-absent stub rule (`:449-452`). Note §14's stub rule is **the opposite** of the ruling
  for reports: diagnostics absent prints one line and writes nothing; a report absent falls back to
  chat. The new rule must say why they differ (size: a report is tens of lines asked for by name).
- slash-commands (`standards/slash-commands.md:40`, `:76`, `:84`): reserved verbs, the diagnostics row.
  Nothing on chat-vs-console routing of a verb's output.
- `grep -i 'LibKa0s#79\|D:Report\|DevTools_Dump\|report seam'` over `standards/standards/*.md` and the
  CHANGELOG: no hits. The rule is new.

### Buffer-strip blast radius (measured)

Experiment in scratch copies only (`git archive` of each default branch into
`scratchpad/r3rv/<repo>`, the vendored `libs/LibKa0s/DebugLog.lua` patched so `D.buffer` gets the
escape-stripped message, suite run through `ka0s-bounded` before and after, FAIL lines diffed; the
baseline failures are archive artefacts such as no `.git`, identical before and after):

| Repo | New failures from a plain-message buffer |
|---|---|
| LibKa0s (own suite, 4668 cases) | 0 |
| ConsumableMaster | **3**: `/cm dump item on an unclassifiable item says (none) in red`, `/cm dump pick on a composite renders both sections with on/off tags`, `/cm priority list renders item and spell rows in the same columns` (they pin `|cff…` in console lines read from `D.buffer`, `tests/test_slash.lua:405-406`, `:775`, `:824-825`) |
| AbsorbTracker, AuraMaster, BankLedger, DpsRace, DropWatcher, KickCD, LibKa0sSkinTester, LootHistory, MultiMeters, OutfitterReborn, PanelMaster, PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat, QuickComms, WhatGroup, SkillMaster, CombatTrail | 0 each |

So the plain-Copy change costs three test rewrites, all in ConsumableMaster. (Not measured: the
parity break from new instance members, see above. That one hits every addon with a DebugLog parity
case.)

## 2. Proposed design

### 2.1 Plain Copy buffer, colored view (DebugLog shell 22 → 23, Window 4 → 5)

- Lift `strip` into the shell as a lib-level pure function, **`lib.PlainText(s)`** (name open; also
  `lib.StripEscapes`). Diagnostics drops its private copy and uses it (one definition; Diagnostics
  10 → 11 anyway, see 2.2).
- In `append`, after `msg = safeToString(msg)`:
  `local plain = msg:find("|", 1, true) and lib.PlainText(msg) or msg` — the fast path keeps the
  common trace line at zero extra allocation (one plain `find`), which matters because `append` is on
  the gated hot path while logging is on.
- `D.buffer[i] = FormatPlain(ts, tag, plain)`. The view keeps `msg`.
- **Difference from Out's strip**: Out turns `|n` and raw newlines into spaces. For `Add`, recommend
  stripping escapes but turning `|n` into a space only, leaving raw `\n` as is (Copy already joins with
  `\n`; changing raw newlines would alter what a perf dump pastes). Decision D5.
- **Keep the view's colors across a skin switch**: maintain a private parallel array `D.__view`
  (dense; the colored `msg` when it differs from `plain`, else `false`), compacted in the same loop as
  `D.buffer` (`DebugLog.lua:432-438`) and wiped in `D:Clear`. `rebuildLog` reads
  `D.__view[i] or msg-from-buffer`. Double underscore so `Kit.publicMembers` filters it and no stub
  changes. Cost: one array slot per line, a string reference only for lines that carried escapes.
  Alternative: accept losing colors on a skin switch (simpler; rare event). Decision D3.
- Test seam for hosts that pin colors of console lines (ConsumableMaster's three cases): a public
  reader **`D:ViewLine(i)` / or document `D.__view`**. Recommend a public `D:FindViewLine(substr)`
  mirroring `FindLine` over the colored view — but that is another public member every stub must
  carry. Cheaper: hosts read `D.__view` in tests (it is a test of library-owned internals either way),
  or switch the assertion to the stripped text plus one "the view carries the color" case using the
  `f.log.AddMessage` rawset pattern LibKa0s already uses (`tests/test_debuglog.lua:466-476`).
  Recommend the latter: no new public member. Decision D4.

### 2.2 `D:Report(tag, title, fn) -> n` (recommended in DebugLogDiagnostics.lua, minor 11)

Placement: `DebugLogDiagnostics.lua` already owns every private piece a report needs (`ctx.append`,
`ctx.repaint`, `ctx.emit`, the cap, the strip, the pointer pattern) and is 429 lines; adding ~60 for
Report keeps it under 500 + Serialize (~120) ≈ 610. The shell stays ≈ 700. Alternative: a fifth
secondary file `DebugLogReport.lua` (own pairing, version key grows to five segments, `tools/gen-api-members.lua`
and every `docs/api/DebugLog` heading pattern follow). Decision D1, recommend Diagnostics (rename of
the file is not worth the churn; its header gains "and reports").

Contract (matching CM's so its call sites do not change):

```lua
--- fn(out): out(line) appends one body line (any value, through safeToString). Collected first.
--- 0 lines -> writes nothing, prints nothing, returns 0 (the verb refused in chat itself).
--- Else: header "<slash> <title>" (or "<title>" with no slash) + body, every line through the
--- ungated append under `tag`, capped at the diagnostics cap (truncated line when hit), ONE repaint,
--- D:Show() if hidden, ONE chat line via the descriptor's print:
---   D:Text("REPORT_WRITTEN"):format(title, n)   -- "%s: %d lines written to the debug console. Use Copy to share it."
--- Returns n (header included). Never touches the debug flag. Never clears.
function D:Report(tag, title, fn)
```

- Header comes from the descriptor's `slash` (`DebugLog.lua:258`, `nonEmpty(d.slash)`). Every Ka0s
  host passes `slash` (e.g. DropWatcher `core/DebugLogSetup.lua` `slash = NS.SLASH`).
- New `lib.STRINGS.REPORT_WRITTEN` beside `DIAG_WRITTEN`, overridable via `d.L`.
- Body lines are **not** stripped at write (the view keeps colors; 2.1 strips the Copy copy). This is
  the key behavioural difference from diagnostics, which strips both.
- `fn` raising: recommend `pcall`; on error append the collected lines plus one
  `<title> failed: <err>` line (err through `safeToString`) and still reveal + point, so a broken
  report is visible and copyable, as a raising diagnostics section costs one line. Decision D2.
- `tag` validation: non-string → `"Report"`. `title` non-string → `tostring`.
- Optional 4th arg `opts` (`{ maxLines = n }`) for a host that wants a smaller cap; default the
  diagnostics cap. Keep it out of v1 unless a consumer needs it (YAGNI).
- `out` is a **plain function**, as CM's is, so the degraded stub can hand `fn` its own plain
  function and every body works on both arms. Do not make it a method-bearing object: the stub would
  have to replicate the methods.

### 2.3 `Serialize(value, opts) -> lines, truncated`

- Pure, returns an **array of lines** rather than writing, so it composes with `out` (`for _, l in
  ipairs(D.Serialize(t)) do out(l) end`), with diagnostics' `out:add`, and is trivially testable.
  CM's `serialize(out, value, indent)` becomes a three-line adapter.
- Lib-level `lib.Serialize(value, opts)` in DebugLogDiagnostics.lua, plus the instance forwarder
  `D.Serialize = function(value, opts) return lib.Serialize(value, opts, safeToString) end` so the
  host's `safeToString` is used, and so a degraded host reaches it through the same `NS.DebugLog`
  seam (stub answers `{ "<table: LibKa0s not loaded>" }` or a `tostring` line). It must be on the
  instance for the degraded arm to have anything to call; that makes it a second stub member (D6).
  Alternative placement `Core.Serialize`: wider reuse, but Core 17 → 18 bumps the most-depended-on
  major and DebugLog's `NEEDS_CORE` for no consumer outside reports today. Recommend DebugLog.
- `opts`: `maxLines` (400), `maxDepth` (6), `indent` ("  "), `sort` (true). Port CM's semantics
  exactly (sorted keys numbers → strings → other; bare identifier keys; `%q` strings kept on one line;
  `<function>`/`<userdata>`/`<thread>`; `<cycle>` on the current path; `{}`; `{...}` past depth;
  `... truncated at N lines`).
- **Secret-safety**, stricter than CM's:
  - A local `isSecret(v)` = `issecretvalue and issecretvalue(v)`; plus the Core concat probe for a
    value that is not a table. Any secret value or key renders as `Core.SECRET`.
  - `%q` and `k:match` run only after the value/key proved non-secret (both raise on a secret).
  - A **secret table** (12.0 can return those) is never iterated: rendered as the sentinel.
  - `table.sort` under `pcall` (a comparator on a hostile key set must not cost the report); fallback
    is `pairs` order.
  - The whole walk under `pcall`; on a raise, the lines so far plus `<serialize failed: err>`.
  - Numbers rendered via `safeToString`, never `%d` (the gated sink's lesson, `DebugLog.lua:458-466`).

### 2.4 Degradation stub (every addon, at re-vendor)

```lua
Report = function(_, _, fn)          -- library absent: stream to chat, no pointer (ruling)
    local n = 0
    fn(function(line) n = n + 1; NS.Print(NS.SafeToString(line)) end)
    return n
end,
Serialize = function(v) return { NS.SafeToString(type(v) == "table" and "<table>" or v) } end,
```

Placed beside the stub's `RunDiagnostics`. Note `Report` is called as a method (`D:Report`), so the
stub's first parameter is self, unlike CM's flat `DL.Report(tag, title, fn)` facade.

## 3. LibStub minors

| File | Now | After | Why |
|---|---|---|---|
| `DebugLog.lua` (shell) | 22 | 23 | `lib.PlainText`, plain buffer message, `__view`, `STRINGS.REPORT_WRITTEN` |
| `DebugLogDiagnostics.lua` | 10 | 11 | `D:Report`, `lib.Serialize`/`D.Serialize`, uses `lib.PlainText` (re-pairs on shell 23 regardless) |
| `DebugLogGates.lua` | 1 | 1 | untouched (re-pairs on the shell) |
| `DebugLogWindow.lua` | 4 | 5 | `rebuildLog` reads `__view` |

Version key `22.10.1.4` → `23.11.1.5`; new `docs/api/DebugLog/version-23.11.1.5-docs.md` and a
regenerated `members-23.11.1.5.json` (`lua tools/gen-api-members.lua`). No other major moves.
`docs/api/CONSUMERS.md` gains the Report/Serialize rows (ConsumableMaster first consumer). If other
research items in this run also bump DebugLog, the key is coordinated once per release.

## 4. Test plan

LibKa0s (`tests/test_debuglog.lua`, `tests/test_debuglog_diagnostics.lua`, or a new
`tests/test_debuglog_report.lua` — a new file must join the suite inventory the kit asserts):
1. Plain Copy: `D:Add("T", "|cffff0000red|r x")` → view (rawset `f.log.AddMessage`) carries `|cff`,
   `D:LastLine()`/`CopyText()` do not; `||` survives as `||`; `|Hitem:1|h[Item]|h` → `[Item]`; a line
   with no pipe is byte-identical to today (fast path).
2. Skin switch keeps colors: add a colored line, trigger `rebuildLog`, the view still carries it;
   compaction past `MAX_BUFFER + BUFFER_SLACK` keeps `__view` aligned with `buffer`; `Clear` wipes both.
3. Report: ungated (logging off, lines land); header `<slash> <title>`; no-slash header; one repaint;
   reveal when hidden, stays shown; exactly one `print` call with `REPORT_WRITTEN` and the count;
   returns n; 0 lines → no buffer growth, no print, returns 0; `fn` raising → failure line, still one
   pointer; cap → `truncated` line, total ≤ cap; flag untouched before/after; `d.L` override of the
   pointer; secret body line renders `<secret>` without raising.
4. Serialize: CM's case ported (sorted keys, indent, `{}`, cycle vs shared subtable, depth, line cap)
   plus secret value, secret key, secret table, `%q` newline, mixed-type keys, `pcall` around a raising
   `__pairs`/`__lt` metatable.
5. `test_diagnostics_contract`/surface: the instance members list in docs matches `members-*.json`.
Kit (optional, adoption phase): `Kit.assertReport(console, runVerb, opts)` contract case (like
`testkit/test_diagnostics_contract.lua`) so every addon asserts reveal/one-pointer/refusal identically.
That is a kit revision bump; recommend deferring to adoption.

Per addon at re-vendor: green gate + the stub additions; CM additionally its three color-pinned
cases rewritten (see table), its `DL.Report` lifted to `return D:Report(tag, title, fn)` is adoption.

## 5. Standard / doc ripple

- **New rule** (lands before rollout audit, per the issue): debug-logging gains a section, e.g.
  §15 *Reports go to the console (MUST)*: definition of a report (any multi-line read-out a player
  asks for: every dump target, every non-reserved `… list`, perf reports, diagnostics); routing table
  (chat: acks/short answers, refusals/errors/usage, help, the reserved `/<slash> list`; console:
  every report); ungated, reveal, exactly one pointer through `D:Report`; usage/refusal inside a
  report verb stays in chat and writes nothing; library-absent stub streams to chat with no pointer
  (and why that differs from §14's absent rule); MUST NOT call `DevTools_Dump`/print tables to chat;
  Copy is plain text (the library's guarantee, listed in §2's *What the library guarantees*).
  slash-commands gains a one-paragraph cross-reference under the verb surface. anti-patterns gains
  "a report printed to chat" and "DevTools_Dump in addon code". Tested clause: each report verb lands
  with logging off, reveals, one pointer, refusal writes nothing, degraded falls back.
- Bump: minor (new MUST). Index blurb, CHANGELOG, context pack, AUDIT playbook ripple per the harvest
  procedure. Watch the standard version collisions note (another session may release mid-run).
- LibKa0s: `CHANGELOG.md`, `docs/api/DebugLog/version-23.11.1.5-docs.md`, `docs/api/CONSUMERS.md`,
  `README`/`CLAUDE.md` file-size table (DebugLog.lua ~700, Diagnostics ~610).
- Each addon at adoption: `docs/debug.md` "Reports" section (CM already has one), `docs/test-cases.md`.

## 6. Rollout inventory (adoption phase, deferred per owner)

Candidate report verbs from each addon's `COMMANDS` (to confirm verb by verb at adoption):
ConsumableMaster (done locally: dump *, priority … list, aio … list → one-line lift);
AuraMaster `containers` (`settings/Slash.lua:68`); KickCD `spells` / `debug spells|events`
(`core/KickCD.lua:451`); OutfitterReborn `missing`, `iteminfo` (`settings/Slash.lua:75`, `:86`);
PanelMaster `panels` (`settings/Slash.lua:415`); PartyFrameEnhanced `status` (`settings/Slash.lua:54`);
QuickComms `why`, `check`, maybe `probe` (`settings/Slash.lua:65-73`); DropWatcher `scan`;
MultiMeters `export` (likely a window, check); LibKa0sSkinTester `widths`; BankLedger `session`;
DpsRace `results`. Others (AbsorbTracker, PGFE, PrettyChat, WhatGroup, LootHistory, SkillMaster,
CombatTrail) show no obvious report verb beyond diagnostics/list. Perf reports already go to the
console through LibKa0s-Perf.

## 7. Risks

- **Parity break at re-vendor in every addon** (new public instance members). Mitigation: plan the
  stub addition as part of each re-vendor commit; one snippet; or temporarily ignore-list them (worse:
  hides the degraded crash the parity gate exists to catch).
- **Color-pinned host tests** that read `D.buffer` (measured above). Mitigation: rewrite to the plain
  text + one view-color case.
- Skin-switch color loss if `__view` is skipped.
- `append` hot-path cost: fast path on `find("|")`; the strip runs only on escaped lines.
- A host that relied on Copy carrying escapes (e.g. pasting a colored chat-format string back): the
  `||` protection keeps `Out:escape`-style deliberate escapes intact; a raw live code is no longer
  copyable, which is the point.
- Cap: a report larger than the diagnostics cap truncates; CM's largest (`dump item`, `priority list`)
  is far below 1200.
- File-size band: Diagnostics ≈ 610 lines, fine; shell ≈ 700, fine.

## 8. Decisions for the owner (recommended answer first)

- **D1 Where do Report and Serialize live?** In `DebugLogDiagnostics.lua` (minor 11), reusing its
  append/cap/strip/emit plumbing. (Alt: new `DebugLogReport.lua`.)
- **D2 A raising report body?** pcall it; write what was collected plus one `<title> failed: <err>`
  line, still reveal and point. (Alt: let it raise like CM's does.)
- **D3 Keep view colors across a skin switch?** Yes, via a private parallel `__view` array.
  (Alt: accept plain re-render after a skin switch.)
- **D4 How do host tests pin colors of a report line?** Through the view (`f.log.AddMessage`
  capture), no new public reader. (Alt: public `D:FindViewLine`, one more stub member.)
- **D5 What does Add's strip do to `|n` and raw newlines?** `|n` → space, raw newline kept.
  (Alt: identical to diagnostics' strip, both → space.)
- **D6 Serialize on the instance (stub member) or lib-level only?** On the instance as a forwarder,
  so the degraded arm can answer it; stub returns one line. Returns lines, does not write.
- **D7 Does Report turn logging on, as diagnostics does?** No. A report is not a trace; the ruling
  says it lands "whether or not trace logging is on" and says nothing about enabling.
- **D8 Pointer wording?** `"<title>: N lines written to the debug console. Use Copy to share it."`,
  N including the header, title without the slash (CM's shipped wording; the issue's example).
- **D9 Re-vendor scope for this issue:** each addon's re-vendor commit adds `Report` + `Serialize` to
  its stub (required for green), and CM's three color tests are rewritten; moving report verbs onto
  `D:Report` (including CM's one-line lift) is adoption, deferred.
