# Wave D smoke sheet (#79 reports, #87 sample characters, #82 tokens, #80, #81, #85)

The owner runs these in game and records **PASS**, **FAIL** (with a note) or **N/A**. The run never marks a check
passed by itself. Each id is written out in full in that addon's `docs/smoke-tests.md`. Run each check on Retail,
and on WoW Forever too where the addon ships there (**R·F**). Skill Master ships on Forever only.

**What to look for everywhere:**
- **Reports (#79):** with logging off and the console closed, a report verb opens the debug console and writes the
  report under a `/<cmd> <verb>` header. Chat gets exactly one line: `<title>: N lines written to the debug console.
  Use Copy to share it.` Copy pastes plain text, with no color codes. Help, the reserved `/x list`, short one-line
  answers, usage and refusals stay in chat and write nothing to the console.
- **Sample characters (#87):** test and sim modes show the library's shared sample people (`Sample…` / `Mock…` on
  `Samplerealm` / `Mockrealm`), never a real-looking name or a real realm.
- **Degraded installs:** with `libs/LibKa0s` renamed aside, a report prints its rows in chat with no pointer.

| Addon | Checks | What changed | Result |
|---|---|---|---|
| Absorb Tracker (R·F) | PROFILE-17, PROFILE-4, PROFILE-16, DEGRADED-5 | `/at profile list` is a console report | |
| Aura Master (R·F) | SLASH-5a | `/am containers` is a console report | |
| Bank Ledger | DIAG-33, DIAG-12, DEGRADED-17, LEDG-70, SIM-3, SIM-4 | The `/bl debug` scan and panel dumps are reports (`/bl session` is a one-line toggle and stays in chat); test and sim characters are the shared set, and the sim alt is on a fictional realm | |
| Combat Trail (R·F) | SM-CT-N21, SM-CT-D13, SM-CT-S12, SM-CT-D2, SM-CT-M6, SM-CT-P9 | `/ct ignore list`, `/ct dummy show` and `/ct race ignore show` are reports; the mock fights use the shared hunter and pet (Mockfang, alt pet Mockclaw) | |
| Consumable Master (R·F) | SLASH-18, SLASH-17 | `dump` and the list verbs go through the library's Report and serializer | |
| Dps Race | SM-DR-AD79IG, SM-DR-AD79EM, SM-DR-AD79TD, SM-DR-AD79CP, SM-DR-AD87, SM-DR-AD85A, SM-DR-AD85B, SM-DR-AD85C, SM-DR-AD85D | Ignore lists are reports; shared sample names; **the race's final-seconds countdown is now LibKa0s Callout** (gold, same position, new font and slam in place of Blizzard's BigGold digits) | |
| Drop Watcher (R·F) | SLASH-10, SLASH-5, STATE-11, SKIN-52 | `/dw scan` and other reports; shared sample names (the seeded crowd stays); an expanded row's wash clears the new row floors under Ka0s Default | |
| Kick CD | DIAG-49, DIAG-1, DIAG-2, DIAG-5, DEGRADED-15, DEGRADED-17, SIM-20, SIM-14, SIM-10 | `/kcd spells list` and the `/kcd debug …` dumps are reports; the sim uses shared names | |
| Skin Tester (R·F) | SLASH-6 | `/st widths` is a report | |
| Loot History | LED-7, TM-3, SIM-15, SIM-5 | `/lh holdings <query>` is a report (every match); the `<Class>-Ravencrest` characters are the shared set and the sim alt is on Samplerealm | |
| Multi Meters | DIAG-44, DIAG-45, DIAG-46, DEGRADED-12, SLASH-11, STATE-9, SKIN-52, SKIN-2, EXPORT-34 | Report verbs on the console; shared sample names; **Ka0s Default row stripe and hover raised to .08 / .15** (were .05 / .10) to meet the new floors | |
| Outfitter Reborn (R·F) | RP1, RP2, RP3, RP4, B3 | `/or missing`, `/or zone` and `/or iteminfo` are reports; "nothing missing" and the bank-closed refusal stay in chat | |
| Panel Master (R·F) | SLASH-8, SLASH-9, SLASH-10, DEGRADED-2 | `/pm panels` and the per-panel field dump are reports | |
| Party Frame Enhanced (R·F) | PREV-4, PREV-5, INSTALL-4, FADE-1, FOREVER-8 | `/pfe status` is a report | |
| Pretty Chat (R·F) | TEST-1, TEST-2, TEST-7, DEGRADED-6 | `/pc test` and the General page's Test button print one chat pointer | |
| Quick Comms (R·F) | DIAG-3, PREVIEW-8, FOREVER-22, FOREVER-23, FOREVER-25 | `check` (two or more lines), `why`, `probe` and `/qc preview list` are reports; a one-line verdict stays in chat | |
| Skill Master (F) | SM-PROBE-1, SM-PROBE-2, SM-TEST-1, SM-TEST-12, SM-BAR-1, SM-BAR-2, SM-BAR-3, SM-LDB-1, SM-LDB-3 | `/sm probe` is a report (one JSON line); shared sample names; **bars are now the library's `W.Bar`** (same look); **the minimap button menu gains Journal** | |
| What Group | TEST-13, POPUP-1 | The test preview's leader is a shared sample character, not `Testadin-Silvermoon` | |

PGF Extension has no wave D change: it has no report verb and no sample data, and its realm fixtures must be real
for the region lookup. Every item that doesn't apply is in `plan-data/exceptions.tsv`.

## Owner calls raised in wave D

The build keeps the behavior described until you rule.

**Report routing**
1. **Bare `/x profile` lists** (Absorb Tracker, Aura Master, Kick CD, and every addon using LibKa0s-Slash
   CliProfile) still print in chat. Treating them as reports is a library change. Report or chat?
2. **Short answers:** a one-line result stays in chat (`/or missing` with nothing missing, a one-line `/qc check`
   verdict). `/lh holdings` sends every match to the console, even a single row. `/cm stat list` (three lines) stays
   in chat. Keep these splits?
3. **Scope added by agents:** Combat Trail also moved `/ct dummy show` and `/ct race ignore show`, Quick Comms moved
   `/qc preview list`, and Panel Master made `/pm panel <name>` a report. Bank Ledger moved its `/bl debug` dumps
   instead of `/bl session`. Dps Race left `/dr results` alone, because it opens a window. Keep all of these?
4. **`/ct probe`** keeps its own chat line with the "fight for 20 s" hint instead of the single stock pointer. Keep
   it?
5. **Pretty Chat's Test button** now prints the chat pointer too (one name, one act). Should it stay silent instead?
6. **Skill Master's `/sm probe`** writes its JSON as one console line so a paste still parses. Keep that, or switch
   to a readable multi-line dump?
7. **Consumable Master degraded dumps:** without the library, a table dump prints `<table>` instead of full rows (the
   library's prescribed stub). OK?

**Sample characters**

8. **Bank Ledger test mode** keeps its eight-class mix, so the shared Samplehunter never appears. Swapping Rogue for
   Hunter would bring in all five shared characters. Swap?
9. **Sim alts off your realm:** Bank Ledger and Loot History now put the sim alt on Samplerealm (Loot History's mail
   is addressed by its full Name-Realm). Keep, or keep the alt on your realm with a sample name?
10. **Real names in docs:**
    - Drop Watcher's `docs/smoke-tests.md` quotes real players from your own runs.
    - Skill Master's `docs/forever-quirks.md` and the standard's client-quirks catalog quote "Traxex Silentshot".
    - Aura Master's `tools/` research fixtures use "Tester-Realm-US".

    Scrub them, or leave them as historical records?
11. **Drop Watcher's seeded crowd** (`modules/SimRoster.lua`) includes realm names like Stormhold. Check it for real
    realms in a later pass? And its test-mode alt Samplealt stays one word on Forever. OK?

**Look**

12. **Multi Meters' Ka0s Default rows** are raised to stripe .08 / hover .15 to meet the floors. Keep them, or
    revert `e9888cc` and record an exception?
13. **Drop Watcher's expanded-row wash** follows `list.hover`, so an expanded row looks like a hovered one. Should it
    follow `list.sel`? That changes every skin.
14. **Dps Race countdown:** the Callout's font and slam replace Blizzard's BigGold digits and pop. It is silent,
    with no Look or Sound settings tab and no voice pack. Should it get a larger size, the old pop, or a settings tab?
    Its race wiring sits in `core/CalloutSetup.lua`: keep it there, or split it into a `modules/` consumer?
