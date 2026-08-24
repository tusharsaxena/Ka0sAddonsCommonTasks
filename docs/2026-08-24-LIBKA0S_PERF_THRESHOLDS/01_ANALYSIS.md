# 01 — Analysis: perf regression thresholds and gates

**For [LibKa0s #1](https://github.com/tusharsaxena/LibKa0s/issues/1) — "Perf: set regression
thresholds and gates once baselines exist".**

Produced 2026-08-24. **Analysis only — nothing here has been executed.** No threshold was set, no
code, doc or issue was changed in any repo, and no capture was taken. Every figure below was
recomputed from the committed `dump.json` files rather than copied from an existing write-up.

---

## The short version

The issue is blocked on "rollout step 5 — all six consumers wired and producing captures". **That
gate is unreachable, not late**, and it should be retired rather than waited on: three of the six
consumers it counts have since ratified a decline of the `Perf` major, and one addon that was never
in the six has adopted it.

More importantly, the three captures that *do* exist answer the issue's second question
decisively — and the answer is no:

> **`deltaMsPerFrame` cannot carry a threshold. In all three captures it is negative** — the arm
> running *more* code measured *faster* — and its noise floor is between 3× and 89× larger than the
> cost it is being asked to resolve.

What the captures *can* carry a threshold on is per-bucket `ms/s` and per-call `maxMs`. Both are
measured directly rather than inferred from a difference between two arms, and both are stable
enough to compare.

---

## 1. What is actually deployed

Not six consumers. Nine addons, four postures:

| Posture | Addons | Captures on disk |
|---|---|---|
| Wired **and** captured | AbsorbTracker, ConsumableMaster, KickCD | 1 each |
| Wired, never captured | **MultiMeters** | 0 |
| Declined, ratified under `performance-§12` | BankLedger, LootHistory, PrettyChat, WhatGroup | n/a |
| Declined, **not** ratified — an open MUST | PanelMaster | n/a |

The six consumers named in the rollout were AbsorbTracker, KickCD, LootHistory, BankLedger,
ConsumableMaster and WhatGroup. **Three of those six — LootHistory, BankLedger and WhatGroup — now
carry ratified `performance-§12` no-combat-path exemptions.** They have no `core/PerfSetup.lua`, no
`perf` verb and no `docs/perf-analysis/` store, and they are not going to grow one; LootHistory's
`docs/performance.md` argues the point at length, including that `suspend` would suppress the very
loot the addon exists to record.

So the gate as written counts three addons that will never satisfy it. Waiting on it is waiting on
nothing.

**The one capture genuinely missing is MultiMeters'** — wired, never run. It is also the addon most
likely to have a cost worth measuring: a damage meter is the only thing in the collection doing
per-combat-event work at scale, and the three existing captures are all of addons whose cost is, as
shown below, near the floor of the instrument.

---

## 2. The baselines, recomputed

Every figure recomputed from the committed `dump.json`. Nested buckets are excluded from the totals
(`paintBar` inside `repaintPass`; `pollSpell` and `spellState` inside `spellPoll`; `iconApply`
inside `spellState`), so each total is the top-level bracketed work and nothing is double-counted.

| Addon | Version | Active window | Bracketed total | **ms/s** | ms/frame | Share of one frame | Measured `deltaMsPerFrame` |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | 1.9.0 | 26.60 s / 1606 f | 9.06 ms | **0.34** | 0.0056 | 0.034 % | **−0.1777** |
| ConsumableMaster | 1.5.0 | 24.01 s / 1596 f | 42.72 ms | **1.78** | 0.0268 | 0.178 % | **−0.1082** |
| KickCD | 1.2.1 | 25.65 s / 1772 f | 161.63 ms | **6.30** | 0.0912 | 0.630 % | **−0.1740** |

All three were captured on 2026-08-07, each a single ~25-second run on one character. **n = 1 per
addon**, which is the second reason not to write a number into a gate yet.

### The delta arm does not work at this scale

The negative sign is not a rounding artifact — it is the instrument reporting that the difference it
was built to measure is smaller than its own noise. AbsorbTracker's own
`docs/perf-analysis/20260807-125002/ANALYSIS.md` reached this in August and put the resolution floor
at **±0.3–0.5 ms/frame**; this analysis agrees and quantifies the gap:

| Addon | Bracketed cost | Noise floor ÷ signal | \|measured delta\| ÷ signal |
|---|---|---|---|
| AbsorbTracker | 0.0056 ms/frame | **53× – 89×** | 32× |
| ConsumableMaster | 0.0268 ms/frame | **11× – 19×** | 4× |
| KickCD | 0.0912 ms/frame | **3.3× – 5.5×** | 1.9× |

Even KickCD — the most expensive addon in the collection by a factor of nineteen — sits three to five
times under the floor. A threshold on `deltaMsPerFrame` would not be a loose threshold; it would be a
threshold on a number whose *sign* has been wrong in three out of three observations.

### The spread kills a shared default

**0.34 → 6.30 ms/s is an 18.5× spread across three addons.** A single ceiling in the library would
have to be set either near KickCD's 6.3 ms/s — where it would never fire for anyone, including a
KickCD that got twice as slow — or near AbsorbTracker's 0.34, where KickCD is permanently red on
day one for behaviour that was accepted at review.

---

## 3. The three decisions the issue defers

### (1) "Does any threshold gate CI, or is this report-only?"

**The question conflates two instruments, and only one of them can gate anything.**

| | `tests/perf.lua` (offline) | `docs/perf-analysis/` (in-game) |
|---|---|---|
| Runs in CI | **Yes** | **No — CI has no game client** |
| Asserts | API calls, bytes allocated per iteration | wall-clock ms |
| Determinism | deterministic | varies by machine, spec, fight, pull |
| Present in | AbsorbTracker, ConsumableMaster, KickCD, MultiMeters | same four, three with data |
| Today | `"status":"pass"`, `"gating":false`, `"gates":{"release":true}` | frozen bundles, read by hand |

`tests/perf.lua` already refuses to assert wall-clock time, and says why in its own header: timings
"vary with the machine and the CPU governor and would turn this into a flake generator nobody
reads." It is the CI-able instrument and it is already release-gated by the automated-test battery.

**Recommendation.** The in-game capture stays **report-only**, permanently and by nature — not as a
deferral. If a threshold is ever to gate anything automatically, it belongs on the offline suite's
deterministic counters (calls, bytes), where a regression is a fact rather than a measurement. Those
two answers should be recorded separately, because they are separate questions that this issue has
been carrying as one.

### (2) "Per-bucket ms/s, a single delta-ms-per-frame, or both?"

**Per-bucket `ms/s`, plus a per-call `maxMs` ceiling. Not `deltaMsPerFrame` — see §2.**

`ms/s` is measured directly inside the active window rather than inferred from the difference
between two arms, so it does not inherit the delta's noise. It is also the number that already
appears in every capture and that a reader can compare across runs without re-deriving anything.

`maxMs` is the one signal in these captures that is unambiguously resolvable at the per-call level,
and it catches the failure that `ms/s` averages away — a rare, expensive call. KickCD's record has
three worth naming:

| Bucket | Calls | Total ms | **Max single call** | As share of one 14.5 ms frame |
|---|---|---|---|---|
| `spellPoll` | 399 | 135.26 | **1.7497 ms** | **12.1 %** |
| `spellState` | 1171 | 54.39 | 1.4186 ms | 9.8 % |
| `iconApply` | 2342 | 50.03 | 1.3961 ms | 9.6 % |

A single call eating an eighth of a frame is visible to a player as a hitch in a way that 6.3 ms/s
spread across a second is not — and unlike the delta, it is 3–4× *above* the instrument's floor
rather than below it.

### (3) "Thresholds in the lib as shared defaults, or per-addon in the descriptor?"

**Per-addon, in the descriptor.** The 18.5× spread in §2 settles it: there is no shared number that
is meaningful for both AbsorbTracker and KickCD, and buckets are per-addon concepts anyway —
`cooldown`, `spellPoll` and `repaintPass` are not comparable quantities that happen to differ in
magnitude, they are different work.

What belongs in the library is the **mechanism**, not the numbers: a place in the descriptor to
declare a ceiling per bucket, and the comparison and reporting that reads it. That is the same split
the collection already uses for art in `LibKa0s-Widgets-1.0` — the library owns the behaviour, the
host owns the values, because a vendored copy cannot know what it was vendored into.

---

## 4. Recommendation

1. **Retire "rollout step 5" as the gate on this issue.** It counts three addons with ratified
   declines. The reachable ceiling is four wired consumers, of which three have captured.
   [LibKa0s #3](https://github.com/tusharsaxena/LibKa0s/issues/3) (CurseForge) is parked behind the
   same dead gate and needs the same correction.
2. **Take one MultiMeters capture.** It is the only missing one, and it is the only addon likely to
   produce a cost the instrument can actually resolve. Until then every baseline in hand belongs to
   an addon sitting under the noise floor.
3. **Then set per-bucket `ms/s` and `maxMs` ceilings per addon in the descriptor**, report-only, with
   the library owning only the declaration and the comparison.
4. **Record the CI answer separately** against the offline suite, where it is a different and
   answerable question.
5. **Do not write a `deltaMsPerFrame` threshold.** On this evidence the field cannot support one at
   any addon in the collection. Whether the two-arm protocol is worth keeping at all — given that it
   has now failed to resolve its target in three of three captures — is a larger question than this
   issue, and belongs with
   [LibKa0s #5](https://github.com/tusharsaxena/LibKa0s/issues/5) (in-combat and out-of-combat
   capture variants), which proposes changing what the arms measure.

Item 2 is the only one that needs a player at a keyboard. Items 1, 3, 4 and 5 are decisions.

---

## 5. One defect found on the way

**A `within` can name a bucket that is not in the record.** AbsorbTracker's capture has
`visibility` declared `within = "appearance"` (`core/PerfSetup.lua:72`), and `appearance` is a real
declared bucket (`:68`) — but it recorded no calls in that run, so it is absent from the record
entirely. A reader reconstructing the nesting from the record alone hits a dangling parent.

That matters because reconstructing the nesting from the record alone is exactly what `within` was
added for. `LibKa0s/docs/record-schema.md` introduces it as carried on each bucket "so a reader can
reconstruct the nesting without the addon's source in hand" — and here they cannot.

It did not affect the totals above (a parent with no calls contributes nothing, so treating
`visibility` as top-level neither drops nor double-counts anything), and it is a schema-2
data-integrity nit rather than a perf finding. **Not filed** — this document is analysis only. It is
worth its own LibKa0s issue: either emit declared-but-unused buckets with zero counts, or drop a
`within` whose target did not survive into the record.
