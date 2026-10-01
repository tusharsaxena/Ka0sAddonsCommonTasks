# Design and decisions

Drawn from `plan-data/design-scout.json` (two design agents, seven host scouts, one standard and plugin
scout, all read-only on 2026-10-02). The owner said "go ahead and fix all these 9 issues", so the
orchestrator took every decision below without asking. Each one is listed in `99_REPORT.md` for review.

## D1. LibKa0s#41: Core minor 10 adds three optional `MakeResizable` fields

| Field | Contract |
|---|---|
| `canResize` | `function(frame) -> truthy/falsy`. Read fresh at every left mouse-down, before `StartSizing`. Falsy refuses: nothing starts, and the next mouse-up is inert (no stop, no `onResize`, no `onResizeStop`). A drag already under way finishes even if the answer flips. Never touches the grip's visibility. Not a function: ignored. |
| `onResizeStop` | `function(w, h)`. Runs once per mouse-up that ends a sizing the grip started, after `onResize`. Never from `OnSizeChanged`. This is where a host persists geometry; `onResize` (every size tick) is for relayout. |
| `gripParent` | Frame the grip is built on, anchored to and levelled from. Default: the sized frame. Sizing, bounds and the user-placed flag stay on the sized frame. `frame.resizeGrip` stays on the sized frame. |

Every existing caller passes none of them and is unchanged. No member is added, so no degradation stub moves.

**Why a predicate:** LootHistory keeps its grip visible and inert when locked, which a hidden grip cannot
express. Two of the three grip hosts tie the grip to the lock, so this is a collection semantic, not one
host's flag (library-stack-§7 bar 2). **Why `onResizeStop`:** every host saves on release only. Mapping the
save onto `onResize` would write SavedVariables on every frame of a drag and on every programmatic `SetSize`.
**Why `gripParent`:** MultiMeters sizes a clean anchor but draws on the art frame (its rule R3). Without it,
the grip would lose the window's strata, alpha and rule-driven visibility.

**Rejected:** hosts hiding `frame.resizeGrip` (cannot express visible-but-inert, and needs every visibility
writer to agree); a library-owned locked look (the standard is silent, and the hosts disagree); `gripSize`
and `gripInset` (corner consistency across the collection is the argument LootHistory's own register row
ratified; MultiMeters' grip grows from 12 to 16 px, smoke WIN-37 decides).

## D2. LibKa0s#42: every host passes `addonName`; the library guards it

- **Option 1 (derive a default) is unavailable.** Nothing on the Options descriptor is the folder name, and
  library-stack-§8 forbids substituting a frame-name prefix or a title.
- **Option 2 is chosen**, with a guard: `idHelpIcon` accepts `d.addonName` only when the client says that
  addon is loaded (`C_AddOns.IsAddOnLoaded`, then the global; trusted when neither exists, as headless). A fall
  past that rung emits one `d.debug("Cfg", ...)` line per instance, saying why. A wrong name therefore yields
  the client glyph and a debug line, never a dead texture path.
- OptionsIdList minor 2 → 3. Options minor 27 → 28 (docblock correction: the reader is OptionsIdList, and the
  field is the folder name, not MasterControls' display `addonName`).
- **Correction to the issue:** only AuraMaster draws help marks today. BankLedger and LootHistory pass no `help`
  on their IdList entries, so for them, and the eight addons with no IdList, the change is latent.
- **Standard (CA-STD-01):** options-ui-§1's descriptor table gains an `addonName` row, and the
  `NEW_ADDON_CONTEXT.md` template descriptor carries `addonName = addonName,`. Standard v2.75.0.

## D3. Host decisions

| # | Host | Decision |
|---|---|---|
| D3.1 | BankLedger | *Lock frame* only stops the drag today; resizing a locked window works. Kept: no `canResize`. Gating it is the owner's call (smoke SESS-13 records it). |
| D3.2 | BankLedger, LootHistory | The library-absent arm of `core/CoreSetup.lua` keeps a working fallback grip (today's grip, moved), per each host's seam policy of working pre-library fallbacks. |
| D3.3 | MultiMeters | The library-absent arm publishes `NS.MakeResizable = function() return nil end`: no grip on a degraded install, per its seam's rule that a stub must not re-implement the library. The live arm gates on Core minor ≥ 10, because an older Core would ignore `gripParent` and `onResizeStop`. MultiMeters keeps hiding the grip on lock and minimize, and also passes `canResize` as defence in depth. |
| D3.4 | LootHistory | `canResize = not B:IsLocked()`. A mouse-up after a refused mouse-down no longer saves (strictly more correct; the characterization test is updated deliberately). |
| D3.5 | AbsorbTracker | `/at profile list` reads `Slash.ProfileNames` (sorted, current always listed) with the `Available profiles` header kept; the library-absent arm keeps the store's own list. |
| D3.6 | AbsorbTracker, ConsumableMaster, KickCD | The library-absent arm defines its own minimal verb split and lookup (slash-commands-§1 sanctions minimal stub dispatch). Degraded sub-help prints plain `cmd  desc` rows; it must not copy `FormatRow`. |
| D3.7 | KickCD | `PANEL_HEADER_TOP` and `PANEL_HEADER_HEIGHT` are deleted, not re-read: `lib.LAYOUT`'s header values are INTERNAL and never handed to a host (options-ui-§8). Two duplicates the issue missed are folded in: the `/kcd spells` sub-help loop and `runDebug`'s inline verb split. |
| D3.8 | MultiMeters | `Diagnostics.SECRET` has zero readers and is deleted, not aliased. |
| D3.9 | PanelMaster | The degraded stub gains `PADDING_X = 0`, beside its other zero placeholders. |
| D3.10 | ConsumableMaster | `core/SlashDump.lua`'s third verb split is outside #44 and left alone. |
| D3.11 | All | `"<secret>"` survives only in each library-absent arm (events-frames-taint-§8 allows exactly that copy). |

## Not done

No standard rule that a locked window must not resize (the scout offered one as optional). No `gripSize`
option. No addon version bump.
