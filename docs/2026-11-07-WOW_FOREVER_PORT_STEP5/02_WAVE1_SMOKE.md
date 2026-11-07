# Wave 1 smoke: the owner's checks on WoW Forever

The checks live in each addon's own `docs/smoke-tests.md`, in its new **WoW Forever** section, and their results go on
those `Result:` lines. This file is the run sheet. Claude marks nothing passed.

## Setup (once)

Neither addon is linked into the Forever client yet (`../symlinks.txt` lists `_retail_` links only). From an elevated
Windows prompt:

```
mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\AbsorbTracker" "D:\Profile\Users\Tushar\Documents\GIT\AbsorbTracker"
mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\LibKa0sSkinTester" "D:\Profile\Users\Tushar\Documents\GIT\LibKa0sSkinTester"
```

Then fully restart the Forever client. Both checkouts are on `feat/2026-11-07-forever-port-wave1`, so the Retail
client loads the same branch.

## Checks

| Addon | Checks | Client |
|---|---|---|
| AbsorbTracker | FOREVER-1..14 (`../../../AbsorbTracker/docs/smoke-tests.md`, section *WoW Forever*) | WoW Forever |
| LibKa0sSkinTester | FOREVER-1..12 (`../../../LibKa0sSkinTester/docs/smoke-tests.md`, section *WoW Forever*) | WoW Forever |
| Both | A Retail sanity pass: log in, `/at` and `/st show` open, no Lua error. The TOC change is the only Retail-visible edit | Retail |

The checks cover the open questions in the research report that these two addons can answer:

- whether the client accepts the two-number line (FOREVER-1, no *Out of date*);
- whether `Settings.OpenToCategory` opens a LibKa0s panel (AT FOREVER-5, ST FOREVER-6);
- the Ace3 CheckBox and ColorPicker fixes (AT and ST FOREVER-5/6);
- the AceDB 40 profile key and whether SavedVariables persist across a full restart (AT FOREVER-8, ST FOREVER-7).

## Results

**Passed**, by the owner on 2026-11-08: "both absorbtracker and skintester work perfectly!". AbsorbTracker
FOREVER-1..14 and Skin Tester FOREVER-1..12 are recorded as passed on the addons' `Result:` lines (commits `fb0963c`,
`f2e408a`). New checks owed since then: AbsorbTracker FOREVER-15 and Skin Tester FOREVER-13 (the default skin per
client, `W1_DEFAULT_SKIN_AND_FOREVER_NAMES.md`).
