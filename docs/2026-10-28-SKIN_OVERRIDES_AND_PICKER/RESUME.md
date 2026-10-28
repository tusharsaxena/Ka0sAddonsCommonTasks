# Resume: skin overrides and picker run

The owner paused the run on 2026-10-28 for a PC restart. Git is the state. In each repo, check out
`feat/2026-10-28-skin-overrides-picker` and run `git log --oneline` and `git status`.

## Done at the pause

- **LibKa0s:** SO-01..03, SO-06, PK-01..03 and SO-04 (71f5df8) are committed. SO-05 has three
  commits: d66fc1f, 3c9225f and 730c1d8 ("close v1.79.0 with its release record"). The branch is pushed
  only up to 183bc57; SO-04 and SO-05 are local.
- **LootHistory:** LH-01 is done and pushed (ca095c2).
- **LibKa0sSkinTester:** ST-01 is done and pushed (4540e17).
- **GitHub:** LibKa0s #63 and #64 are closed on the owner's word and labeled `state:done`.
- **Owner decisions:** the textures are approved, with Azeroth on Ka0s Parchment and WoW Forever on
  Ka0s Classic. Closing in combat keeps its revert, and a direct picker call in combat stays the host's
  concern. No skin has a 3px border, so the 3px-to-2px rule changes nothing.

## Left, in order

1. **SO-05 (finish).** Check that the release record is complete and the tree is clean. Create the local
   annotated tag `v1.79.0` (`git tag -l v1.79.0` was empty at the pause), made as v1.78.0 was. Never
   push it without the owner's go-ahead.
2. **LH-02 and ST-02.** Re-vendor both consumers from the tag. Use `git archive` of the tag, never the
   working tree. Prune icons per each repo's declaration and roll the CLAUDE.md provenance line back to
   its plain tag form. Add an in-game check that every skin's bars wear its own texture.
3. **ST-03 (owner's request).** Give the Skin Tester showroom a visible, skinned scrollbar that shows
   only when the content overflows. Today `modules/Showroom.lua` scrolls with the wheel only. Add tests
   and a smoke check.
4. Run the gates in all three repos and push the feature branches. LibKa0s's branch push includes SO-04
   and SO-05.
5. Write `99_REPORT.md` and update the plan's checkpoints. Never mark a smoke check passed.
6. Merge, push the tag and delete the branches only on the owner's go-ahead.
