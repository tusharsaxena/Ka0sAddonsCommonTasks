# LibKa0s tooltip-place hook (v1.68.0) and its collection-wide re-vendor

**Why.** AuraMaster #22 smoke feedback (owner, 2026-10-02): the drag strip's tooltip should sit beside
the strip, to its right, or its left when the strip is near the right screen edge, not at the cursor.
The tooltip is LibKa0s-Widgets' (`WidgetsDragHandle.lua`), and a host whose strip hangs under a
restricted frame (AuraMaster's anchor inherits `DisableUntrustedLayoutScriptsTemplate`) cannot own it
by the strip, so the widget gains a host hook. The owner then asked (same day) that v1.68.0 be
re-vendored into every Ka0s addon, adopting where necessary.

**Scope.** `../WowAddonStandards/standards/ADDONS.md` is the roster (not copied here).
- LibKa0s: optional `tooltipPlace(tip, frame)` (spec and descriptor), owner UIParent `ANCHOR_NONE`,
  called after Show under pcall, falling back to the cursor tooltip; existing hosts byte-identical.
  WidgetsDragHandle minor 3 to 4, release v1.68.0 per `../LibKa0s/docs/releasing.md`, tag LOCAL only.
- AuraMaster: re-vendor and adopt (its own placement reads the strip through `NS.Secrets`, right of the
  strip, left when its right edge plus the tooltip would leave the screen, cursor when unreadable).
- AbsorbTracker, ConsumableMaster, KickCD: the three other drag-strip hosts. Re-vendor, then decide per
  strip: adopt beside-strip placement where the strip tooltip is cursor-owned today; where it is already
  owned by the strip (ConsumableMaster, per the widget's own docs) adoption is not necessary, recorded in
  the commit body. A declined candidate is NOT filed as an issue unless the reason is a real gap.
- The other seven: re-vendor only (no strip).

**Rules.** Same branch name in every repo: `feat/2026-10-02-drag-attach` (AuraMaster's, already open).
Each repo's own `CLAUDE.md` governs its gate, provenance line (`Bundles LibKa0s vX`) and docs. Commit
subjects start `<ID>: `; independent review notes under `refs/notes/ka0s-review`. Payload copied
whole (`libs/LibKa0s/`, `tests/_kit/`), byte-identical to the v1.68.0 tag. Push feature branches at
the M2 checkpoint; merge, the v1.68.0 tag push and branch deletion wait for the owner's go-ahead.
No addon version bump.

**Order.** M0 this bundle. M1 TP-LK-01. M2: TP-AM-01 after AuraMaster's DD-15 lands (shared tree), the
other ten in parallel. M3 TP-FIN-01. State: `./resume-state.sh`; restart: `RESUME.md`.

**Smoke (owner).** AuraMaster DRAG-11 (tooltip beside the strip, flips left near the right edge); the
same hover on AbsorbTracker's, ConsumableMaster's and KickCD's strips if adopted. Never marked passed
by the orchestrator.
