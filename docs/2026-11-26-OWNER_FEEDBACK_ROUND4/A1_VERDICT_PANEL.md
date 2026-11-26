# Addendum A1: the verdict panel in the Item Search window (R4-DW-11)

Added during the run; the owner's words are in `inputs/OWNER_FEEDBACK.md` ("Added during the run"). It lands after the build
workflow `wf_9c6b1326-97b`, on the same Drop Watcher branch, because that workflow's Drop Watcher chain is sequential and
already running.

**What it builds.** A section at the bottom of the window's left column, under the Matches list, which shrinks to make room.
- **When it shows.** Only when the current character holds the item shown: bags or bank, with the bank counted from the
  client's cached count (`GetItemCount(id, true)`), so it works with the bank closed. It hides otherwise, and the Matches list
  takes the full height again. It updates on bag changes for the item shown, throttled, never in a hover path.
- **The badge.** The same filled two-part badge as the tooltip (R4-DW-07), from one shared builder: the verdict word with
  its lock and the score.
- **The breakdown.** One line per part that counted, each with its points, in the order the score adds them up:
  - quests, by quest;
  - crafting: known recipes by color, recipes you could learn, other professions, with the cap shown when it was hit;
  - gear;
  - the dampers: easy to buy again, everything gray or done;
  - the poor-quality cap and the quest-item floor when they apply;
  - a total line, then the line the verdict word comes from ("Keep from 50").

  Parts that scored 0 are left out. The confidence tier is not shown (R4-DW-07); a missing input reads as a plain hint, for
  example "Open your profession window to rank recipes".
- **Where the numbers come from.** The verdict code exposes the parts it already computes as a structured breakdown, so the
  panel never computes a score of its own, and the tooltip's reasons and the panel cannot disagree.
- **Space.** The panel has a fixed height for the badge plus up to about 8 lines. More lines scroll inside it. The Matches
  list keeps a minimum of about 5 rows; below that, the panel is the part that scrolls.
- **Tests and docs.** Headless tests cover: shown when held in bags, shown when only in the bank, hidden when not held, the
  breakdown adding up to the score, the caps and dampers listed, and the Matches list height restored. Plus docs and an unrun
  smoke row.

Lead's calls: the panel lives under Matches (the owner's "probably the bottom left"); the bank is counted through the client's
cache; a hit cap is shown; zero parts are hidden.
