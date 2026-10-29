# Decisions taken by the lead

Each is derived from the owner's rulings in `00_PLAN.md` (R-1..R-12). Reports in `inputs/inventory/` hold the
evidence; the id in brackets names the report and the question.

## The Scope, settled once (governs LK-05, LK-06, every addon)

**D-01. "Ignore settings panel" covers the settings panel and nothing else.** That is the AceGUI pages, the
Options chrome (drawer, nav, tabs, id lists, the Skin tab) and any library widget a host places *on a settings
page*. Windows (debug console, copy window, perf and sim panels, drag strips, the first-run picker, an addon's own
editor modals and browsers) are windows: they wear the skin whatever that switch says. "Ignore fonts" applies to
every string the library paints, windows and HUD included. [lib-widgets 4.2; AbsorbTracker "open dependency";
QuickComms (b)]

**D-02. How a widget knows it is on a settings page.** `S.Text(fs, role, { panel = true })` opts in (S.Text is
used on windows too, so it cannot be panel-scoped by default). `WidgetsReorder` is panel-scoped by default with an
opt-out, because every consumer puts it on a settings page; the same `panel` flag is offered on every owned
Widgets constructor (Dropdown, SearchBox, TestStrip, Autocomplete, LineChart, DragHandle). The test is the
public `Skin:GetIgnore(owner)` panel half, never the internal `__PanelSkinned`. [lib-fonts-scope LK-05]

**D-03. Host paints on a settings page follow the same rule.** Where an addon paints its own settings-page
surface from tokens (LootHistory's AH price table, MultiMeters' reorder ghost colors), it gates on
`Skin:GetIgnore(owner)` (public already), so one page never mixes stock and skinned. [LootHistory D-LH-1 (b);
MultiMeters]

## R-2, the stock look

**D-04. Retire `opts.stockDefault`; keep `opts.stock`.** `stockDefault` is the "stock look under Ka0s Default"
switch, and it goes (`P.keepStock` and the `stockKept` mark with it; the `stock` mark Shell and CloseButton use
stays). `opts.stock` is not a stock look: it is a list of template art to fade, honoured under every skin, and the
library's own OptionsTabs depends on it. It stays; its doc example (`stock = { win.Bg }`, a frame the list drops)
is corrected. Stale `stockDefault` keys are ignored without error. [lib-stock-close-picker; QuickComms (a)]

**D-05. PremadeGroupsFilterExtension's metal panel retires (option A).** It is the addon's stand-in for a working
`stockDefault`, and R-2 says Ka0s Default looks like Ka0s Default everywhere and the stock look is the WoW Default
skin. PG-01 makes the panel one frame painted through the facade and amends the ratified deviation row
(`docs/ARCHITECTURE.md:478`). The degraded install (no library) keeps the template art. [PremadeGroupsFilterExtension §0]

**D-06. QuickComms' popup and browser chrome go Ka0s under Ka0s Default.** They are windows (D-01), so R-2 applies
as written; `docs/ARCHITECTURE.md:333` is rewritten. [QuickComms (b)]

**D-07. `__chromeAway` is renamed in comment and meaning to what it does.** Since SkinPaint minor 6 it paints under
Ka0s Default too, which is what R-2 now asks for. LK-06c corrects the helper's comments and the IdList help-mark
comment instead of restoring the old constants. [lib-widgets F-1]

**D-08. `P.unpaint` restores TitleBar's text alignment** (a gap found while reading LK-02's sites); it lands in
LK-02. [lib-stock-close-picker]

## R-1, Ignore fonts

**D-09. The gate sits in `S.Resolve` and `Token` for `hud.font` and `hud.outline`**: while the owner ignores fonts,
Resolve returns the stored value (a stored `"@skin"` gives nil) and Token gives nil. The composer's preview follows
from it; the font picker stays disabled while Ignore fonts is on (R-1 does not ask to lift that). BarStyle's font
fields are nil while fonts are ignored. [lib-fonts-scope]

**D-10. DropWatcher's monospace glyph face stays the skin's `font.mono` under Ignore fonts.** It is chosen for glyph
coverage (▲ ≈ ▼), not looks, and the override already leaves `font.mono` alone. [DropWatcher]

## R-4, the HUD faces

**D-11. One face per skin, each already shipped and OFL, same family as the skin's text, the heavier weight**
(HUD text is 12 px under an OUTLINE): Obsidian Inter SemiBold, Azeroth Vollkorn Bold, Glass Nunito SemiBold, High
Contrast Atkinson Bold, Ember Bitter Bold, WoW Midnight Philosopher Bold, WoW Forever Fira Sans SemiBold. **WoW
Default** sets Friz Quadrata explicitly: it is the client's own face, which "OFL only" (a rule about faces the
library ships) does not touch, and the skin's point is the client look. `hud.outline` stays OUTLINE and
`hud.fontSize` 12 everywhere. [lib-tokens-api LK-04]

## R-5, the custom widgets

**D-12. LK-06 splits into four items** (plan-data/addendum-01.tsv): LK-06a Widgets controls, LK-06b tool windows
and the Core grip (SimPanel's owner-less dropdowns, F-2, included), LK-06c Options chrome, LK-06d the tooltip lines
the library writes. Toast, Launcher, SimTimeline, Glow, the Core window and close control, OptionsCombat, the
Options header, OptionsAppearance, OptionsCompose and the chat-markup strings need no item (already token-painted
or no surface). [lib-widgets 4.1]

**D-13. Newly fonted strings take Ka0s Default's face (Oxanium).** Routing them through `P.font` is what lets
Ignore fonts act on them, so R-5 implies it; each one is listed in the smoke test. [lib-widgets D-1]

**D-14. Tooltip colors use the existing tooltip tokens, not new near-duplicates.** LK-08's title `gtip.title`, body
`gtip.value`, plus one new `gtip.footer` (Ka0s Default 0.6 gray, following `gtip.muted` in the other skins).
SimPanel's key column takes `gtip.title` and IdList's 0.8 lines `gtip.body` (a slight shift under Ka0s Default,
recorded, in exchange for one tooltip palette across the collection). Nil-colored tooltip lines stay the client's.
Suggestion popup rows take `menu.text`, like the dropdown menu. New tokens `list.hoverArt` and `icon.grip` (both
`false`, the client's art, under Ka0s Default and WoW Default). [lib-widgets D-2, D-4, D-5, D-6, section 3]

**D-15. The skin picker is a window, not the settings panel**, and its rows keep previewing each skin's own face
under Ignore fonts: they exist to show the skins. [lib-widgets D-3]

## R-9, R-11

**D-16. `Skin:DrawsKey(owner)`, lib-level, not a facade member** (a facade member would turn nine addons' parity
tests red). `__DrawsKey` stays one release as an alias: PremadeGroupsFilterExtension's tests call it until PG-01
moves them. [lib-tokens-api LK-10]

**D-17. The picker's owner line** is `frame.ownerLabel`, painted `heading`, on its own line above the dropdown; the
window widens to the label's unbounded width and refits on every show and skin change. [lib-stock-close-picker LK-11]

## Everything else

**D-18. LootHistory joins** (gate green on master: 1830/0/1, luacheck 0/0); its re-vendor is v1.79.0 → v1.81.0 and
meets v1.80.0's consumer obligations too. [LootHistory]

**D-19. A `ResetToSkin` guard inside a schema step that already shipped stays** (QuickComms): the step must keep
producing the same result for a profile that migrates late. LK-07 fixes every absent companion, picker keys
included. [QuickComms (c)]

**D-20. One minor bump per file per release, one new docs version file per docs key.** An implementer whose file was
already bumped on the run branch does not bump it again. [lib-widgets 4.1; lib-fonts-scope]
