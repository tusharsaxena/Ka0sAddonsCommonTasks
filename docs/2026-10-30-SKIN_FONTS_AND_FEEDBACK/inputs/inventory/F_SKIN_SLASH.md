# F_SKIN_SLASH: `/xx skin` in every addon (owner item 12)

Read-only inventory. I read every repo's working tree on `feat/2026-10-30-skin-library-followups`, which is the
follow-ups run (LibKa0s v1.81.0) and was not yet merged when I read it. Line numbers refer to that tree.

## 1. How the shared verbs work today

**The library never registers a verb.** `LibKa0s-Slash-1.0` owns dispatch, help, the schema CLI and the parser,
but each host passes in the `COMMANDS` table as plain data: `LibKa0s/LibKa0s/Slash.lua:9-13`, and `lib:New(d)`
at `Slash.lua:447`. Dispatch is an exact match on `entry[1]` (`Slash.lua:794-799`, `OnSlash` at `:801`), after
`d.aliases` resolve (`:827`).

- The standard makes this binding. `slash-commands-§3` says "The ordered verb table **MUST** live in the addon
  ... never owned by the library", because the landing page renders the same table and a library-owned table
  would create an Options→Slash dependency cycle (`WowAddonStandards/standards/standards/slash-commands.md:51-55`).
  `slash-commands-§2` says the same for `perf`: "the verb **MUST** be registered by the addon through its own
  `COMMANDS` table, never by the library" (`slash-commands.md:40`).
- **The library-wide verbs (`diagnostics`, `perf`, `sim`) were each a per-addon rollout.** In each case the
  library ships the act and every addon adds a row:
  - `NS.DebugLog:RunDiagnostics()` / `D:DebugVerb(rest)` (`DebugLogDiagnostics.lua:391-416`)
  - `P.OnCommand(args)` (`PerfCommands.lua:214`)
  - `sim.RunVerb()` (`Sim.lua:670`)

  The canonical row shapes are at `slash-commands.md:62-84`. For example, LootHistory's rows:
  `LootHistory/settings/Schema.lua:1205` (diagnostics), `:1210` (perf), `:1226` (sim).
- **The disabled gate.** `lib.LIVE_VERBS` lists the 13 reserved verbs that still answer while the addon is
  disabled (`Slash.lua:124-127`). Any other registered verb gets the one `DisabledLine` (`Slash.lua:851`).
  Some hosts restate the set and gate at the table as well, for example `LootHistory/settings/Schema.lua:1102-1137`
  (`gateFeatureVerbs`) and `DropWatcher/settings/Slash.lua:87` (`NS.SLASH_LIVE_VERBS`).

So **`/xx skin` cannot come free from the library** without reversing slash-commands-§3. Every addon needs one
`COMMANDS` row. What the library can provide is the act behind that row, so 16 addons do not write 16 copies.

## 2. How the first-run picker opens today

- **Library side.** `O.SkinPicker(spec)` is in `LibKa0s/LibKa0s/OptionsSkinPicker.lua:770-784` (file minor 2,
  `:105`), and `O.HideSkinPicker()` is at `:788`.
  - It answers the frame. It answers `nil, "queued"` when another owner's picker is up, or when the queue is
    waiting out combat (`:776-778`). It answers `nil` when there is no Skin major, no `CreateFrame`, or the owner
    is unregistered (`pickerTarget`, `:751-758`).
  - **It does not check `pickerSeen`.** The "seen" gate belongs to the host.
  - A first call with nothing up **shows even in combat**. Only the queue's next owner waits out combat
    (`:53-58`, `:209-212`). Picks, Apply, Apply to all and the gear are refused in combat through
    `O.__combatRefused` (`:335-337`).
- **Host side.** The shape is uniform across all 15 addons (ConsumableMaster uses `KCM.`). Each has
  `core/SkinSetup.lua` with three functions:
  - `NS.SkinPickerSpec()` builds the spec: owner, get, set, page/tab, onPreview (the eye) and `onClose`, which
    writes `settings.appearance.pickerSeen = true`. LootHistory's is at `LootHistory/core/SkinSetup.lua:384-395`.
  - `NS.MaybeShowSkinPicker()` shows the picker only if `pickerSeen == false`, the addon is not stood down, and
    the player is not in combat. In combat it holds the call for `PLAYER_REGEN_ENABLED`
    (`LootHistory/core/SkinSetup.lua:400-437`).
  - `NS.HideSkinPicker()` closes quietly and writes no seen flag (`:407-415`).

  Where each addon's functions are:

  | Addon | Spec / Hide / MaybeShow (file:line) |
  |---|---|
  | AbsorbTracker | `core/SkinSetup.lua:186/211/223` |
  | AuraMaster | `:291/314/326` |
  | BankLedger | `:400/428/440` |
  | ConsumableMaster | `:367/393/405` |
  | DpsRace | `:396/420/432` |
  | DropWatcher | `:417/434/447` |
  | KickCD | `:301/325/337` |
  | LootHistory | `:384/407/419` |
  | MultiMeters | `:374/391/403` |
  | PanelMaster | `:250/285/298` |
  | PartyFrameEnhanced | `:203/231/244` |
  | PGFE | `:241/261/277` |
  | PrettyChat | `:253/270/281` |
  | QuickComms | `:345/377/390` |
  | WhatGroup | `:232/257/271` |

- **LibKa0sSkinTester already has the on-demand form.** It keeps the spec in `NS.SKIN_PICKER_SPEC`
  (`settings/Panel.lua:166`). `NS.ShowSkinPicker()` (`settings/Panel.lua:200-208`) shows the picker whether or
  not the profile has seen it, and refuses while disabled or in combat, silently. Its showroom "Show the picker"
  button calls it (`modules/ShowroomWidgets.lua:179`). This is the prototype for the verb.
- **Every addon's Options degradation stub carries `SkinPicker` / `HideSkinPicker`**, for example
  `AbsorbTracker/settings/OptionsSetup.lua:348-349` and `BankLedger/settings/OptionsSetup.lua:268-269`.
  `Kit.assertSurfaceParity` compares each stub against the live instance (`skinning.md` §3 *Degradation*;
  `ConsumableMaster/tests/test_surface_parity.lua:273-282` lists the members). **Any new `O.*` member is
  therefore owed by all 16 stubs.**

## 3. Collision check, every addon

No addon has a `skin` verb or an alias for one. I grepped for `{ "skin|skins|picker|theme|look",` in every
non-vendored `.lua` file and checked each `aliases` map. The aliases are only `options→config` in AT, AM, DR,
KCD, MM and PFE (for example `AbsorbTracker/settings/Slash.lua:720`) and `rewrite→rewritemacros` in CM
(`ConsumableMaster/settings/Slash.lua:145`). There is no prefix matching, so nothing shadows the verb.

| Addon (slash) | COMMANDS table | Near-miss to note |
|---|---|---|
| AbsorbTracker `/at` | `settings/Slash.lua:71` | none |
| AuraMaster `/am` | `settings/Slash.lua:39` | `pick` = attach a container to a frame (`:78`). No collision, but the help text must not say "pick" for the skin. |
| BankLedger `/bl` | `settings/Schema.lua:924` | none |
| ConsumableMaster `/cm` | `settings/Slash.lua:164` (+ sub-trees in `core/SlashCommands.lua`) | none at top level |
| DpsRace `/dr` | `settings/Slash.lua:30` | none |
| DropWatcher `/dw` | `settings/Slash.lua:27` | none |
| KickCD `/kcd` | `core/KickCD.lua:247` | none |
| LootHistory `/lh` | `settings/Schema.lua:1139` | none |
| MultiMeters `/mm` | `settings/Slash.lua:85` | `"skin"` is a color-mode *value* (`defaults/Profile.lua:132`), not a verb |
| PanelMaster `/pm` | `settings/Slash.lua:381` | none |
| PartyFrameEnhanced `/pfe` | `settings/Slash.lua:22` | none |
| PGFE `/pgfe` | `settings/Slash.lua:22` | none |
| PrettyChat `/pc` | `settings/Slash.lua:46` | none |
| QuickComms `/qc` | `settings/Slash.lua:25` | none |
| LibKa0sSkinTester `/st` | `settings/Slash.lua:22` | `show` opens the showroom, not the picker |
| WhatGroup `/wg` | `settings/Slash.lua:40` | none |

**Every addon needs code.** That means one row, one small host handler, one stub member, and test updates.
Nothing comes free.

## 4. Proposed change

### 4a. LibKa0s (`LibKa0s-Options-1.0`, `OptionsSkinPicker.lua` minor 2 → 3)

The precedent is `D:DebugVerb`: the act and its words live in the library, and the row lives in the host.

- **A new member, `O.SkinVerb(spec)`.** It is the `skin` verb's act: the same picker a new profile shows, on
  demand, whatever `pickerSeen` says.
  1. **In combat** (`InCombatLockdown()`, the same predicate as the file's `inLockdown`, `:186`), it prints
     `SKIN_PICKER_STRINGS.VERB_COMBAT` through `O.__print` **every time**, writes one `Cfg` line through
     `d.debug` (`"skin picker <owner> refused (in combat)"`), and answers `nil, "combat"`. It must not reuse
     `O.__combatRefused`, because that prints its notice once per combat, so a second `/xx skin` in the same
     fight would print nothing.
  2. Otherwise it calls `O.SkinPicker(spec)`.
     - Frame → answer it. If the same owner's picker is already up, it refreshes in place.
     - `nil, "queued"` → print `VERB_QUEUED` and answer `nil, "queued"`.
     - `nil` → print `VERB_UNAVAILABLE` and answer `nil, "unavailable"`.
- **New keys in `lib.SKIN_PICKER_STRINGS`** (`:117-129`), ASCII only (item 5's glyph rule), `spec.strings`
  overriding as usual:
  - `VERB_HELP = "Choose a skin: open the skin picker"`, exported so hosts and the standard name one wording.
  - `VERB_COMBAT = "|cffaaaaaacannot open the skin picker during combat|r"`, gray like `COMBAT_REFUSED`.
  - `VERB_QUEUED = "Another Ka0s addon's skin picker is open; this one opens when it closes."`
  - `VERB_UNAVAILABLE = "Skins are unavailable: LibKa0s-Skin-1.0 did not load."`
- **Bookkeeping.** Bump the `PICKER_MINOR` header block, `lib.MODULES.OptionsSkinPicker = 3`, and publish a new
  `docs/api/Options/version-<key>-docs.md` that names `SkinVerb` as a member **every Options stub owes**.
  Update `CHANGELOG.md` and `docs/api/CONSUMERS.md`.
- **Tests.** Add a new suite, `tests/test_options_skin_verb.lua`, because `test_options_skin_picker.lua` is
  already 1064 lines. Each case falsifies the behavior it pins:
  1. Shows the picker on a profile that has seen it, with the same spec and `onClose` run once.
  2. In combat: shows nothing, prints exactly one `VERB_COMBAT` line, and prints it again on a second call in
     the same combat (red under: routing through `__combatRefused`).
  3. With another owner's picker up: answers `nil, "queued"`, prints one `VERB_QUEUED` line, and the picker
     shows when the other closes.
  4. A repeat while its own picker is up: one window, preview kept.
  5. No Skin major, or an unregistered owner: one `VERB_UNAVAILABLE` line, no frame.
  6. One `Cfg` line on the combat refusal, through `d.debug`.

  Also extend the minor/attach case at `test_options_skin_picker.lua:174` to three members.

The Slash major does **not** change. `skin` is **not** added to `lib.LIVE_VERBS`; see Q2.

### 4b. Each of the 16 addons, the same five edits

1. **A `COMMANDS` row placed directly after `config`**, so the help index groups the settings surfaces:

   ```lua
   {"skin", L["Choose a skin: open the skin picker"], function() NS.RunSkinVerb() end},
   ```

   - The help string is the same English key in every addon, as `diagnostics` is, and is added to
     `locales/enUS*.lua`.
   - LibKa0sSkinTester's table is `settings/Slash.lua:22-45` (`Tester.COMMANDS`). KickCD's is
     `core/KickCD.lua:247`. LootHistory and BankLedger keep theirs in `settings/Schema.lua`, and there the
     `gateFeatureVerbs` wrap applies to the new row automatically.
2. **`NS.RunSkinVerb()` in `core/SkinSetup.lua`**, next to `NS.MaybeShowSkinPicker`:

   ```lua
   O.SkinVerb(NS.SkinPickerSpec())
   ```

   Using `SkinPickerSpec()` means "the same picker a new profile shows" holds by construction. On the
   Options-stub answer `nil, "absent"`, it prints the collection's library-absent line
   `L["%s is unavailable: the LibKa0s library did not load."]:format(SLASH .. " skin")` (slash-commands-§1).
   LibKa0sSkinTester routes it with `NS.SKIN_PICKER_SPEC` instead, and can keep `NS.ShowSkinPicker` for the
   showroom button.
3. **The Options stub** (`settings/OptionsSetup.lua`) gains `SkinVerb = function() return nil, "absent" end`
   (`Kit.assertSurfaceParity`). ConsumableMaster's `tests/test_surface_parity.lua:282` gains `"SkinVerb"` in its
   member list.
4. **The Slash degraded stub.** Add `skin` to the set of verbs not offered without the library, for example
   LootHistory's `UNAVAILABLE_WITHOUT_LIB` (`settings/Slash.lua:306-309`), CM's library-routed set
   (`settings/Slash.lua:147+`), and the KickCD/DR/DW/QC/PC equivalents. Their help-row cases
   (`tests/test_slash_degraded.lua`) gain the row.
5. **Tests.**
   - Update the help, landing and verb-count pins: AT `test_slash*.lua`, AM `test_slash.lua`, BL
     `test_libka0s_slash.lua`/`test_slash.lua`, CM `test_slash*.lua`, DR `test_skeleton.lua`, DW/KCD/MM/QC
     `test_slash.lua`, LH `test_panel.lua`/`test_schema.lua`, PM `test_panel.lua`/`test_slash.lua`, PFE/PC/WG
     `test_slash.lua`, PGFE `test_setup.lua`.
   - Add `test_disabled.lua` step 7 coverage. The suite dispatches every `COMMANDS` entry while disabled, so
     `skin` must refuse with exactly one `DisabledLine` and write nothing. Where a suite pins per-verb outcomes
     (AM, DR, DW, KCD, MM, QC), add the row.
   - Add one host case in `test_skinsetup.lua` (or `test_skin_picker.lua` for the tester): `/xx skin` shows the
     picker on a profile with `pickerSeen = true`, and closing it leaves `pickerSeen` true.

The standard's `/<slash> perf` and `diagnostics` rollouts are the size model for this: one commit per addon,
and a re-vendor to the new tag first.

### 4c. WowAddonStandards: proposed text (minor bump, for example v2.93.0)

**`slash-commands-§2`, the reserved list** (`slash-commands.md:40`). Add `skin` after `diagnostics` in the
sentence "`help`, `get`, ... **`perf`** and **`diagnostics`** are reserved", and append this paragraph:

> **`skin` opens the skin picker (skinning-§3) and is registered in every addon that has adopted skins**,
> on the same footing as `diagnostics`: reserved always, and registered by the addon through its own
> `COMMANDS` table, never by the library. It shows the **same picker a new profile shows**: the host's
> first-run spec, handed to the library's `O.SkinVerb(spec)` (`LibKa0s-Options-1.0`, from `LibKa0s
> v<tag>`), whatever the profile's *picker seen* flag says. A close still marks the profile seen. The help
> row reads `Choose a skin: open the skin picker`. The verb takes no argument, and a word after it is
> ignored. In combat it **MUST** refuse with the library's one gray line and show nothing, on every
> call, because a typed command that answers nothing reads as broken. While another Ka0s addon's picker
> is up, it **MUST** say that this one is queued, not stay silent. It is a **feature verb**, not a live
> one: while the addon is disabled, slash-commands-§7's refusal line answers it (the Skin tab is still
> reached through `config`). It **MUST NOT** be given an alias (`theme`, `look`) or a second meaning,
> and **MUST NOT** be hand-built: an addon that opens its own window for it is anti-pattern #47.

Then:

- Add the `skin` row to **`slash-commands-§3`'s canonical `COMMANDS` example**, after `config`.
- In **`slash-commands-§7` step 7**, leave the live list unchanged, and add one sentence: "`skin` is a feature
  verb and refuses."
- In **`skinning-§3`**, after *Drawn by the library*, add: "**On demand.** `/<slash> skin` shows the first-run
  picker at any time (slash-commands-§2); the Options degradation stub owes `SkinVerb` beside `SkinPicker` and
  `HideSkinPicker`."
- Ripple: `STANDARDS.md` changelog line, `CHANGELOG.md`, `NEW_ADDON_CONTEXT.md` (the verb list), the
  `NEW_ADDON.md` scaffold's `COMMANDS`, and the audit checklist if it enumerates the reserved verbs.

## 5. Risks

- **The stub-parity cascade.** Once an addon re-vendors the new tag, `Kit.assertSurfaceParity` goes red until
  its Options stub gains `SkinVerb`. Re-vendor and stub must land in one commit per addon, as the `SkinPicker`
  members did at v1.80.0.
- **Picks in combat.** A picker opened just before combat stays up. Picks are already refused in combat
  (`OptionsSkinPicker.lua:588` test), so the verb adds no new risk here.
- **The `onClose` seen-write.** Writing `pickerSeen = true` on a profile that already has it writes the same
  value again, which may log one `[Set]` debug line. That is harmless; whether a same-value write logs is up to
  each host's seam.
- **A held first-run start.** If a first-run start is held for `PLAYER_REGEN_ENABLED` and the player types
  `/xx skin` after combat, the verb shows the picker and the held start then shows the same owner's picker,
  which refreshes the same window (`OptionsSkinPicker.lua:780-783`). No second window opens.
- **AuraMaster's `pick` verb.** It sits next to `skin` in the help index, so the help wording must keep "pick"
  for frames only.
- **Help/landing pins in about 30 test files** need a one-row bump. This is mechanical, but it touches every repo.

## 6. Open questions for the lead

1. **Does the act go in the library (`O.SkinVerb`) or is each host composed from `O.SkinPicker`?**
   *Recommend the library.* It puts one wording and one combat/queued behavior in one place (the `DebugVerb`
   precedent), and the cost, a stub member per addon, is owed either way because the row is too. Composing it
   per host means 16 copies of about 15 lines, which is the duplication testing-§8 forbids.
2. **Disabled state: is `skin` a feature verb (refused) or a live verb (added to `LIVE_VERBS`)?** *Recommend a
   feature verb.* `pickerDue` already never shows the picker while the addon is stood down, LibKa0sSkinTester's
   `ShowSkinPicker` refuses while disabled, the eye's test-mode preview cannot run while disabled, and the Skin
   tab stays reachable through `config`. Going live would mean a Slash-major change, standard text for 14
   reserved live verbs, and an edit to every host's restated live set.
3. **Combat: refuse or defer?** *Recommend refuse, with one line on every call*, as `config`
   (`COMBAT_REFUSED`) and `profile` (`PROFILE_COMBAT`) do. Deferring would pop a window up after the fight that
   the player may have forgotten asking for. The first-run path defers only because nobody asked for it.
4. **Arguments: `/xx skin <name>` to set a skin directly?** *Recommend not in this run.* Treat the verb as bare
   and ignore extra words, which keeps `skin <key>` open for later. `/xx set settings.appearance.skin <key>`
   already sets it from chat.
5. **Is `skin` a reserved verb in the standard (MUST) or a SHOULD?** *Recommend reserved and MUST in every
   adopted addon.* The owner asked for "every addon", and all 16 have adopted skins.
6. **LibKa0sSkinTester: should the showroom button also go through `O.SkinVerb`, so it gets the queued and
   combat lines?** *Recommend yes.* It is a small change and makes the button and the verb behave the same way.
