# Owner rulings after M3 (2026-10-29)

The owner's answers to `99_REPORT.md` §Owner calls. These are addendum items in `plan-data/addendum-02.tsv`.

- **R-1 (call 1), KickCD cast-bar borders:** keep an edge. → **KC-A1**: both cast-bar BorderGroups follow the
  icon border family (`fromSkin = "icon"`), a flat edge under every skin.
- **R-2 (calls 3 and 4), the Ka0s Default look changes** (Oxanium on addon-drawn text, the title bands,
  the flat controls, the library scroll bars): accepted as built. No change.
- **R-3 (call 5), MultiMeters window chrome:** it follows the skin. → **MM-A1**: the inventory's D1, D3, D4
  and D16, covering the fill, the edge, the header strip and the header controls, taken onto the skin
  by the one-time reset.
- **R-4 (calls 6 and 7), make these consistent with every Ka0s addon and skin:**
  - BankLedger's close control → **BL-A1**: the library's `S.CloseButton` with no `stockDefault`, the same
    as every other addon.
  - PrettyChat's TreeGroup (X11) keeps the library's flat edge, which is already how every AceGUI widget
    the library paints looks in every addon. No change.
- **R-5 (call 8), the old-session trailers:** leave them.
- **Call 2 (Ignore fonts and the HUD):** the owner made no ruling, so the HUD stays as built and
  documented. It remains library follow-up 1 in `99_REPORT.md`.
- **Then:** sync docs, merge, push and delete every branch (M4), on the owner's go-ahead given here.
