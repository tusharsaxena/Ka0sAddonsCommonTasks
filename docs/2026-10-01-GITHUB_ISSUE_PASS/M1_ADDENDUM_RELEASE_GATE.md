# M1 addendum: the release gate and the band (decided during execution, 2026-10-01)

The plan is frozen. This file records two decisions taken after M1's first pass, and the extra commits
they produce. The orchestrator took both decisions on the owner's standing instruction to use best judgement.

## A1. Lizard's length warning is not a complexity finding

**What happened.** GI-LK-12's release run (LibKa0s `996c5c4`) refused v1.66.0 with `suites.complexity.warnings
= 2`. Neither warning is a CCN finding. Both are lizard's default function-length warning (> 1000 lines), on
`lib.__AttachIdList` (OptionsIdList.lua, 1165 lines, CCN 1) and `lib.__AttachWidgets` (OptionsWidgets.lua,
1040 lines, CCN 6). Each is a closure that wraps its whole file. The raw run was blind to both. The sighted
shadow (kit 35) lists them for the first time.

**Decision.** The kit runner passes lizard `-L 1500`, so the function-length threshold equals the
layout-§1 file cap. A function cannot be longer than its file, so length stays governed by layout-§1
alone and the complexity suite's warnings mean CCN > 15 and nothing else. Standard v2.74.0 says so in
automated-tests-§3.

**Rejected.** Splitting the two attach closures: it changes two core Options files that all eleven addons
vendor, for a metric that duplicates the file cap. Gating on `maxCcn` instead of `warnings`: it would mean
changing the plugin, the standard and every recorded bundle's reading of the field.

**Commits.** `GI-LK-10R:` (runner + kit doc + test), `GI-STD-01R:` (standard text), then GI-LK-12 completes
with a passing release run and the local tag.

## A2. This cycle adds no file to the 1000–1500 band

**What happened.** LibKa0s#7's requirement (Perf.lua out of the band) was not met by the command-surface peel
alone. After GI-LK-07/08/09, Perf.lua is 1307 lines. Separately, GI-LK-03 pushed Slash.lua from 999 to 1030,
into the band.

**Decision.** Both get a further peel in this cycle. For Perf, the sampler goes to a paired secondary file,
the seam the issue originally named. For Slash, the parser block goes to a paired secondary file. Each stays
in its existing major and gets a paired minor, a `LibKa0s.xml` row, a `tests/majors.lua` row and a
load-without stub test. The commits are `GI-LK-07R:` and `GI-LK-03R:`. The payload grows to 32 files, and
GI-STD-01R recounts it.
