# SP-AMX-01 research: empty weapon-enchant name on a fresh login (2026-09-29)

Read-only research against Blizzard's AuraContainer source (Gethe/wow-ui-source, branch `live`, fetched
2026-09-29) and AuraMaster `master`. Condensed from the research agent's report.

## How the engine names an enchant frame

- Enchant data (`CreateAuraData`, Blizzard_AuraContainerEnchantments.lua:337-353) carries no `name`, so
  `AuraContainerUtil.SetSpellNameForAura` (Blizzard_AuraContainerUtil.lua:241-263) falls back to the
  **equipped item's name**: `Item:CreateFromEquipmentSlot(inventorySlot):GetItemName()`; when that is nil
  it registers `item:ContinueWithCancelOnItemLoad(function() auraButton:UpdateAuraDisplay() end)` and
  writes `""`. (That is why the bar reads "Aln'hara Cane", not the oil.)
- The retry rides one event (AsyncCallbackSystem, `ITEM_DATA_LOAD_RESULT`): `success=false` clears the
  callback; a location lookup that stays nil while the ID is cached ("rare cases", Blizzard's comment)
  never re-fires. Nothing else retries the name.
- What re-fills an enchant frame: `RefreshItemEnchantments`, from `WEAPON_ENCHANT_CHANGED`,
  `WEAPON_SLOT_CHANGED`, `AddItemEnchantment`, and `UpdateAllAuras` while enabled. No ticker.
- **Asymmetry**: an unchanged enchant is only updated in place (`ShouldReassignForEnchantmentInfo`
  false → `UpdateAuraInstance`, same-string `SetText`); it is never cleared and reassigned, unlike pooled
  aura frames (`ResetAuraFrames` skips slots and enchantments). A disabled engine's `UpdateAllAuras` does
  clear enchants (`ClearActiveItemEnchantments`).

## Why it stays blank (two candidates; not separable without an in-client check)

- **H1 font not loaded**: the name was drawn before the addon font file loaded; later same-string
  rewrites may not redraw it (the time text heals because it changes every second).
- **H2 item data not ready**: `GetItemName` nil at the login build and the async retry lost.
- AuraMaster's font-primer world refresh runs only if something was primed, at 1.5 s, and its
  `UpdateAllAuras` + re-apply only do same-string rewrites for enchants.
- Owner check while a bar is blank: `/dump C_Item.GetItemName(ItemLocation:CreateFromEquipmentSlot(16))`
  (non-nil → H1).

## Fix (covers both)

`ContainerClass:ResetEnchants()`: on a live instance (engine, enchant frames, not parked/stale,
`ShouldShow()` and not previewing) call `SetEnabled(false)` then `SetEnabled(true)`, which forces a clear
(`""`, Hide) and a fresh `InitializeItemEnchantmentFrame` with a fresh `GetItemName`. Triggers:
loading-screen end (after about WORLD_REFRESH, independent of the primer), and the equipped weapon's
item data arriving (`Item:CreateFromEquipmentSlot(slot):ContinueOnItemLoad`, or `ITEM_DATA_LOAD_RESULT` /
`GET_ITEM_INFO_RECEIVED` for `GetInventoryItemID("player", 16|17)`, debounced). Never flip an engine that
should be off. `SetEnabled` / `UpdateAllAuras` are public inbound calls (secure delegates), already used
by AuraMaster in combat; enchant data is not a secret aura. Legal in combat and while secret.

## Redraw options (owner chose: light = B, full = B + C; D not offered)

| Option | Calls | Combat | Secret | Note |
|---|---|---|---|---|
| A light refresh | `UpdateAllAuras` | legal | legal | does NOT reset enchant names (in-place update) |
| B flip | `SetEnabled(false/true)` on live instances | legal | legal | repaints groups and resets enchants |
| C re-apply in place | `RequestApply(nil,true)` → Restyle re-binds every button | deferred | deferred | touches buttons, must be held |
| D full rebuild | Retire + Build new engines | forbidden, defer | forbidden, defer | leaks one engine frame per container per run (frames are never freed) |
