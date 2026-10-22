# WowAddonStandards v2.86.0 and dev-copilot 2.4.0: consolidated change set

**Bundle:** `docs/2026-10-22-LIBKA0S_ISSUES_45_58/` (Ka0sAddonsCommonTasks). **Branch in every touched repo:** `feat/2026-10-22-libka0s-issues-45-58`.
**Inputs:** the owner decisions in the task; `analysis.json` (clusters c45 to c58, survey); and the live text of `WowAddonStandards@6bb1bc7` (v2.85.0), `dev-copilot@276ce68` (2.3.5, byte-identical to the installed `~/.claude/plugins/cache/dev-copilot/dev-copilot/2.3.5`) and `LibKa0s@d9f9454` (unreleased v1.75.0, kit 40). Everything was read-only. This document is the design. Nothing has been written to any repo.

---

## 0. Classification, sequencing and assumptions

**Standard bump: minor, v2.85.0 → v2.86.0.** It adds new MUSTs: launcher-§6, the preview-mode marker, the documentation-§1 `gi:` credit, and the closed set of library-drawn icons. It adds one new SHOULD (TestStrip in standalone-windows) and two anti-patterns (#96, #97). The rest are clarifications: automated-tests-§3 crash handling, the library-stack-§7 `__` rule and the hazard-row correction.

**Plugin bump: minor, dev-copilot 2.3.5 → 2.4.0.** `wow-revendor-libka0s` gains behavior: the icon declaration and the prune. Three readers gain the crashed bucket.

**Order the run must keep (hard dependencies):**
1. **The standard's v2.86.0 commits on the branch**, before LibKa0s is tagged:
   - The `__` clause in library-stack-§7 must exist before or with OptionsTabs minor 9. The c45 challenger made this a precondition for the #45 payload removal.
   - LibKa0s release step 7 checks its README standards pointer against `head -1 ../WowAddonStandards/standards/STANDARDS.md`.
2. **LibKa0s v1.75.0 tagged** (kit 41). The figures in §A11 are then recounted at that commit.
3. **dev-copilot 2.4.0 merged, then the owner runs `/plugin update` and `/reload-plugins`.** This must happen before any consumer re-vendor. Per memory (*Use the installed plugin*), the sweep runs only through the installed command. The c55_57 challenger warns that a 2.3.5 sweep leaves every consumer unpruned: green, but in breach of library-stack-§7, *What ships is exactly what is declared*.
4. **Per addon:**
   - `wow-revendor-libka0s` to v1.75.0: declaration, prune, blockers and credits all in one commit.
   - The adoptions.
   - `wow-revendor-standards` to v2.86.0.
5. **GitHub issue actions** (§C), only after the owner's merge go-ahead, with spacing between writes.

**Library layout this document assumes.** It comes from the analyses. The LibKa0s design for this run is authoritative, so correct the figures in §A11 against it before committing:
- `Widgets.lua` minor 12 → 13: `SearchBox` and `TestStrip`, sharing the file-local dropdown `SKIN`.
- New `WidgetsStepPanel.lua` (WidgetsStepPanel minor 1): `StepPanel`.
- `Item.lua` minor 2 → 3: `BonusIDsFromLink`.
- New `Glow.lua` (LibKa0s-Glow-1.0, minor 1).
- New `Sim.lua` (LibKa0s-Sim-1.0, minor 1; it floors on Widgets for StepPanel).
- Comment-only minors: OptionsTabs 9 (the #45 removal), Core 11, DebugLog 20, OptionsIdList 5 (the stale icon comments).
- PerfPanel gets a minor bump only if it is rebuilt on StepPanel.
- Result: **17 majors**. Files: 36 (actual today; the standard's "thirty-four" is already stale) + 3 = **39**.

---

## A. WowAddonStandards v2.86.0: ordered edit list

Write everything in US English and LF. Cite sections as `filename-§N`. `preview-mode` and `standalone-windows` are among the eleven files with no numbered subsections, so add **only unnumbered** headings there. A `### N.` heading would make check-standard's citation check misread them.

### A1. `standards/standards/launcher.md`: new `### 6.` (MUST), plus edits to §2 and §5

**§2, the bullet "Clicking an entry toggles it through the addon's OWN handler".** After "…*Show window* through the window's own toggle (standalone-windows), or the display's `toggle` verb.", insert:

> That same handler is what the addon's Show window key binding presses (launcher-§6): the menu entry, the `toggle` verb and the key are three surfaces onto one handler.

**§2, the bullet "An entry appears exactly when…".** Leave it unchanged ("a dial opened by a keybinding" is not a primary display).

**New section, appended after §5:**

> ### 6. The Show window key binding (MUST)
>
> An addon whose launcher has a **Show window** entry (launcher-§2; its `ADDONS.md` row) **MUST** ship one key binding that toggles that window or display. A player then reaches the thing the addon exists to show without the minimap, a broker display or a slash verb. At v2.86.0 that is six addons:
> - Bank Ledger, Drop Watcher, Loot History, Multi Meters and WhatGroup owe the binding.
> - Quick Comms ships *Toggle Comms Pads*, the reference implementation.
>
> - **One binding, one handler.** The binding **MUST** be a `CLICK` binding in the addon's root `Bindings.xml` (layout-§1). It names a **plain, named, hidden, non-secure** `Button` that a module creates at load and registers with `RegisterForClicks("AnyDown")`, so one press toggles once. Its `OnClick` **MUST** call **the handler the launcher descriptor's `toggleWindow` calls**, which the `toggle` verb and the menu entry already share (launcher-§2). Not allowed:
>   - a second handler or a global function;
>   - Lua in the `<Binding>` element;
>   - a secure template. The window is non-secure (standalone-windows), and a secure button would add combat rules the window does not have.
>
>   ```xml
>   <Bindings>
>     <Binding name="CLICK <Folder>Toggle<Window>:LeftButton" header="<FOLDERUPPER>" category="ADDONS"/>
>   </Bindings>
>   ```
>
>   An addon that already ships bindings, such as Quick Comms' dials, adds this one beside them. It goes under its existing `header`, which only the file's first `<Binding>` carries.
> - **The button's name is permanent.** It is `<Folder>Toggle<Window>` (`QuickCommsTogglePads`). The client stores a player's key against the binding's name, so renaming the button silently unbinds every player's key.
> - **Labels come from the module, through the locale.**
>   - `BINDING_HEADER_<FOLDERUPPER>` is the addon's brand name, `Ka0s <Name>` (launcher-§1).
>   - `BINDING_NAME_CLICK <button>:LeftButton` is a localized label naming the action (`Toggle <window>`).
>
>   Both are assigned in the module that creates the button. The second needs `rawset`, because its name holds a space and a colon.
> - **No default key.** `Bindings.xml` **MUST NOT** carry a `default` attribute. Any key the addon picks collides with somebody's existing binding. The player chooses in the client's Key Bindings → AddOns menu.
> - **A press while stood down refuses exactly as the toggle verb does (MUST).**
>   - It toggles nothing, writes nothing, and prints **exactly one line** through the addon's own printer.
>   - The line is chosen by hold (slash-commands-§7, *Which refusal, by hold*). While the `disabled` hold is taken it is the disabled refusal line. While only the `perf` hold is taken it is `Not available during a performance capture.`, and **never** the disabled line.
>   - A press is a feature, not setup (slash-commands-§7, *The launcher while disabled*). It comes through the addon's one refusal helper:
>     - Where the toggle handler already refuses through that helper, the button just calls it.
>     - Where the handler relies on the dispatcher's gate instead, the button's `OnClick` asks the helper first.
>
>     A third wording is never acceptable.
>   - A silent press is the failure this bullet exists for. The player pressed a key and nothing told them why nothing happened.
> - **Combat.** A press follows the handler's combat contract and adds none. A non-secure window opens and closes in combat (standalone-windows). A display that a secure driver moves defers exactly as its toggle already does (Quick Comms' pads).
> - **Documented.** The README's `## Usage` names the binding and where to set it (Key Bindings → AddOns → `Ka0s <Name>`). `docs/settings-panel.md`'s launcher row lists it beside the *Show window* entry.
> - **Why this is not a library helper (recorded rejection, LibKa0s#58).**
>   - The client reads `Bindings.xml` only from the addon's root, so the file is per addon whatever a library does.
>   - A helper could own about six lines: a named button, its click registration, and two label globals. That is the high-frequency, low-content shape library-stack-§7 keeps inline.
>   - A library writing `BINDING_HEADER_*` on a consumer's behalf would split ownership of a global that an addon with bindings of its own already writes.
>   - **Re-check if** this rollout produces two or more binding buttons that diverge on correctness (a missing or wrong refusal, a double toggle, a secure template, a default key), or if a second binding per addon (Locked, Test mode) is ruled in.
> - **Commencement.** Each owing addon's next release. Missing, mis-shaped or silent bindings are **anti-pattern #96**.

**§5, "Adopting it": append one paragraph:**

> **The Show window key binding (v2.86.0) is a fourth adoption, and it needs no library tag.** Per owing addon: create the button and its labels in the module that owns the window toggle; add the `CLICK` line to a root `Bindings.xml`, creating the file if needed (layout-§1); extend `tests/test_disabled.lua` step 8 (slash-commands-§7); and document it (launcher-§6).

### A2. `standards/standards/layout.md` §1: generalize `Bindings.xml`

- **Tree comment** (lines 12–13). Replace it with:

  `Bindings.xml -- key bindings: owed by every addon with a Show window entry (launcher-§6), else ONLY if the addon ships bindings; client-mandated name and place, beside the TOC; no Lua beyond what the client requires; NOT a TOC line (layout-§1)`

- **The MUST paragraph** (line 101). Replace "a `CLICK` binding on a secure button needs none at all" with:

  > a `CLICK` binding on a named button needs none at all, whether the button is secure (Quick Comms' dial headers) or the plain, hidden button every Show window binding presses (launcher-§6)

  Replace "An addon with no key bindings has no such file." with:

  > An addon with no key bindings has no such file, and since v2.86.0 an addon with a Show window entry always has one (launcher-§6).

- **"Why the root has to hold it"** (line 103). Append:

  > Since v2.86.0 the file is no longer one addon's exception. launcher-§6 makes it owed by every addon whose launcher has a Show window entry, so the root carries it in six repositories, and the MUSTs above are unchanged for all of them.

`toc-file.md:70` ("MUST NOT list `Bindings.xml`") needs no edit.

### A3. `standards/standards/slash-commands.md` §7

- ***Which refusal, by hold*, last bullet.** Change "A feature verb, a button press and any other site" to:

  > A feature verb, a button press, a key binding's press (launcher-§6) and any other site

- ***The launcher while disabled*.** Insert a new bullet after the bullet "A launcher click MUST NOT write SavedVariables…":

  > - **A key press is a feature, and it refuses (MUST).** The Show window binding (launcher-§6) is not setup. A press while the addon is stood down toggles nothing, writes nothing, and prints the one line that *Which refusal, by hold* picks. A grayed menu entry can show its state. A key cannot, so the line is the only answer the player gets, and a silent press is a finding.

- ***The conformance test every addon ships*, step 8.** Rename it **"The launcher and the key binding"** and append:

  > Where the addon ships launcher-§6's binding, invoke its button's `OnClick` (the button the binding names) while disabled. Assert exactly one line matching *The refusal line*, zero SavedVariables writes and zero frame shows. Then write `enabled = true`, take the `perf` hold alone, and invoke it again. Assert exactly one `Not available during a performance capture.` line, no match on *The refusal line*, and no toggle.

### A4. `standards/standards/preview-mode.md`: the marker MUST, and the simulator

**Insert after the "MUST ship a test mode" bullet:**

> - **A test mode MUST say so on the display (v2.86.0).** While test mode is on, every display drawing placeholder data **MUST** carry a visible **text** marker that it is showing test data. The marker:
>   - is readable without hovering;
>   - is localized (localization);
>   - is visible in **every layout in which the placeholder data is visible**, including a hidden header, a compact layout and a collapsed title bar.
>
>   The measured failure: a meter window's `TEST MODE` title text disappeared with its header while the sample bars stayed (Multi Meters, header turned off). The marker's form is the addon's choice: a title badge, inline title text, or a strip. For a standalone window with a filter bar, standalone-windows names the recommended form.
>
>   What is not a marker:
>   - The launcher tooltip's `Test mode: On` and the Master-controls checkbox, because neither is on the display.
>   - Placeholder data that only looks plausible. Placeholder data whose visible text itself names the test (a group popup titled *Test Group*) **is** a marker.
>
>   Under the exception above, where unlocking is the preview, the unlocked display's drag handle (`LibKa0s-Widgets-1.0`'s `DragHandle`, a labeled strip, or the host's equivalent label) is the marker, and nothing more is owed. Missing, hover-only or layout-hidden markers are **anti-pattern #97**.

**Append an unnumbered sub-heading at the end of the file:**

> ### The in-game simulator (MAY)
>
> An addon **MAY** ship an in-game simulator: a session that plays scripted events through its real engine so a player can watch it work without a group, an instance or a real loot event. Drop Watcher's `/dw sim` is the reference, and Loot History and Bank Ledger ship one from v2.86.0.
>
> An addon that ships one:
> - **MUST** build it on **`LibKa0s-Sim-1.0`** (LibKa0s v1.75.0). A private session, seam, timeline or step panel beside the major is anti-pattern #47.
> - **MUST** route every client read the simulation answers through its `NS.Compat` table (compat), because that table is what the seam wraps. The seam must be installed after the compat family loads. A read cached in a local before then answers live data during a session, silently.
> - **MUST** refuse to start:
>   - while the addon is stood down, with the line by hold (slash-commands-§7);
>   - while test mode is on;
>   - in combat, in an instance, or in a group.
>
>   The major computes the last three. The host supplies the first two through its descriptor.
> - **MUST NOT**:
>   - send anything: every outward member (chat, whisper, addon message, trade) is in the host's guarded set;
>   - act on a real player;
>   - write SavedVariables from a simulated event. A session log the host keeps in memory and drops at stop is not SavedVariables.
> - **MUST** leave the addon exactly as it was at stop. Every module the session touched registers its cleanup.
> - **MUST** mark the session while it runs, like test mode (the marker bullet above). The major's step panel on screen satisfies this.
>
> These are the host's contract. The library guarantees only the refusal it computes, and it never advertises the rest as enforced (the LibKa0s#54 record).

### A5. `standards/standards/standalone-windows.md`: a SHOULD naming `W.TestStrip`

**Insert after the "A wide action button keeps its label…" bullet:**

> - **A window with a filter bar marks test mode with the library's strip (SHOULD, v2.86.0).** A standalone window whose body sits under a filter bar **SHOULD** satisfy preview-mode's marker rule with `LibKa0s-Widgets-1.0`'s **`TestStrip`** (Widgets minor 13, LibKa0s v1.75.0). The strip:
>   - spans the window's full width between the filter bar and the body;
>   - carries the catalog's `info` mark and one line saying what test mode shows and what ends it, plus a tooltip;
>   - shifts the body by its own height while it shows, and folds to a compact height when the window is narrow.
>
>   A window with no filter bar keeps whatever marker satisfies preview-mode (a title badge, inline title text), and **MAY** use the strip too. Multi Meters does, because its header, and the marker in it, can be hidden.
>
>   Once an addon is on v1.75.0, a host-built copy of the strip is anti-pattern #47. Drop Watcher is the strip's origin, and Loot History, Bank Ledger and Multi Meters adopt it.

### A6. `standards/standards/anti-patterns.md`: #96 and #97 new, #92 and #95 amended

- **#92**, the sentence "…and over a function literal in a `for ... in` header;": add, after it,

  > and, worse, a **keyed** function literal in a multi-line `for`/`while` header table makes it **raise**, so the run measured nothing and the traceback was read as its footer (a **crashed** run, automated-tests-§3)

  Change "and treat a blind file as complexity not passing" to:

  > and treat a blind file **or a crashed run** as complexity not passing

- **#95**, the sentence beginning "The commonest case is one the host never wrote: the library draws `close`, `copy` and `clear`…": rewrite it to name the closed set from A11:

  > the library draws `close` (every `Core.MakeCloseButton` window), `copy` and `clear` (the debug console's title bar), `info` (an `Options` id list's help mark, and `Widgets.TestStrip`) and `confirm` (`Widgets.StepPanel`'s completed step, so the `Sim` panel too)

  Append the clause:

  > and, upstream, a library release that starts resolving a catalog name outside that closed set from a host's folder (library-stack-§7)

- **New #96:**

  > 96. **A Show window with no key binding, or a binding that is a second feature.** Any of these:
  >     - An addon whose `ADDONS.md` row lists *Show window* and ships no binding for it.
  >     - A binding whose button runs anything but the handler the launcher's `toggleWindow` calls.
  >     - A `<Binding>` element carrying Lua or calling a global function.
  >     - A secure template on a non-secure window's toggle.
  >     - A shipped `default` key.
  >     - A button registered for both click edges, so one press toggles twice.
  >     - A press that toggles, writes or stays silent while the addon is stood down, or that prints the disabled line under the `perf` hold alone.
  >     - A renamed button, which silently unbinds every player's key.
  >
  >     (`launcher-§6`, `layout-§1`, `slash-commands-§7`)

- **New #97:**

  > 97. **A test mode that does not say so.** Any of these:
  >     - Placeholder data drawn with no visible text marker, so sample names read as real ones.
  >     - A marker visible only on hover, or only in the launcher's tooltip or the Master-controls checkbox.
  >     - A marker a layout option hides while the sample data stays visible. Multi Meters with its header turned off is the measured case.
  >     - An unlocalized marker string.
  >     - A simulation session whose displays are unmarked.
  >
  >     (`preview-mode`, `standalone-windows`)

`STANDARDS.md` changes its range to `(#1–#97)`. `check-standard.sh`'s anti-patterns check enforces the 1..N numbering and the index range.

### A7. `standards/standards/documentation.md` §1: icon-set credits

- **Item 12** (line 95). Replace the opening clause "**`## Credits`** — **MAY**, and **only** for genuinely **external** credit…" with:

  > 12. **`## Credits`** — **MAY** for discretionary external credit (third-party artwork, a font, a sound pack, another author's work the addon builds on or ships), with **two exceptions for the LibKa0s icon sets the addon ships**. Which sets ship is decided by its `LibKa0s icons:` line after the prune (library-stack-§7, *The icon subset*):
  >     - **MUST, where any `gi:` icon ships (`all` included).** Credit Game-icons.net with: the set's name; the CC BY 3.0 license; a link to <https://game-icons.net>; the authors of the marks that ship (`Media.IconAuthor(name)` per icon, or the shipped `game-icons/AUTHORS.txt` in full for `all`); and a statement that the marks were modified (rasterized, background removed, recolored). CC BY 3.0 makes attribution a license condition, and an `AUTHORS.txt` inside `libs/` is not attribution a player sees.
  >     - **SHOULD, for each MIT set that ships:** Open Iconic (unprefixed names, by Waybury) and Phosphor (`ph:`, by Phosphor Icons), each named with its author, license and link. Their license files already ship beside the art, so this is a courtesy the collection extends uniformly, not a license condition. Every addon that wires the debug console ships Open Iconic's `close`, `copy` and `clear`.
  >
  >     Credit goes by **set**, and only for sets that actually ship after the prune. It is never credit to `LibKa0s` as a library (the inventory ban below; anti-pattern #58 unchanged). A set that stops shipping loses its credit line in the same commit that prunes it.

  Keep the rest of item 12: it is the last section, and it must not carry a library list.

- **Line 117.** Replace "and `## Credits` (12) is **MAY**, omitted entirely when there is nothing external to credit" with:

  > and `## Credits` (12) is **MAY**, omitted entirely when there is nothing external to credit, except that item 12 makes it **MUST** where a `gi:` icon ships and **SHOULD** where an MIT icon set ships

### A8. `standards/standards/automated-tests.md` §3: crashed runs and the hazard row

This closes WowAddonStandards#8, with the facts corrected. The issue proposed scope as the axis. The measurements show that the **line shape** decides, not the scope.

- **Hazard table** (line 155). Replace the one row with two:

  | Hazard | What `lizard` 1.24.0 does | A line that loses its function |
  |---|---|---|
  | a function literal in a `for`/`while` header's table, on one line or positional | it is not listed. Inside a function its body folds into the enclosing function's CCN, so it is counted, but not as a function, and parity flags the file | `for _, p in ipairs({ function() end }) do` |
  | a **keyed** function literal (`K = function … end`) in a `for`/`while` header's table constructor that **spans lines** | it **raises** (`TypeError`) and aborts the run. Nothing after it is measured, at file scope or inside a function (a **crashed** run, below) | `for name, fn in pairs({` ⏎ `  A = function() f() end,` ⏎ `}) do g(name, fn) end` |

  Under the table, add:

  > The second row is not a blind spot. The kit's sanitizer does not rewrite it, because renaming the header keyword would drop the loop's own decision point and under-count the enclosing function, which is the unsafe direction for a ceiling. The remedy for both rows is in the source: hoist the table to a named local. Ka0s Premade Groups Filter Extension's `RegionTags.lua` was the measured instance, hoisted in `10350bc`.

- **New bullet, after the parity bullet:**

  > - **MUST** treat a run in which `lizard` **raised**, or was stopped by the kit's bound, as complexity **not passing**. A crashed run is not a blind file:
  >   - **Blind:** `lizard` parsed the file and under-listed it. The remedy is a sanitizer rule or a hoist.
  >   - **Crashed:** `lizard` refused a file and measured nothing reliable.
  >
  >   Function rows stream before the traceback, so a crashed run's `complexity.txt` can hold some `@` rows. They are partial and in walk order, not a measurement.
  >
  >   From **LibKa0s test-kit revision 41 (LibKa0s v1.75.0)** the runner:
  >   1. keeps `lizard`'s stderr out of the footer parse, and accepts the footer only in its exact shape (a `Traceback` on stderr invalidates it even after a well-formed footer);
  >   2. records `suites.complexity.status` as **`fail`**;
  >   3. sets every CCN figure, the maximum included, to **0** in `manifest.json`, so no figure measured over part of the tree enters the trend (`RESULTS.md` and the console print them as `n/a (lizard raised)`);
  >   4. skips parity, which a crash would otherwise report as "blind in every file";
  >   5. before removing its shadow, retries each file singly with the same flags to **name** the file or files `lizard` raised on. The count goes in **`suites.complexity.crashedFiles`** (0 on a measured run; absent from a kit older than 41). The names go on the console and in `RESULTS.md`'s first watch-list line, **Not measured — lizard raised**.
  >
  >   A bounded stop (timeout or memory cap) is the same `fail`, named as the bound, with no per-file retry. An exit of 1 with a valid footer and an empty stderr is **not** a crash: `lizard` 1.24.0 exits 1 whenever it warns.

- ***The release gate*, first bullet.** After "**`blindFiles` at 0** — a sighted run, since a parity mismatch is itself a `fail`", add:

  > — and a run on which `lizard` did not raise (`crashedFiles` at 0 where the field exists), since a crashed run is a `fail` too

  This is a clarification of "complexity pass", **not** a new gate term. The release gate stays "complexity pass".

- **§4.** Where the watch list's **Not sighted** first line is described, add the parallel line, **Not measured — lizard raised**, naming the crashed files. Where the trend row is described, add that a crashed run's CCN cells read `n/a`.

### A9. `standards/standards/library-stack.md` §2: a LibCustomGlow-1.0 row

**Add to the optional-libs table:**

| Lib | When |
|---|---|
| LibCustomGlow-1.0 | any addon that draws a button, pixel, autocast or proc glow; listed in `## OptionalDeps`. Driven through `LibKa0s-Glow-1.0` (library-stack-§7), which resolves it at call time |

### A10. `standards/standards/library-stack.md` §3: no edit

The icon carve-out is already there.

### A11. `standards/standards/library-stack.md` §7: the bulk of the change

1. **The `__` clarification.** Insert directly after "**MUST** keep a **module's descriptor / API contract additive-only** within a major…". This is required before or with OptionsTabs minor 9.

   > - **A `__`-prefixed member is a library internal, not contract.** A member whose name begins with two underscores is the library's own:
   >   - an attach seam between a major's files (`lib.__AttachTabs`);
   >   - a minor probe its suites read (`__tabsMinor`);
   >   - a test seam.
   >
   >   The additive-only rule above binds the contract a consumer is entitled to call, and a `__` member is not part of it. It **MAY** be removed in a later minor once nothing in the payload, the library's suites, `tests/majors.lua` or the testkit reaches it. The file's minor moves, and the changelog names the removal. A consumer **MUST NOT** call a `__` member. The one place it **MAY** name one is a library-absent stub mirroring the live table for surface parity (`Kit.assertSurfaceParity` reads live keys only, so a stub left with a removed key stays green). Such a mirror of a removed member is dead and goes in the consumer's next re-vendor commit.
   >
   >   The testkit is not a LibStub major and this rule does not reach it. A kit member listed in a kit version document is the kit's contract to consumer suites, whatever its name: `M.__fireUnconditional` is what slash-commands-§7 step 6 is built on.
   >
   >   The first removal under this rule is `O.__releaseChrome` (OptionsTabs minor 9, LibKa0s v1.75.0, LibKa0s#45). It is no precedent for removing a public member.

2. **The module table.**
   - **`LibKa0s-Item-1.0` row.** Change "item identity as four primitives and no policy: id and quality from a link, the quality label, and the cache-then-callback load" to:

     > item identity as five primitives and no policy: id and quality from a link, the quality label, the cache-then-callback load, and, from **Item minor 3 (`LibKa0s v1.75.0`)**, `BonusIDsFromLink`, the ordered bonus ids an item link or bare item string carries (field 13 is the count; empty fields are kept). Everything else LibKa0s#51 nominated (link detail and the better-link merge, identity keys, the gear-level and bag-location reads, the quality fallback, the Wowhead URL, the loot-line parser) was rejected; the record is the Item API document's *What this major is not*.

   - **`LibKa0s-Widgets-1.0` row.**
     - Change the Files cell to: `Widgets.lua`, `WidgetsReorder.lua`, `WidgetsDragHandle.lua`, `WidgetsLineChart.lua`, `WidgetsAutocomplete.lua`, `WidgetsStepPanel.lua`.
     - Before the closing clause, insert:

       > From **Widgets minor 13 (`LibKa0s v1.75.0`)** `Widgets.lua` also carries:
       > - **`SearchBox`**: the flat filter-bar search box in the dropdown's own skin, with a hint shown while it is empty, Escape and Enter clearing focus, and a gold focus line. Text handling stays the host's. Promoted with three consumers: Loot History, Bank Ledger, Drop Watcher.
       > - **`TestStrip`**: the test-mode strip standalone-windows recommends for a window with a filter bar. Promoted with four consumers: Drop Watcher, Loot History, Bank Ledger, Multi Meters.
       >
       > From **WidgetsStepPanel minor 1 (`LibKa0s v1.75.0`)**, in the sixth file, **`StepPanel`**: the host-driven clickable step panel `LibKa0s-Sim-1.0` draws its session with[, and `LibKa0s-Perf-1.0`'s guided panel is built on].
     - Rewrite the closing clause "and `Widgets.lua` stays at minor 12" (the c52 MISS) as:

       > Each secondary file is paired on the shell's minor as `WidgetsDragHandle.lua` is

     - The flat checkbox and an exported flat skin were rejected in LibKa0s#52.

   - **New row, `LibKa0s-Glow-1.0` | `Glow.lua`:**

     > A **stateless** driver for LibCustomGlow-1.0. It starts and stops one of LCG's four styles (button, pixel, autocast, proc) on a frame under a caller key, from a style name and knob values. It maps the knobs onto LCG's positional arguments with the two traps handled once (a `pixelLength` of 0 becomes nil; `pixelBorder` is coerced to a boolean), and passes nil through so LCG's own defaults apply. LibCustomGlow-1.0 is **soft-resolved at call time** and the major declares no floor on it: a consumer vendors LCG itself (library-stack-§2), so there is nothing to floor on, the same reasoning as `Bus` and AceEvent. With LCG absent, a start does nothing. The major owns **no state**: no lifecycle, no unchanged-repaint no-op, no defaults, no knob catalog, and no options composer. Those stay the host's (rejected in LibKa0s#56). **Ships from `LibKa0s v1.75.0`** (Glow minor 1). Consumers: Drop Watcher, Quick Comms, KickCD.

   - **New row, `LibKa0s-Sim-1.0` | `Sim.lua`:**

     > The in-game simulator's host-neutral core (preview-mode, *The in-game simulator*):
     > - the session, and the refusal the library can compute (combat, instance, group) beside the host's own;
     > - the answer seam over a host's `NS.Compat` members, with guarded members never reaching the client;
     > - the scripted timeline (step, run, pause, resume, restart, run-to) delivering events into the host's dispatch;
     > - the session panel, drawn with `Widgets.StepPanel`.
     >
     > What a simulation *means* stays the host's, declared in its descriptor: the scenarios, the guarded members, where a session's writes go, and what stop cleans. **Ships from `LibKa0s v1.75.0`** (Sim minor 1). Consumers: Drop Watcher (migrated, its generic copy deleted), Loot History, Bank Ledger.

   - **`LibKa0s-Perf-1.0` row.** Only if PerfPanel is rebuilt, add:

     > from PerfPanel minor N (`LibKa0s v1.75.0`) the guided panel is drawn with `Widgets.StepPanel`, with an unchanged look, which adds the edge in item 4

3. **The counts paragraph** ("**The modules.**"). Change "**fifteen LibStub majors across thirty-four files**" to "**seventeen LibStub majors across thirty-nine files**". Insert `Glow` and `Sim` into the major list in `tests/majors.lua` order. Correct "`Options` spans ten files" to **eleven** (`OptionsDrawer.lua`, v1.73.0, was never counted). Add "`Media` two" (`MediaIcons.lua`, v1.74.0). Change "`Widgets` five" to **six**. Append the dated recount sentence:

   > **`LibKa0s v1.73.0`** adds `OptionsDrawer.lua` and **`v1.74.0`** adds `MediaIcons.lua`, neither counted here until now: the two commands answered **15 and 36** at `v1.74.0`. **`LibKa0s v1.75.0`** adds two majors, `Glow` and `Sim`, and three files, `WidgetsStepPanel.lua`, `Glow.lua` and `Sim.lua`. Each is added to `tests/majors.lua` and `LibKa0s.xml` in the same change, so the two commands, re-run at the v1.75.0 tag, answer **17 and 39**.

   *(Recount with `grep -c 'major = "LibKa0s-' tests/majors.lua` and `grep -c '<Script file=' LibKa0s/LibKa0s.xml` at the release commit, and write the numbers measured.)*

4. **Inter-module dependencies.** Recount with `grep -n 'NEEDS_' LibKa0s/*.lua` at the tag.
   - "**Fourteen of the fifteen majors**" becomes "**Sixteen of the seventeen**".
   - "**ten of those fourteen** gate on it without calling a single member" becomes **eleven** or **twelve**, depending on whether `Sim` reads a Core member. Add `Glow` to the list, and `Sim` if applicable.
   - "There are exactly three second edges" becomes **four** (or five):
     - `LibKa0s-Sim-1.0` floors on `LibKa0s-Widgets-1.0`, whose `StepPanel` draws its panel.
     - If PerfPanel is rebuilt: `LibKa0s-Perf-1.0` also floors on Widgets, declared in `PerfPanel.lua`. This is a re-vendor trigger only for a host whose `libs/` is otherwise mixed, and the changelog must call it out (the "Raising a floor" bullet).
   - Append:

     > `LibKa0s-Glow-1.0` resolves `LibCustomGlow-1.0` at call time and declares no floor on it, which is not an edge, as `Bus` and AceEvent are not.

   - Ship-payload bullet (line 108) and anti-pattern #48: "fourteen of the fifteen majors refuse to register without Core" becomes "sixteen of the seventeen".

5. **Adoption of the new majors.** Insert after the paragraph "**The three majors that ship from `LibKa0s v1.55.0`…**":

   > **`Glow` and `Sim`, from `LibKa0s v1.75.0`, are adopted by their named consumers at their v1.75.0 re-vendor.**
   > - An addon that drives LibCustomGlow-1.0 **MUST** do it through `LibKa0s-Glow-1.0` once it carries v1.75.0. A host start/stop table beside the major is anti-pattern #47.
   > - An addon that ships a simulator **MUST** build it on `LibKa0s-Sim-1.0` (preview-mode).
   > - `SearchBox`, `TestStrip`, `StepPanel` and `Item.BonusIDsFromLink` need no sentence of their own: once an addon carries v1.75.0, a hand-built copy of any of them is #47 as written.

6. **The icon subset, *The icons the library draws for you are yours to declare*.**
   - Rewrite "At `LibKa0s v1.74.0` those are…" as:

     > At `LibKa0s v1.75.0` those are:
     > - `close`: `Core.MakeCloseButton` with an `addonName`, so every Ka0s window's close control, the debug console's and the perf panel's among them.
     > - `copy` and `clear`: the debug console's title bar (debug-logging-§13).
     > - `info`: an `Options` id list's default help mark when the host supplies no `helpIcon`, and `Widgets.TestStrip`'s mark.
     > - `confirm`: `Widgets.StepPanel`'s completed-step tick, so every `Sim` session panel.

   - Change "therefore declares at least `close, copy, clear`" to:

     > therefore declares at least `close, copy, clear`, plus `info` where it builds a `TestStrip` or an id list without a `helpIcon`, and `confirm` where it runs a `Sim` session

   - Then add a new bullet:

     > - **The library-drawn set is closed (MUST).** The five names above are every catalog name the library resolves from a host's folder, and a later library release **MUST NOT** resolve a further one, on any surface. LibStub serves the newest copy of each file to every host. A name a newer `DebugLog`, `Core`, `Widgets` or `OptionsIdList` started drawing would be drawn into the folder of a host still pruned at an older tag, where the file is absent: blank, silent, and invisible to that host's gate. New library chrome takes its art **from the host** instead, as a resolved path or texture argument (the `helpIcon` pattern). Adding a name to the set is a standard change first and a major-version decision for the drawing major.
     >
     > The set closes at v1.75.0, the first tag at which any consumer prunes, which is why v1.75.0's own additions (`info` on `TestStrip`, `confirm` on `StepPanel`) are safe: no host was pruned at an older tag. A surface rebuilt on a set member keeps the declaration burden it had. If Perf's panel draws the `confirm` tick, every Perf host owes `confirm`, so its rebuild keeps its color-texture dots instead.

   - In ***The runtime is unchanged…***, change "**A pruned copy cannot break another addon.**" to:

     > **A pruned copy cannot break another addon** through a name the **host** passes, since `Icon` builds the path from the caller's folder. For names the **library** resolves, the closed set above is what keeps that true.

   - In ***Attribution travels with its set (MUST)***, append:

     > The README half, crediting the sets that ship, is documentation-§1 item 12: a **MUST** for Game-icons, a **SHOULD** for the MIT sets.

7. ***What earns promotion*.** After the SHOULD-record-rejections bullet, append:

   > The rejections of the 2026-10-22 batch (LibKa0s#49–#58) are indexed in open-evolutions, *Further `LibKa0s` modules*, each with the bar it failed and its re-check trigger. The full record of each is the issue's closing comment, or the API document of the major it would have joined.

### A12. `standards/standards/open-evolutions.md`

- ***Further `LibKa0s` modules*** (line 13).
  - Change "**fifteen majors across thirty-four files** (recounted at `LibKa0s v1.70.0` …)" to "**seventeen majors across thirty-nine files** (recounted at `LibKa0s v1.75.0` …)".
  - In "Shipped so far", add:
    > the flat search box, test-mode strip and step panel (Widgets, v1.75.0), the bonus ids of a link (Item), the stateless LibCustomGlow driver (Glow) and the in-game simulator's core (Sim)
  - Append a new bullet, **"Recorded rejections, LibKa0s#49–#58 (2026-10-22)"**, with one line per rejection naming the bar it failed and its trigger. No API sketch for any of them, so no next nomination is anchored to it:
    - **#49 chat sender** (`Compat.ChatSender`). No content: on every admitted client the fallback rung is unreachable.
    - **#49 tooltip line reader / duration decoder.** One consumer.
    - **#49 restriction tracker.** Bar 3: a same-author copy under ten days old, with the two copies' edges already diverged.
    - **#49 the four restriction readers.** These are guards, so promotion removes no host line. Re-check when a non-copy addon needs Drop Watcher's absent and secret answers **and** Multi Meters' and Consumable Master's readers reconcile with them.
    - **#49 / #51 loot-line parser.** The consumers disagree on correctness (crafting and refund lines).
    - **#50 mixed grid composer.** One consumer, and the issue's premise is gone.
    - **#51 the other item reads.** Single consumer, or disagreeing semantics, or a simulator bypass.
    - **#52 flat checkbox.** No consumer.
    - **#52 exported flat skin.** High frequency, low content, and themes disagree.
    - **#56 IconStyle.** Every consumer means something different.
    - **#56 glow lifecycle.** Disagreeing no-op policies, and it writes LCG private state.
    - **#56 glow catalog defaults.** Profile-owned, and the hosts disagree.
    - **#56 `GlowGroup` composer.** No canonical glow block in options-ui.
    - **#56 LSM `Solid` registration.** One line, four sites.
    - **#58 key-binding helper.** See launcher-§6.
    - **#47's lizard detector and sanitizer rewrite.** Zero instances; the rewrite under-counts CCN.
    - **#55 picker-credit helper.** `all` is reserved to one addon.
- ***A per-addon adoption command*.** "fifteen majors" becomes "seventeen majors".
- **Line 155.** "Ten of the fifteen" becomes the recounted "Eleven (or twelve) of the seventeen".

### A13. `standards/standards/compat.md`: one sentence (confirm against the Sim seam design)

Append to ***The applicability condition***:

> An addon that ships an in-game simulator (preview-mode) also routes through its compat family every client read the simulation answers, deprecated or not, because that table is what `LibKa0s-Sim-1.0`'s seam wraps. Such a read is a family member like any other, and the addon is never exempt from the family on this condition.

Loot History and Bank Ledger already have a `core/Compat.lua`, and Drop Watcher already routes this way.

### A14. `standards/ADDONS.md`

After "**The launcher column is normative input to an audit…**", add:

> **Show window** also means the addon owes launcher-§6's key binding: a `CLICK` binding in a root `Bindings.xml` on the same toggle handler. The audit reads this column for that too. No new column.

### A15. `standards/STANDARDS.md`

- **Title:** `# Ka0s WoW Addon Standard (v2.86.0, <landing date>)`.
- **Sections blurbs:**
  - **launcher:** append "; and the **Show window key binding** (§6) every addon with a primary window ships — a `CLICK` binding in a root `Bindings.xml` on a plain hidden named button that calls the `toggleWindow` handler, no default key, a permanent button name, and a press that refuses by hold while stood down".
  - **preview-mode:** "placeholder-data preview/test mode for positionable displays; a test mode **says so on the display**, in every layout where the sample data shows; and the optional **in-game simulator**, built on `LibKa0s-Sim-1.0`, with its refusals and its no-send, no-SavedVariables contract".
  - **standalone-windows:** append "; and `Widgets.TestStrip` as the test-mode marker of a window with a filter bar".
  - **slash-commands:** add "a key binding's press refuses by hold".
  - **layout:** add "`Bindings.xml` owed by every Show window addon".
  - **library-stack:**
    - "fifteen majors across thirty-four files" becomes "seventeen majors across thirty-nine files".
    - Add "`LibCustomGlow-1.0` as an optional lib driven through `LibKa0s-Glow-1.0`".
    - Add "a `__` member is an internal, removable in a later minor".
    - Add "the library-drawn icon names closed at `close`, `copy`, `clear`, `info`, `confirm`".
  - **automated-tests:** add "a **crashed** run — `lizard` raised or bounded — is complexity not passing, its figures zeroed and its file named (`crashedFiles`, kit revision 41)".
  - **documentation:** add "the README credits the LibKa0s icon sets it ships — **MUST** for Game-icons (CC BY 3.0), **SHOULD** for the MIT sets".
  - **anti-patterns:** `(#1–#97)`.
- **Changelog.** Move the v2.85.0 entry **verbatim** to the top of `standards/CHANGELOG.md`, then write the new current entry in STANDARDS.md. A draft in the house shape:

  > **v2.86.0 (<date>):** **Six rulings from the LibKa0s #45–#58 run.**
  >
  > **(1) launcher-§6 (MUST).** An addon with a Show window entry ships one `CLICK` key binding on a plain, hidden, named button that calls the `toggleWindow` handler. It refuses by hold while stood down (slash-commands-§7: the disabled line, or the perf line, never the disabled line under `perf` alone), ships no default key, and keeps its button name permanent. Quick Comms is the reference. layout-§1's `Bindings.xml` paragraph is generalized. A library helper was rejected (LibKa0s#58). Anti-pattern #96.
  >
  > **(2) preview-mode (MUST).** A test mode carries a visible, localized text marker in every layout where its sample data shows; Multi Meters' header-off case is the measured failure. standalone-windows **SHOULD** use `Widgets.TestStrip` for a window with a filter bar. A new MAY sub-section covers the in-game simulator on `LibKa0s-Sim-1.0`, and compat gains its one sentence. Anti-pattern #97.
  >
  > **(3) documentation-§1 item 12.** Game-icons credit is a **MUST** wherever a `gi:` icon ships (CC BY 3.0). The MIT sets are a **SHOULD**. Credit is by set and only for the sets shipped.
  >
  > **(4) automated-tests-§3, a clarification.** A run in which `lizard` raised or was bounded is complexity not passing. From kit revision 41 its figures are zeroed, `crashedFiles` names the file and parity is skipped. The hazard row is split, and the axis is the line's shape, not its scope (closes WowAddonStandards#8).
  >
  > **(5) library-stack.**
  > - §2 gains a LibCustomGlow-1.0 row.
  > - §7: `__` members are internals (first removal: `O.__releaseChrome`, OptionsTabs minor 9).
  > - §7: the library-drawn icon set is closed at `close`, `copy`, `clear`, `info`, `confirm`.
  > - §7: the module table gains `LibKa0s-Glow-1.0`, `LibKa0s-Sim-1.0`, `SearchBox`, `TestStrip`, `StepPanel` and `Item.BonusIDsFromLink`, recounted at 17 majors across 39 files (the 34 had been stale since v1.73.0).
  >
  > **(6) open-evolutions.** Indexes the rejections, each with its re-check trigger.
  >
  > Version rippled to `CLAUDE.md`, `README.md`, `EXECUTIVE_SUMMARY.md` and `NEW_ADDON_CONTEXT.md`.
  >
  > **Who is affected.**
  > - Bank Ledger, Drop Watcher, Loot History, Multi Meters and WhatGroup owe the binding at their next release.
  > - Every addon with a test mode is re-checked for its marker.
  > - Consumable Master, Panel Master, Party Frame Enhanced, Pretty Chat and WhatGroup add the Open Iconic credit (SHOULD).
  > - Every consumer adopts the closed-set declaration at its v1.75.0 re-vendor.
  >
  > Minor.

### A16. `standards/EXECUTIVE_SUMMARY.md`

- Line 11 stamp: `current: **v2.86.0**, <date>`. check-standard's `version-stamps` greps exactly this.
- Line 23, "One launcher, one identity": append "; an addon with a primary window also ships a **Show window key binding** on the same toggle handler, refusing while disabled (launcher-§6)".
- Line 57: "seventeen LibStub majors across thirty-nine files (Core, Env, Compat, Lifecycle, Bus, Schema, Pool, Item, Media, Widgets, DebugLog, Slash, Launcher, Options, Perf, Glow, Sim)", in `tests/majors.lua` order.
- In the numbered list item that covers preview and test mode (or the options-ui item), add one sentence: "a test mode **says so on the display**, in every layout (preview-mode, #97)".
- Item 7 (automated tests): add "a **crashed** `lizard` run is not a pass".

### A17. `standards/NEW_ADDON_CONTEXT.md` (pack version line 1 → v2.86.0)

- Starter tree, line 108: the same `Bindings.xml` wording as A2.
- **Launcher snippet section.** Add a `Bindings.xml` plus button snippet for an addon with a primary window, modeled on `QuickComms/settings/SlashVerbs.lua` (the `V.TOGGLE_BUTTON` block) and `QuickComms/Bindings.xml`'s last line. It routes the click through the toggle handler and the refusal helper, and carries no `default`.
- Item 18 (preview-mode): add the marker rule. Item 18a (launcher): add the binding.
- Don'ts list, near line 1614: extend the lizard line with "or a crashed run read as a pass".
- Checklist:
  - Add "- [ ] Show window key binding (launcher-§6) if the addon has a primary window".
  - Extend line 1680 with "with a visible test marker in every layout".
  - Add "- [ ] `## Credits` names each LibKa0s icon set shipped (documentation-§1 item 12)".
- Lines 57, 1402 and 1421: the declaration template and prose name the closed set. A new addon's minimum stays `close, copy, clear`, plus `info` or `confirm` per the surfaces it wires.

### A18. `NEW_ADDON.md`

- Lines 217–244, the launcher step: add "and, where the addon has a primary window, the Show window key binding (launcher-§6): a root `Bindings.xml` `CLICK` line and the button, from the context pack".
- Line 310: replace "`## Credits` is optional and carries **only external** credit" with "`## Credits` carries only external credit, and **must** credit Game-icons (and **should** credit each MIT icon set) the addon's `LibKa0s icons:` line ships (documentation-§1 item 12)".
- Line 366: "`blindFiles` at 0" becomes "`blindFiles` at 0 and a run on which `lizard` did not raise".

### A19. `AUDIT.md`

- **Lines 88–96 (README):** add "and, where the addon's `LibKa0s icons:` line ships a `gi:` icon, a `## Credits` crediting Game-icons per documentation-§1 item 12 (missing: MUST finding); each shipped MIT set named (missing: SHOULD finding); no credit for a set the prune removed".
- **Line 281 (`Bindings.xml`):** generalize "(a `CLICK` binding carries none)" to "(a `CLICK` binding, on a secure or a plain named button, carries none)".
- **Line 496 (icon subset):** add "the declaration includes the library-drawn names the addon's wired surfaces use: `close, copy, clear` with the debug console; `info` with a `TestStrip` or an id list without `helpIcon`; `confirm` with a `Sim` session. The library-drawn set is closed (library-stack-§7)".
- **Launcher check (575–635): new sub-bullet**, "**The Show window key binding** (`launcher-§6`, new in v2.86.0)":
  > For a row whose `ADDONS.md` column lists *Show window*, check:
  > 1. A root `Bindings.xml` holds a `CLICK <button>:LeftButton` line, with no `default` attribute and no Lua.
  > 2. The button is created in a module as a plain `Button`, not secure, registered `AnyDown`, and its `OnClick` reaches the same function the descriptor's `toggleWindow` calls. Grep both and compare; a copy of the body is #81 and #96.
  > 3. `BINDING_HEADER_<FOLDERUPPER>` and the `BINDING_NAME_…` label are assigned in a module, the label through `L`.
  > 4. The press refuses by hold (read the handler or the helper it calls).
  > 5. `tests/test_disabled.lua` step 8 covers the press.
  >
  > Missing binding: a MUST finding from the addon's first release after v2.86.0.
- **Line 682 (the disabled-surface census):** add "- **The key binding.** A press that toggles, writes or is silent while stood down, or prints the disabled line under the `perf` hold alone (`launcher-§6`, `slash-commands-§7`)."
- **Line 708, step 8:** add "and, where launcher-§6's binding ships, the button's `OnClick` while disabled (one refusal line, zero writes and shows) and under the `perf` hold alone (the perf line)".
- **Line 884 (test mode):** add a paragraph:
  > **Then check the marker** (`preview-mode`, v2.86.0). With test mode on, every display drawing sample data shows a visible, localized text marker, and it stays visible in every layout option the display offers: header off, compact, collapsed. Read the code path that hides the header or title and confirm the marker does not ride it. Under the unlock-preview exception the drag handle's label is the marker. A filter-bar window not using `Widgets.TestStrip` on v1.75.0+ is a SHOULD finding (standalone-windows). A missing or layout-hidden marker is #97. Behavior is confirmed by the owner's in-client smoke, never by the auditor.
- **Line 1175 (complexity):** add "and, on kit 41 or later, `suites.complexity.crashedFiles` is **0** (above 0, `lizard` raised; complexity did not pass, and the watch list's first line names the file)".
- **LibKa0s adoption checks:**
  - An addon on v1.75.0+ that drives LibCustomGlow-1.0 with its own start/stop table, or runs a simulator not on `LibKa0s-Sim-1.0`, is #47.
  - A consumer call to a `__` member outside a parity stub is a finding (library-stack-§7).

### A20. `AUTOMATED_TESTS.md`

- Line 96, the table: add a row `| Crashed files (lizard raised) | |` under "Blind files (parity mismatch)".
- After line 104, add a paragraph:
  > **A `crashedFiles` above 0 is complexity not passing.** `lizard` raised on the files named, so the run's CCN figures are 0 in the manifest and `n/a` in the row. Partial `@` rows in `complexity.txt` that stream before the traceback are not a measurement. The usual fix is to hoist a keyed function literal out of a multi-line `for`/`while` header table. A manifest without the field came from a kit older than 41, where a crash read as "blind in every file".
- Line 276: add a bullet, "`crashedFiles`, and every file named, when it is above 0: complexity did not pass".

### A21. Version strings

- `README.md:173`: "The standard is at **v2.86.0**".
- `CLAUDE.md:172`: "As of v2.86.0 the sets are:". The doc sets themselves are unchanged, so only the stamp moves.
- `standards/NEW_ADDON_CONTEXT.md:1`: as in A17.
- `docs/ARCHITECTURE.md`: no version stamp to move. Check with grep.

### A22. Gate (WowAddonStandards CLAUDE.md)

- **`bash scripts/check-standard.sh` must exit 0.** It checks:
  - `cr-bytes`;
  - `gitattributes`;
  - `citations`: every new `launcher-§6` must hit a real `### 6.` heading, and no `preview-mode-§N` or `standalone-windows-§N` may appear;
  - `sections`;
  - `anti-patterns`: 1..97 and the index `(#1–#97)`;
  - `version-stamps`: STANDARDS title, README Status, the EXECUTIVE_SUMMARY `current:` line, NEW_ADDON_CONTEXT line 1, and CLAUDE.md's "As of";
  - `links`.
- **No script change is needed.** None of the new rules is mechanically decidable by the script's existing checks beyond those, so the script and DEPENDENCIES.md stay as they are.
- **Read the documents for meaning as well:**
  - launcher-§6 against slash-commands-§7, *Which refusal, by hold*;
  - preview-mode's marker against options-ui-§15's test-mode row;
  - library-stack-§7's counts against `LibKa0s@<v1.75.0>`.
- **Check line endings:** `tr -dc '\r' < <file> | wc -c` → 0.
- **Commit per item id**, for example `STD-01: launcher-§6 …`, ending with the session trailers.

---

## B. dev-copilot 2.4.0: ordered edit list

The repo checkout is byte-identical to the installed 2.3.5. Nothing in `commands/`, `profiles/` or `agents/` mentions the `LibKa0s icons:` line, the prune, or crashed runs today.

### B1. `commands/wow-revendor-libka0s.md` (the main change)

1. **Front matter `description`.** After "rolls the CLAUDE.md provenance line in the same commit", add:

   > writes or keeps the `LibKa0s icons:` declaration directly under it, prunes `media/icons/` to it with the tag's own `tools/prune-icons.lua`, and keeps the README's icon-set credits in step

2. **Step 2, the extract.** Change it to:

   ```sh
   git -C ../LibKa0s archive <tag> LibKa0s testkit tools | tar -x -C <scratch>/
   ```

   Add:

   > `tools/` is extracted only for `prune-icons.lua`, which `dofile`s `../testkit/vendor_sync.lua` beside it, so the tool and the gate share one parser at the same tag. It is never copied into the addon. A tag older than v1.75.0 carries no `prune-icons.lua` and no declaration-aware kit: skip the prune and the declaration, and say so.

3. **Step 3d, reading the diffs.** Add a fourth reading:

   > - **`Only in <scratch>/LibKa0s/media/icons…`** → in a consumer whose `CLAUDE.md` carries a `LibKa0s icons:` line, these are the icons it did not declare. That is the declaration working, not a fork and not #48. Compare against the declaration with the same parser. Only a declared icon that is missing, or an `Only in <Addon>/…/media/icons` line, is drift.

4. **New Step 3i, "The icon declaration → `01_DELTA.md`".** Before the copy:
   - **Read the declaration.** Run `grep -n 'LibKa0s icons:' CLAUDE.md`. The line must be the **next non-blank line** after the provenance line (`testkit/vendor_sync.lua` `iconDeclaration`).
   - **Provenance line run into prose is a blocker.** If the provenance line continues into prose on the same line, or the next non-blank line is prose, split it so the declaration can sit directly under it. The survey measured this at Loot History `CLAUDE.md:56` and Panel Master `CLAUDE.md:50`. The split is fixed in Step 4's commit.
   - **No line yet: derive one, and never from `Media.Icon(` greps alone.** Those find nothing in a roster addon (c55_57 C3). Read:
     - (a) every call of the addon's media seam (`NS.Icon(`, `KCM.Icon(`, `NS.IconMarkup(`);
     - (b) data tables and constants that feed it (`icon =`, `art =`, `HANDLE_ICON`);
     - (c) the **library-drawn** names for the surfaces it wires, taken from the tag's own `docs/releasing.md` table and changelog re-vendor notes, never from this spec. At v1.75.0 those are `close, copy, clear` with the debug console, `info` with a `TestStrip` or an id list without `helpIcon`, and `confirm` with a `Sim` session.
   - **`all` only** when the addon's UI lets the player choose among the catalog, with the parenthesized chooser (`all (icon browser).` for Quick Comms).
   - **Show the proposed line with `file:line` evidence per name, and confirm with the user before the copy.** Hand-maintained lists have already drifted (KickCD `tests/test_mediasetup.lua:28`, WhatGroup `:19`), so state that the owner's in-client smoke is the backstop.

5. **New Step 3j, "Tests that assume the whole icon folder" (a blocker class).**
   - Run `grep -rn "media/icons\|lib.ICONS\|\.ICONS)" tests --include='*.lua' | grep -v '/_kit/'`.
   - A suite that opens a file for **every** catalog name (AbsorbTracker `tests/test_mediasetup.lua:111-121`) goes red after the prune. So does one that asserts an icon file the addon no longer declares (AbsorbTracker `tests/test_optionssetup.lua:538-546`).
   - Fix both in Step 4's commit: delete the whole-catalog file loop, which the kit gate already enforces as declared == shipped, and narrow file assertions to declared names.
   - Do not write a second declaration parser in the addon.

6. **Step 4, "The copy".** Replace the sequence with:

   ```sh
   cp -r <scratch>/LibKa0s/.  <Addon>/libs/LibKa0s/
   cp -r <scratch>/testkit/.  <Addon>/tests/_kit/
   # both diffs, both directions: content MUST be empty against the WHOLE copy (before the prune)
   # roll the provenance line AND write/keep the `LibKa0s icons:` line directly under it (3i)
   lua <scratch>/tools/prune-icons.lua <Addon>     # prints every path it removes; refuses unknown names and removes nothing
   ```

   - Add: "**A refusal from the prune stops the run.** It means a typo, a name the tag does not carry, or an earlier prune. Re-copy the folder and correct the line. Never hand-delete icons."
   - **In *The provenance line*:** add "**and the declaration under it.** Write or keep `LibKa0s icons: …` as the next non-blank line. If the existing provenance sentence runs on into prose, split it (3i). The kit gate reads only the next non-blank line."
   - **New sub-step, "Credits":**
     > Read which icon sets ship after the prune (unprefixed → Open Iconic, `ph:` → Phosphor, `gi:` → Game-icons). Make `README.md`'s `## Credits` agree, per documentation-§1 item 12:
     > - add Game-icons with CC BY 3.0, the link, the authors from `Media.IconAuthor` (or `AUTHORS.txt` for `all`) and the modification note (MUST);
     > - add each shipped MIT set (SHOULD);
     > - remove the credit line of a set the prune removed.
     >
     > Credit sets, never "LibKa0s". This is the one README edit this command makes beyond removing a superseded provenance line. Announce it.
   - **Gate:** unchanged.
   - **The commit** now carries: both payloads after the prune, both `CLAUDE.md` lines, the provenance split if needed, the Step 3g and 3j blockers, and the credits. Keep it one commit: the consumer's `test_vendor_sync.lua` fails a split.
   - **Remove dead stub mirrors.** Add: "A library-absent stub that mirrors a `__` member the tag removed (for example `__releaseChrome` at v1.75.0, in seven addons' `settings/OptionsSetup.lua`) is dead. Remove it in the same commit (library-stack-§7)."

7. **Step 5, candidates.** Add one line:
   > The owner may pre-decide adoptions in a cross-repo run (a bundle's `items.tsv`). When a candidate is already decided there, record it as decided and do not re-interview.

8. **Step 8 summary.** Add: the declaration line written or kept, the prune's removed count by set, any provenance split, and the credit lines changed.

### B2. `agents/wow-standards-audit.md`, around lines 420–423

- Change "**For `LibKa0s` that is two diffs, both of which MUST be empty**" to:

  > two diffs, both of which MUST be empty **outside `libs/LibKa0s/media/icons/`**. Inside it, read the `LibKa0s icons:` line: `Only in <LibKa0sRepo>/…/media/icons` lines for undeclared icons are the declaration working, while a missing declared icon, a `differ` line or an `Only in <Addon>/…` line is drift (library-stack-§7, *The icon subset*; anti-pattern #95)

- Today's wording would file every pruned consumer as #45 and #48.
- Add to the provenance greps: `grep -n -A3 'Bundles \[LibKa0s\]' CLAUDE.md`. The next non-blank line must be the declaration.

### B3. `profiles/wow/sync-docs.md`

- **`claude-rewrite`, line 210.** Append:

  > The `LibKa0s icons:` line sits directly under the provenance line, as the next non-blank line, and moves with it. Never insert prose between them, and never join the provenance line to a following sentence (`vendor_sync.lua` reads only the next non-blank line). Do not edit the declaration's names: `wow-revendor-libka0s` owns them.

- **Line 201.** Append:

  > **Icon-set credits are external credit and stay:** documentation-§1 item 12 requires Game-icons and recommends each MIT set the declaration ships. Report a set credited but not shipped, or shipped but uncredited, as drift.

### B4. `commands/wow-new-addon.md`

- **Line 242.** Replace the Credits bullet with:
  > `## Credits` is external-only, and **must** credit Game-icons (and **should** credit each MIT icon set) the addon's `LibKa0s icons:` line ships (documentation-§1 item 12).
- **Line 244 (step 6a).** Add:
  > and, on the next non-blank line, the `LibKa0s icons:` declaration matching the prune (`close, copy, clear` plus what the scaffold draws)
- **Launcher step.** Add one sentence pointing at the playbook's launcher-§6 step: a primary-window addon is scaffolded with `Bindings.xml` and its button. The substance stays in `NEW_ADDON.md` and the pack; this command restates nothing beyond that pointer.

### B5. `profiles/wow/bump-version.md`

- **Gate table, line 64.** Change the Sighted row to:

  | Gate | Condition |
  |---|---|
  | Sighted | `suites.complexity.blindFiles == 0` and, where present, `suites.complexity.crashedFiles == 0` (`lizard` saw every function and did not raise) |

- Add after line 73:
  > A **crashed** run (kit revision 41+) already has `suites.complexity.status == "fail"`, so the Complexity row refuses too. Print `crashedFiles` with the file names from the watch list's **Not measured — lizard raised** line. The CCN row reads 0 by construction on that run, so mark it NOT EVALUATED, not PASS. A manifest without `crashedFiles` predates kit 41: print `crashedFiles —`.
- Line 104, the sample table: `Sighted | PASS | blindFiles 0, crashedFiles 0`. Line 347: same.

### B6. `commands/wow-automated-tests.md`

- **Line 127.** Add a bullet:
  > **A `crashedFiles` above 0 is complexity not passing.** `lizard` raised on the files named. The run's CCN figures are zeroed in the manifest and `n/a` in `RESULTS.md`, and any `@` rows before the traceback in `complexity.txt` are partial, never a measurement. Name every file, and the known `lizard` 1.24.0 trigger: a keyed function literal in a multi-line `for`/`while` header table, fixed by hoisting it to a local. A manifest without the field came from a kit older than 41, where a crash read as "blind in every file".
- **Line 187.** Add the parallel bullet for the summary.

### B7. `profiles/wow/agent-review.md`, line 177

Append:

> A **crashed** run (`crashedFiles` above 0, kit 41+) is complexity not passing too. Report the file `lizard` raised on and the hoist, and do not read the zeroed figures as a measurement.

### B8. Version ripple (dev-copilot CLAUDE.md, *Adding/removing a command…*; no command is added)

- `.claude-plugin/plugin.json`: `"version": "2.4.0"`. It is the single source of truth. `marketplace.json` mirrors only the description, which is unchanged.
- `CLAUDE.md` line 11: "Current version: **2.4.0**", with a new leading sentence:

  > 2.4.0 (the 2026-10-22 LibKa0s #45–#58 run) teaches `wow-revendor-libka0s` the `LibKa0s icons:` declaration (derive, confirm, split a run-on provenance line), the tag's `tools/prune-icons.lua` prune, the whole-catalog test blocker and the icon-set README credits; makes the standards audit read a pruned `media/icons/` as the declaration working; and adds the kit-41 crashed complexity bucket (`crashedFiles`) to `bump-version`, `wow-automated-tests` and the WoW review.

- `README.md`: the `wow-revendor-libka0s` row (line 64) gets one sentence on the declaration, prune and credits. The `bump-version` row gets "zero crashed files". No count changes.
- `docs/ARCHITECTURE.md`: no command or agent count changes. Check with grep only.

### B9. Gate (dev-copilot CLAUDE.md, *Build / test / run*)

- `python3 scripts/test_detect_profile.py` (17)
- `test_check_overlays.py` (15)
- `test_bounded_runs.py` (26)
- `test_normalize_eol.py` (13)
- `test_curseforge_journal.py` (48)
- `python3 scripts/check_overlays.py` → `OK: 13 overlays`
- both manifests parse
- `dev-copilot-profile` against an addon, LibKa0s, WowAddonStandards, CommonTasks, this repo and a generic repo
- `/reload-plugins` counts
- LF only

Then merge on the owner's go-ahead. **The owner runs `/plugin update` and `/reload-plugins` before the re-vendor sweep.** No tag (memory: dev-copilot 2.1.0 shipped without one).

---

## C. GitHub issue actions

Act only after the owner authorizes the merges. Space writes at least a few seconds apart (memory: throttle). Each close sets `state:done` or `state:will-not-do`, removes the old `state:*` label, and carries a closing comment citing the merge SHAs.

### LibKa0s

| Issue | Action | Comment carries |
|---|---|---|
| #45 dead exports | close `state:done` | OptionsTabs minor 9 removes `O.__releaseChrome`; kit 41 removes `Kit.__deviationRows`/`__declineFor`; library-stack-§7 `__` clause (v2.86.0); the seven dead stub mirrors removed at re-vendor |
| #46 runner ignores exit status | close `state:done` | kit 41: stderr out of the parse, exact footer shape, `rc ∈ {0,1}` with a valid footer is a measured run, figures zeroed, `CCN_MAX` zeroed |
| #47 sanitizer/parity shape | close `state:done` | the `crashed` bucket with per-file retry and `crashedFiles`. **Rejected:** the `forInFunctionLiterals` detector (zero instances) and the sanitizer rewrite (under-counts CCN); triggers recorded |
| #48 test-mode strip | close `state:done` | `W.TestStrip` (Widgets 13); adopters DW, LH, BL, MM. **Rejected:** a shared tone table (false premise) |
| #49 DW promotion candidates | close `state:will-not-do` | all four rejected plus the surfaced readers and format-compiler; census, failed bar and re-check triggers (open-evolutions index) |
| #50 grid composer | close `state:will-not-do` | one consumer; premise gone (DW-H0, feedback-24); trigger without the "owner asks" clause; no API sketch |
| #51 item read and loot parser | close `state:done` | `Item.BonusIDsFromLink` (Item 3; adopters BL, LH). **Rejected** with reasons: LinkDetail/BetterLink, IdentityKey, EffectiveItemLevel, ItemLevelAt/QualityAt, QualityOf, Wowhead URL, loot-line parser |
| #52 search box and checkbox | close `state:done` | `W.SearchBox` with the gold focus line for all adopters (LH, BL, DW). **Rejected:** `W.Checkbox` (no consumer) and an exported flat skin |
| #53 step panel | close `state:done` | `W.StepPanel` (WidgetsStepPanel 1), used by Sim [and PerfPanel, unchanged look]. **Rejected:** exporting step constants |
| #54 Sim-1.0 | close `state:done` | `LibKa0s-Sim-1.0`; DW migrated, LH and BL new simulators. **Rejected:** "five safety rules enforced by the library", now a host contract in preview-mode |
| #55 icon attribution | close `state:done` after the sweep | documentation-§1 item 12 (v2.86.0); credits per addon in each re-vendor commit. **Rejected:** a picker-credit helper |
| #56 icon styling and glows | close `state:done` | `LibKa0s-Glow-1.0` (adopters DW, QC, KickCD); library-stack-§2 row. **Rejected:** IconStyle, glow lifecycle, GLOW_STYLES/KNOBS defaults, `O.GlowGroup`, LSM `Solid` |
| #57 icon subset | close `state:done` after every consumer's v1.75.0 re-vendor | v1.75.0 tag; per-addon declaration commits; closed library-drawn set |
| #58 keybindings | close `state:done` | launcher-§6 (v2.86.0); BL, LH, MM, DW and WG implement. **Rejected:** a Launcher helper, with trigger; the kit `test_bindings` check deferred |
| #44, #6, #5, #3 | untouched | — |

### WowAddonStandards

| Issue | Action | Comment carries |
|---|---|---|
| #8 hazard row | close `state:done` with v2.86.0 | corrected facts: the axis is line shape, not scope; the single-line or positional form is blind, the multi-line keyed form raises at either scope |
| #10, #11, #12 | untouched | — |

### Addon adopter issues

| Issue | Action |
|---|---|
| LootHistory#37, BankLedger#24 (simulator) | close `state:done` on merge (new simulators on Sim-1.0) |
| LootHistory#36, BankLedger#23, MultiMeters#59 (test strip) | close `state:done` on merge (TestStrip adopted). MultiMeters#59 also cites the header-off marker fix |
| MultiMeters#60, WhatGroup#24, KickCD#38 (simulator) | comment only: Sim-1.0 shipped in v1.75.0; build on it when this addon's turn comes; host contract in preview-mode. Keep `state:triaged`, or the owner closes `state:will-not-do`; owner's call (open question) |

### New issues to file

Use labels `state:untriaged` + `severity:` + `bug`. Skip any that is fixed inside this run.

1. **LootHistory, `severity:low`.** "Price-sources host reparented onto a pooled SimpleGroup has no OnRelease undo (options-ui-§19, anti-pattern #93)." Evidence:
   - `settings/Panel.lua:792-805`: `AceGUI:Create("SimpleGroup")`, then `hf:SetParent(placeholder.frame)`, with no `OnRelease`;
   - the only undo is renderer-side, at `:997-1004`;
   - it is latent today, because every release goes through `renderGeneral`'s park;
   - fix with a guard on `hf:GetParent() == w.frame`, as DropWatcher did (`PageEditors.lua:272`);
   - the test is red under removal of the placeholder's `OnRelease`.
2. **DropWatcher, `severity:low`.** "`ItemRead` bonus walk can leave a nil hole and take the modifier offset from an undefined border." Evidence: `core/ItemRead.lua:55-57`. `bonus[i] = int(...)`, then `at = at + #bonus`. Fix: advance by the declared count. Addon-local; DW keeps its walk because it also reads modifiers.
3. **DropWatcher, `severity:low`.** "Restriction announce edge omits the combat flag, so PLAYER_REGEN edges may go unannounced under the Combat type." Evidence: `modules/Restrictions.lua:139-142` signs reason, canSendChat, canInspect and canTrade only; QuickComms `5a96af0` added `|..inCombat()` for the same defect. Needs the owner's in-client confirmation.
4. **QuickComms, `severity:low`, unless fixed in this run.** "Toggle Comms Pads prints the disabled line under the perf hold alone (slash-commands-§7, launcher-§6)." Evidence: `settings/SlashVerbs.lua:70`. `if NS.IsStoodDown() then return NS.Print(NS.SlashCommands:DisabledLine()) end`, and `IsStoodDown` is true under the `perf` hold (`core/LifecycleSetup.lua:14`). This is already a MUST NOT today. See open question 1.

---

## D. Per-addon standard rollout owed by v2.86.0 (for the bundle's `items.tsv`)

**launcher-§6 binding, plus `tests/test_disabled.lua` step 8:**
- Bank Ledger (ledger browser). Its `toggleWindow` → `verb("toggle")` → `B:Toggle`, so the refusal must come through the helper.
- Loot History (History browser).
- Multi Meters (meter windows). `M:Toggle` already refuses (`WindowManager.lua:738-741`); confirm it picks the line by hold.
- Drop Watcher (drop feed).
- WhatGroup (group popup).
- Quick Comms: the binding exists; only the refusal-by-hold fix (C, new issue 4).

**preview-mode marker:**
- Multi Meters: header-off gap, fixed by adopting TestStrip.
- Loot History and Bank Ledger: TestStrip replaces the red title badge.
- Drop Watcher: TestStrip replaces its own copy.
- WhatGroup: the "Test Group" name counts if the owner agrees.
- AbsorbTracker, KickCD, PanelMaster, PartyFrameEnhanced, ConsumableMaster: audit the unlock-preview handle label.
- AuraMaster: test mode only, no window. Audit its marker.

**documentation-§1 credits:** Open Iconic SHOULD in Consumable Master, Panel Master, Party Frame Enhanced, Pretty Chat and WhatGroup. Quick Comms already meets the Game-icons MUST.

**Everyone:**
- `wow-revendor-standards` to v2.86.0 (TOC `X-Standard`, README badge, `CLAUDE.md`).
- The `LibKa0s icons:` line, including any library-drawn names newly required by adopted widgets.
