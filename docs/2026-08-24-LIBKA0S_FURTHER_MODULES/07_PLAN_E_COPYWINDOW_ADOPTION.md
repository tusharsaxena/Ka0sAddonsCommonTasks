# Plan E — `Widgets.CopyWindow` adoption in three addons

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace three hand-rolled export copy windows with `LibKa0s-Widgets-1.0`'s
`CopyWindow`, and correct the source comment that has been asserting a copy count nobody was
checking.

**Architecture:** Each addon's `EnsureCopyFrame` / `ShowCopy` pair collapses into one
`W.CopyWindow(descriptor)` handle built lazily at first use. The descriptor carries what is
genuinely per-addon — the frame's global name, the monospace face, the title, the skin function and
the anchor — and nothing else changes: same size, same strata, same backdrop alpha, same Esc wiring.

**Tech Stack:** Lua 5.1, LibStub, each addon's vendored test kit, `luacheck`, plus one in-client
smoke check per addon.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §D

**Prerequisite:** [`04_PLAN_B_LIBKA0S_MODULES.md`](04_PLAN_B_LIBKA0S_MODULES.md) Task 8 — Widgets
minor 6 is vendored into all three addons.

## Global Constraints

- Lua 5.1. `luacheck .` **0/0** and `lua tests/run.lua` green before every commit.
- **`LibStub("LibKa0s-Widgets-1.0", true)`** — silent flag, always.
- **No visual change.** All three windows are 640×420 at `FULLSCREEN` strata with a
  `0.06/0.06/0.08/0.95` backdrop and 10pt monospace text today; the descriptor reproduces exactly
  that. A window that comes out different is a bug in the adoption, not an improvement.
- **The `Show` ordering is the library's now** — width, text, cursor, show, focus, highlight. No
  addon re-implements it, and no addon reaches past the handle to do it differently.
- **Each addon keeps its own degraded path.** With no library there is no copy window; the export
  button must say so rather than erroring, exactly as each addon already degrades elsewhere.
- **This is the one plan with an in-client step.** A copy window is a frame with focus, selection
  and an Esc binding, and none of those three things are observable headlessly. Each task ends with
  a smoke check that must be recorded in the addon's `docs/smoke-tests.md`.
- One commit per addon.

---

### Task 1: MultiMeters — and the comment that was wrong

**Files:**
- Modify: `MultiMeters/modules/Export.lua:788-792` (the comment), `:995-1091` (the frame builder and
  `showCopy`)
- Modify: `MultiMeters/core/WidgetsSetup.lua` if one exists, or create it — check first
- Test: `MultiMeters/tests/test_export.lua`
- Modify: `MultiMeters/docs/smoke-tests.md`

**Interfaces:**
- Consumes: `Widgets.CopyWindow(descriptor)` from `04_PLAN_B` Task 4.
- Produces: nothing other modules read — the handle is file-local to `modules/Export.lua`.

MultiMeters goes first because it is the addon whose source comment prompted the register entry, and
because it is the one copy that is **not** a near-clone of the other two — if the descriptor covers
this one it covers all three.

`modules/Export.lua:788-792` currently reads, in part: *"a deliberate local copy of the one in
LootHistory and the one in LibKa0s' debug log — the third in the collection, recorded as a harvest
candidate for the library rather than fixed here."* It was the **fourth**: BankLedger's copy predates
it and nobody was looking. The comment asserted a count that was never checked, and correcting it is
part of this task rather than a follow-up.

- [ ] **Step 1: Find the existing Widgets seam**

```sh
cd MultiMeters && grep -rn "LibKa0s-Widgets-1.0" --include='*.lua' . | grep -v '/libs/'
```

If a seam file already exists (LootHistory has `core/WidgetsSetup.lua`), extend it. If the lookup is
inline in `modules/Export.lua`, leave it there — this addon's dropdown adoption chose that shape and
consistency inside the file beats consistency with another repo.

- [ ] **Step 2: Write the failing test**

Append to `MultiMeters/tests/test_export.lua`:

```lua
-- ── the copy window ──────────────────────────────────────────────────────────────────────
--
-- This addon's copy frame described itself as "the third in the collection". It was the fourth —
-- BankLedger had one too, and nobody was looking. It is now none of them: the frame belongs to
-- LibKa0s-Widgets-1.0 and this file passes a descriptor.

test("Export: the copy window comes from LibKa0s-Widgets-1.0", function()
  local source = io.open("modules/Export.lua"):read("*a")
  local _, builders = source:gsub('CreateFrame%("EditBox"', "")
  assertEqual(builders, 1,
    "only the whisper box builds an EditBox here now; the copy window's belongs to the library")
  assertTrue(source:find("CopyWindow", 1, true) ~= nil, "the descriptor call is present")
end)

test("Export: showing the copy window puts the text in it", function()
  local text = "Metric,Value\r\nDPS,1234\r\n"
  NS.Export.__showCopy(text)
  assertEqual(NS.Export.__copyWindow:GetText(), text)
end)

test("Export: the copy window is built once and reused", function()
  NS.Export.__showCopy("first")
  local f = NS.Export.__copyWindow:GetFrame()
  NS.Export.__showCopy("second")
  assertTrue(NS.Export.__copyWindow:GetFrame() == f,
    "a rebuild per open leaks a frame per open — frames are never destroyed in WoW")
end)
```

`__showCopy` and `__copyWindow` are new publications on the module, on the model of the existing
`Export.__geometry`. Publish them beside it, with a comment saying they exist because an `EditBox`
is write-only through the frame API and this is the only way to assert what the window is showing.

- [ ] **Step 3: Run it to verify it fails**

```sh
cd MultiMeters && lua tests/run.lua
```

Expected: FAIL — `__showCopy` is nil, and the `CreateFrame("EditBox"` count is 2.

- [ ] **Step 4: Replace the builder with a descriptor**

Delete `EnsureCopyFrame` (`:1010-1076`) and `showCopy` (`:1069-1091`) — read the exact bounds before
cutting — together with the now-unused `centerOnWindow` if nothing else calls it, and replace with:

```lua
-- The copy window belongs to LibKa0s-Widgets-1.0. What stays here is the descriptor: the frame's
-- global name, the face, the title, the skin and the anchor — the things a vendored library cannot
-- know about this addon. The build is lazy inside the library, so a session that never exports
-- creates nothing.
local copyWindow

local function ensureCopyWindow()
  if copyWindow then return copyWindow end
  local W = LibStub and LibStub("LibKa0s-Widgets-1.0", true)
  if not W or not W.CopyWindow then return nil end
  copyWindow = W.CopyWindow({
    addonName = addonName,
    name      = COPY_NAME,
    width     = COPY_WIDTH,
    height    = COPY_HEIGHT,
    title     = L["Export"] .. EM_DASH .. L["Ctrl+C, then Esc"],
    font      = Const.FONT_MONO,
    fontSize  = 10,
    editWidth = EDIT_FALLBACK_WIDTH,
    applySkin = NS.ApplySkin,
    -- Consulted on every show, so the popup lands over the window that spawned it wherever the
    -- user has since dragged it.
    anchorTo  = function()
      return type(invoker) == "table" and invoker.anchor or nil
    end,
  })
  return copyWindow
end

--- Show text in the copy window, selected and ready for Ctrl+C.
---
--- The ORDER inside the window — width, text, cursor, show, focus, highlight — is the library's
--- now. It was load-bearing here and it is load-bearing there; what changed is that it is written
--- down once.
local function showCopy(text)
  local win = ensureCopyWindow()
  if not win then return end
  win:Show(text)
end
```

Keep `COPY_NAME`, `COPY_WIDTH`, `COPY_HEIGHT` and `EDIT_FALLBACK_WIDTH` exactly as they are — the
descriptor is the only new thing, and a changed constant is a changed window.

**The `scroll:GetWidth()` read-back note at `:1085-1093` goes with the code it explains.** That
comment argues why reading geometry off a frame is legal here despite this file's rule R3; the
read now happens inside the library, so the note moves into the descriptor block in shortened form
rather than being deleted — the exemption still applies and a reader of R3 needs to find it.

- [ ] **Step 5: Correct the comment at `:788-792`**

```lua
-- Two frames rather than one. The modal picks what to export; the copy window shows the result, at
-- a higher strata so it sits ON TOP of the modal that spawned it.
--
-- The copy window is LibKa0s-Widgets-1.0's now. It used to be a deliberate local copy, and the
-- comment here called itself "the third in the collection" — it was the fourth. BankLedger had one
-- too, and the register that was supposed to be tracking them had never been written. Four copies
-- of one frame is four skins to keep in step, and the collection stops reading as one author's work
-- the first time one is restyled and the others are not.
```

- [ ] **Step 6: Gate**

```sh
cd MultiMeters && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0.

- [ ] **Step 7: Smoke check, in the client**

Add to `MultiMeters/docs/smoke-tests.md` and then actually run it:

1. `/mm` → open a meter window → Export → **Export to CSV**.
2. The copy window opens **centred on the meter window**, above the modal, with the CSV **already
   selected**.
3. Ctrl+C, paste into a text editor: the whole CSV, with its line breaks.
4. Esc closes the copy window and leaves the modal open.
5. Drag the meter window somewhere else, export again: the copy window follows it.
6. `/reload`, export again: still one window, still centred.

- [ ] **Step 8: Commit**

```sh
cd MultiMeters
lua tests/run.lua --list > docs/test-cases.md
git add modules/Export.lua tests/test_export.lua docs/smoke-tests.md docs/test-cases.md
git commit -m "refactor(export): the copy window comes from LibKa0s-Widgets-1.0

This file's own comment called its copy frame 'the third in the collection'. It
was the fourth — BankLedger had one too — and the harvest register the comment
cited had never been written. Both are fixed here: the frame is the library's,
and the comment says what was actually true.

No visual change: same 640x420, same FULLSCREEN strata, same 0.95 backdrop, same
10pt mono. The load-bearing Show ordering is written down once now instead of
four times."
```

---

### Task 2: LootHistory

**Files:**
- Modify: `LootHistory/modules/Export.lua:295-380` (`centerOnBrowser`, `EnsureCopyFrame`,
  `ShowCopy`)
- Modify: `LootHistory/core/WidgetsSetup.lua` — this addon already has a Widgets seam; extend it
  rather than adding a second lookup
- Test: `LootHistory/tests/test_export.lua`
- Modify: `LootHistory/docs/smoke-tests.md`

**Interfaces:**
- Consumes: `Widgets.CopyWindow(descriptor)`.
- Produces: `Export.__showCopy`, `Export.__copyWindow` for the suite.

- [ ] **Step 1: Read the existing Widgets seam**

```sh
cd LootHistory && cat core/WidgetsSetup.lua
```

Follow its shape — if it publishes `NS.Dropdown`, publish `NS.CopyWindow(descriptor)` beside it and
have `modules/Export.lua` call that rather than reaching for LibStub itself.

- [ ] **Step 2: Write the failing test**

Append to `LootHistory/tests/test_export.lua`:

```lua
test("Export: the copy window comes from LibKa0s-Widgets-1.0", function()
  local source = io.open("modules/Export.lua"):read("*a")
  assertEqual(source:find('CreateFrame%("EditBox"'), nil,
    "this file builds no EditBox any more; the copy window belongs to the library")
  assertTrue(source:find("CopyWindow", 1, true) ~= nil, "the descriptor call is present")
end)

test("Export: showing the copy window puts the text in it", function()
  local text = "when,item,quality\r\n1,Thunderfury,4\r\n"
  NS.Export.__showCopy(text)
  assertEqual(NS.Export.__copyWindow:GetText(), text)
end)

test("Export: the copy window is built once and reused", function()
  NS.Export.__showCopy("first")
  local f = NS.Export.__copyWindow:GetFrame()
  NS.Export.__showCopy("second")
  assertTrue(NS.Export.__copyWindow:GetFrame() == f, "no rebuild per open")
end)
```

- [ ] **Step 3: Run it to verify it fails**

```sh
cd LootHistory && lua tests/run.lua
```

- [ ] **Step 4: Replace the builder with a descriptor**

Delete `EnsureCopyFrame` (`:319-371`) and `ShowCopy` (`:373-380`), and `centerOnBrowser` (`:306-317`)
if nothing else calls it — check first, the export modal may use it too. Replace with:

```lua
local copyWindow

local function ensureCopyWindow()
  if copyWindow then return copyWindow end
  local W = LibStub and LibStub("LibKa0s-Widgets-1.0", true)
  if not W or not W.CopyWindow then return nil end
  copyWindow = W.CopyWindow({
    addonName = addonName,
    name      = "LootHistoryExportCopyWindow",
    title     = "Export \226\128\148 Ctrl+C, then Esc",
    font      = NS.Constants.FONT_MONO,
    fontSize  = 10,
    applySkin = function(f) if NS.Browser and NS.Browser.ApplySkin then NS.Browser:ApplySkin(f) end end,
    -- Over the History window wherever the user has moved it, and over the screen when it is not up.
    anchorTo  = function()
      local win = NS.Browser and NS.Browser.GetWindow and NS.Browser:GetWindow()
      return win
    end,
  })
  return copyWindow
end

local function ShowCopy(text)
  local win = ensureCopyWindow()
  if not win then return end
  win:Show(text)
end
```

`width`, `height`, `editWidth` and `backdrop` are **omitted deliberately** — the library's defaults
are this addon's existing values (640, 420, 590, `0.06/0.06/0.08/0.95`). Confirm that before
omitting them:

```sh
cd LootHistory && sed -n '319,371p' modules/Export.lua | grep -n "SetSize\|SetWidth\|BackdropColor"
```

If any differs, pass it explicitly rather than accepting a silent change.

The close button is the library's now (`Core.MakeCloseButton`, given `addonName`), so the
`NS.Browser:MakeCloseButton` call inside the old builder goes away — it drew the same glyph.

- [ ] **Step 5: Gate**

```sh
cd LootHistory && lua tests/run.lua && luacheck .
```

- [ ] **Step 6: Smoke check**

Add to `LootHistory/docs/smoke-tests.md` and run:

1. `/lh` → History tab → Export → **Export to CSV**.
2. The copy window opens centred on the History window, above the modal, text selected.
3. Ctrl+C, paste: the whole CSV.
4. Esc closes the copy window, the modal stays.
5. Repeat from the **Insights** tab — the second `Open` path with a different title — and confirm
   the same one window is reused.
6. Move the History window, export again: the copy window follows.

- [ ] **Step 7: Commit**

```sh
cd LootHistory
lua tests/run.lua --list > docs/test-cases.md
git add modules/Export.lua core/WidgetsSetup.lua tests/test_export.lua docs/smoke-tests.md docs/test-cases.md
git commit -m "refactor(export): the copy window comes from LibKa0s-Widgets-1.0

Fifty-two lines that were, character for character with the addon name
substituted, BankLedger's fifty-two. No visual change — the library's defaults
are this addon's existing constants, and the ones that are not are passed."
```

---

### Task 3: BankLedger

**Files:**
- Modify: `BankLedger/modules/Export.lua:213-284` (`centerOnBrowser`, `EnsureCopyFrame`, `ShowCopy`)
- Modify: `BankLedger/core/WidgetsSetup.lua` if one exists — check first
- Test: `BankLedger/tests/test_export.lua`
- Modify: `BankLedger/docs/smoke-tests.md`

**Interfaces:**
- Consumes: `Widgets.CopyWindow(descriptor)`.
- Produces: `Export.__showCopy`, `Export.__copyWindow` for the suite.

BankLedger is the copy nobody recorded. Its `EnsureCopyFrame` differs from LootHistory's by one
`copyFrame.title = t` assignment and one line wrap.

- [ ] **Step 1: Write the failing test**

Append to `BankLedger/tests/test_export.lua`:

```lua
test("Export: the copy window comes from LibKa0s-Widgets-1.0", function()
  local source = io.open("modules/Export.lua"):read("*a")
  assertEqual(source:find('CreateFrame%("EditBox"'), nil,
    "this file builds no EditBox any more; the copy window belongs to the library")
  assertTrue(source:find("CopyWindow", 1, true) ~= nil, "the descriptor call is present")
end)

test("Export: showing the copy window puts the text in it", function()
  local text = "when,item,quality\r\n1,Linen Cloth,1\r\n"
  NS.Export.__showCopy(text)
  assertEqual(NS.Export.__copyWindow:GetText(), text)
end)

test("Export: the copy window is built once and reused", function()
  NS.Export.__showCopy("first")
  local f = NS.Export.__copyWindow:GetFrame()
  NS.Export.__showCopy("second")
  assertTrue(NS.Export.__copyWindow:GetFrame() == f, "no rebuild per open")
end)
```

Read `tests/run.lua` for this repo's test global before writing `_G.BL_TEST`.

- [ ] **Step 2: Run it to verify it fails**

```sh
cd BankLedger && lua tests/run.lua
```

- [ ] **Step 3: Replace the builder with a descriptor**

Delete `EnsureCopyFrame` (`:231-283`) and `ShowCopy` (`:285-292`), and `centerOnBrowser` (`:221-229`)
if nothing else calls it. Replace with the Task 2 Step 4 block, with:

```lua
    name      = "BankLedgerExportCopyWindow",
    font      = NS.Constants.FONT_MONO,
    applySkin = function(f) if NS.Browser and NS.Browser.ApplySkin then NS.Browser:ApplySkin(f) end end,
    anchorTo  = function()
      return NS.Browser and NS.Browser.GetWindow and NS.Browser:GetWindow() or nil
    end,
```

Confirm the omitted defaults match, as in Task 2:

```sh
cd BankLedger && sed -n '231,283p' modules/Export.lua | grep -n "SetSize\|SetWidth\|BackdropColor"
```

- [ ] **Step 4: Gate**

```sh
cd BankLedger && lua tests/run.lua && luacheck .
```

- [ ] **Step 5: Smoke check**

Add to `BankLedger/docs/smoke-tests.md` and run:

1. `/bl` → open the ledger → Export → **Export to CSV**, with **All Data** selected.
2. The copy window opens centred on the ledger window, above the modal, text selected.
3. Ctrl+C, paste: the whole CSV including the `\r\n` line breaks the exporter writes.
4. Switch the Data Set to **Current View**, export again: the same window, new text, selected again.
5. Esc closes it; the modal stays open.

- [ ] **Step 6: Commit**

```sh
cd BankLedger
lua tests/run.lua --list > docs/test-cases.md
git add modules/Export.lua tests/test_export.lua docs/smoke-tests.md docs/test-cases.md
git commit -m "refactor(export): the copy window comes from LibKa0s-Widgets-1.0

This was the copy the collection's register never recorded — fifty-two lines
identical to LootHistory's but for one assignment and one line wrap, which is
why MultiMeters' comment could call itself the third of three and be wrong."
```

---

### Task 4: Verification

- [ ] **Step 1: Three copies gone, one left**

```sh
cd /path/to/GIT
grep -rn 'CreateFrame("EditBox"' --include='*.lua' \
  BankLedger LootHistory MultiMeters LibKa0s | grep -v '/libs/' | grep -v '/tests/'
```

Expected: exactly two hits — MultiMeters' whisper box (`modules/Export.lua`, a different widget) and
`LibKa0s/LibKa0s/DebugLog.lua`'s own copy window, which this plan deliberately leaves alone.

- [ ] **Step 2: All three green**

```sh
for a in BankLedger LootHistory MultiMeters; do
  ( cd $a && lua tests/run.lua >/dev/null && luacheck . >/dev/null && echo "green: $a" ) || echo "FAILED: $a"
done
```

- [ ] **Step 3: The windows still look identical to each other**

Open all three exports in one session and compare. They were three copies of one design; if the
adoption has made any of them look different from the other two, the descriptor is wrong.

- [ ] **Step 4: Documentation**

Run `/wow-addon:sync-docs` in each addon. Each `docs/module-map.md` entry for `modules/Export.lua`
should stop describing a copy frame it no longer builds.

---

## What is deliberately left undone

`LibKa0s/LibKa0s/DebugLog.lua:545` keeps its own copy window. It is the smallest of the four, it
lives inside the library already, and it is wired to `escClose`, `applySkin` and `dragBar` locals
that are file-scoped to `DebugLog.lua`. Converting it is worth doing **after** three consumers have
proven the descriptor's shape in a live client, not before — and it is a `DebugLog` minor bump with
its own API document, which is a different release from this one.

Record that as a comment beside `EnsureCopyFrame` in `DebugLog.lua` so the next reader knows the
omission was a decision:

```lua
  -- NOT LibKa0s-Widgets-1.0's CopyWindow, yet. This one predates it, it is the smallest of the four
  -- copies the collection had, and it is wired to escClose / applySkin / dragBar, which are locals
  -- of this file. Converting it is a DebugLog minor with its own API document — worth doing once the
  -- three host-side adoptions have proven the descriptor in a live client, and not before.
```
