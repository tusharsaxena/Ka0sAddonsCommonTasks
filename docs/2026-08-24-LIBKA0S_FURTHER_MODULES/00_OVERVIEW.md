# LibKa0s further modules — analysis, spec and plans

**For [LibKa0s #2](https://github.com/tusharsaxena/LibKa0s/issues/2) — "Decide which further modules
move into LibKa0s".** Produced 2026-08-24.

**Nothing in this bundle has been executed.** No module was extracted, no addon was edited, no issue
was opened or relabelled, and no library release was cut. Every file here is a document.

## The files

| File | What it is |
|---|---|
| [`01_ANALYSIS.md`](01_ANALYSIS.md) | The evidence. Every candidate in the register measured against the working trees of eleven addon repos, plus two the register does not carry |
| [`02_SPEC.md`](02_SPEC.md) | The design for items #1–#5 of the analysis's ranking — four library contracts, one bug fix and the console's line cap, with the constraints that bind all of them |
| [`03_PLAN_A_POOL_LEAK_FIX.md`](03_PLAN_A_POOL_LEAK_FIX.md) | LootHistory's chart-pool leak. Ships alone, first, touching no library |
| [`04_PLAN_B_LIBKA0S_MODULES.md`](04_PLAN_B_LIBKA0S_MODULES.md) | `Env`, `Pool` and `Item` majors, `Widgets.CopyWindow`, and `MAX_BUFFER` 500 → 1500, released as v1.14.0 and re-vendored into nine addons |
| [`05_PLAN_C_ENV_ADOPTION.md`](05_PLAN_C_ENV_ADOPTION.md) | Nine addons adopt `LibKa0s-Env-1.0` |
| [`06_PLAN_D_POOL_AND_ITEM_ADOPTION.md`](06_PLAN_D_POOL_AND_ITEM_ADOPTION.md) | BankLedger and LootHistory adopt `LibKa0s-Pool-1.0` and `LibKa0s-Item-1.0` |
| [`07_PLAN_E_COPYWINDOW_ADOPTION.md`](07_PLAN_E_COPYWINDOW_ADOPTION.md) | BankLedger, LootHistory and MultiMeters adopt `Widgets.CopyWindow` |

## What the analysis changed about the register

The two candidates #2 lists as live are the two weakest, and the strongest is not in the register at
all:

- **The copy-paste window is on its fourth copy, not its third.** BankLedger has one, nobody recorded
  it, and MultiMeters' own source comment — the comment the register entry was written to
  substantiate — names itself the third and is wrong.
- **The widget pool is not in the register, and LootHistory's copy leaks.** Its `releaseAll` never
  returns anything to the free list, so 35 pools reallocate every frame on every re-render.
- **The `Item` case has weakened.** The bug that justified it is fixed, and the two addons have since
  adopted deliberately opposite uncached policies — so the primitives move and the resolver does not.
- **The `Env` cluster should be promoted out of the `Compat` bullet.** Eleven implementations of one
  six-line function across nine addons, in four spellings, with no behavioural difference.
- **The message bus should be declined.** Its whole shared surface is six lines wrapping
  `AceEvent:Embed`; the rest of each file is a per-addon message catalog that cannot move.

## Order of execution

```
03  LootHistory pool leak fix ──────────────────────────► alone, first
04  library work → LibKa0s v1.14.0 → re-vendor × 9  (carries MAX_BUFFER = 1500)
        ├─ 05  Env adoption        × 9
        ├─ 06  Pool + Item adoption × 2
        └─ 07  Copy window          × 3
```

Adoption order is cheapest and least contentious first. `Env` and `Pool` are pure functions with no
frames and no art, so they carry full headless coverage and need no smoke test; the copy window needs
one in-client check per addon and is therefore last. Every addon's adoption is an independent commit,
and an addon that has not adopted is still correct.

## The console's line cap

Added after the bundle was first written, on request. `lib.MAX_BUFFER` goes **500 → 1500** —
**one** number, because the copy window shows `table.concat(D.buffer, "\n")` and caps nothing of
its own, so the buffer cap *is* the copy cap. It rides inside v1.14.0 rather than shipping as its
own DebugLog release, because two consumer suites pin the old literal and go red the moment the
library file changes; folding it in means the sweep that fixes them is the sweep B–E already pay
for. `02_SPEC.md` §F has the reasoning and the full ripple; `04_PLAN_B` Task 4b and Task 8 Step 3b
do the work.

## What is deliberately not here

No message-bus module, no wholesale `Compat` extraction, no merged item resolver, and no conversion
of `LibKa0s-DebugLog-1.0`'s own copy window. `01_ANALYSIS.md` §4 and §5 and `02_SPEC.md`'s
non-goals say why for each.
