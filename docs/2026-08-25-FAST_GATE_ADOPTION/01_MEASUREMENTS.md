# Fast-gate adoption — what the nine gates cost, before and after

Measured 2026-08-25 across every addon in
[`ADDONS.md`](../../../WowAddonStandards/standards/ADDONS.md), against
[`testing-§14`](../../../WowAddonStandards/standards/standards/testing.md).

**All nine runs were taken serially, one repo at a time, on an otherwise idle machine.** These
suites are I/O-bound rather than busy, so measuring several at once would have inflated every
figure. Nothing here was timed while anything else was running.

## The premise had already moved

The adoption prompt asks each repo to re-vendor from **LibKa0s v1.14.0 / kit revision 12**. Every
one of the nine was already there and past it: LibKa0s is tagged **v1.15.0**, each addon's
`CLAUDE.md` provenance line already names v1.15.0, and both vendored payloads match that tag
exactly. The only content difference against the library's working tree is a four-line comment
added to `LibKa0s/DebugLog.lua` *after* the tag, which the payload gate correctly ignores because it
compares against the tag the provenance line names.

So step 2 was already done, collection-wide, by the further-modules bundle. What had **not** been
done for the eight non-Multi-Meters repos was the rest of the prompt: measuring the result,
deciding `--jobs` deliberately, and recording any of it. That is what this bundle is.

The consequence for the "before" column: it is quoted from the adoption prompt's own table, not
re-measured here, because re-vendoring had already happened and there was no second chance to take
it. The "after" column is measured. Where the two case counts differ, the repo genuinely gained
cases between the two readings — that drift is shown rather than hidden.

## Wall clock and CPU

| Addon | Before (prompt) | After (measured) | CPU | Cases before → after |
|---|---|---|---|---|
| Ka0s Consumable Master | 77.9s | **3.85s** | 23% | 693 → 698 |
| Ka0s KickCD | 50.7s | **5.66s** | 29% | 774 → 780 |
| Ka0s Multi Meters | 130.8s → 7.26s at v1.14.0 | **6.34s** | 36% | 1,246 → 1,257 |
| Ka0s Panel Master | 11.0s | **3.64s** | 18% | 729 → 731 |
| Ka0s Bank Ledger | 10.7s | **3.35s** | 18% | 775 → 791 |
| Ka0s Loot History | 9.8s | **3.14s** | 16% | 621 → 644 |
| Ka0s Absorb Tracker | 9.4s | **4.17s** | 18% | 506 → 508 |
| Ka0s Pretty Chat | 8.9s | **3.12s** | 17% | 270 → 271 |
| Ka0s WhatGroup | 7.5s | **3.19s** | 19% | 477 → 485 |

Every suite is green: nine repos, **6,199 passing cases, 0 failed**, `luacheck` 0/0 in all nine.

CPU stays low across the board because these gates are still dominated by waiting, not computing —
but the waiting that is left is a few seconds, not two minutes.

## Where the time actually went — the syscall counts

Counted with the shim from the adoption prompt, extended to count `io.open` and `os.execute` as
well. This is the half that cannot be read off the suites, and it is the half that decides which
of the two kit fixes paid in which repo.

| Addon | `loadfile` | `popen` | `io.open` |
|---|---:|---:|---:|
| Ka0s Absorb Tracker | 583 | 19 | 438 |
| Ka0s Panel Master | 119 | 10 | 655 |
| Ka0s Consumable Master | 99 | 10 | 586 |
| Ka0s Multi Meters | 61 | 11 | 1,232 |
| Ka0s Pretty Chat | 58 | 9 | 347 |
| Ka0s KickCD | 49 | 23 | 890 |
| Ka0s Bank Ledger | 41 | 10 | 402 |
| Ka0s Loot History | 41 | 10 | 378 |
| Ka0s WhatGroup | 29 | 9 | 328 |

**`popen` is now single digits to low twenties everywhere, against the ~150 the prompt describes.**
That is the batched blob read in `vendor_sync.lua`, and it is the fix that paid in all nine repos,
because all nine run the vendored-payload gate. WhatGroup is the cleanest confirmation: the prompt
recorded `loadfile=24 popen=147 cpu=0.31s` inside a 7.5s wall clock; it now reads `loadfile=29
popen=9 cpu=0.27s` inside 3.19s. Same trivial CPU, same trivial `loadfile`, 138 fewer processes,
and the wall clock more than halved.

### Two repos never touch the chunk cache at all

`Ka0s Pretty Chat` and `Ka0s WhatGroup` make **zero** calls to the kit's `Loader.load` /
`loadAll` / `loadSource`. Both keep their own `tests/loader.lua`, which compiles chunks through
`loadfile` directly and caches them itself, because each instance needs its own `_G` and the kit
has no mode for that. Kit revision 12's chunk cache is therefore **inert** in those two repos:
their entire improvement is the batched blob reads.

This matters for how it gets written down. Crediting the cache in those two repos' docs would be
crediting a code path they never execute — the mistake the prompt warns about in the other
direction. The other seven do route source loading through the kit loader and do get both fixes.

## The one repo where the kit was not the problem

Ka0s Consumable Master came out of the re-vendor at **25.59s** — an improvement on 77.9s, but four
times slower than any of its siblings and well over the 10-second line. Reading the suites would
have said "more tests"; reading the profile said something else entirely:

```
loadfile=99  popen=10  io.open=28768  cpu=3.49s
```

Twenty-eight thousand file opens, against 328–1,232 in every other repo, and 3.5 seconds of CPU
inside a 25.6-second wall clock. The cause was that repo's own `resolve()` in `tests/run.lua` — a
helper that tolerates either the flat or the `core/`-and-`modules/` layout by probing up to five
candidate paths with `io.open` until one answers. It re-ran that probe for every file, on every
build, several hundred times over. On a WSL2 `/mnt` checkout each probe crosses a 9p mount.

A source file cannot move while the runner is running, so the answer is a constant for the life of
the process. Memoising it — caching the resolved **path**, changing nothing about how chunks are
read, compiled or run, so isolation is untouched — gives:

| | Wall | CPU | `io.open` | Cases |
|---|---|---|---|---|
| After the re-vendor | 25.59s | 15% | 28,768 | 698 |
| After memoising `resolve()` | **3.85s** | 23% | **586** | 698 |

Same 698 cases, `luacheck` still 0/0. This is `testing-§14`'s first rule — do not re-do work the
process has already done — applied one level out from the kit, in the per-addon file the kit
cannot reach. It is also the prompt's own point holding twice over: **grepping for the idiom lied,
and counting the calls did not.** The second-highest `io.open` count in the collection is Multi
Meters' 1,232, which costs nothing worth chasing.

## `--jobs`: declined, in all nine

`testing-§14` says to switch sharding on once a repo's serial gate exceeds **roughly 10 seconds**,
and to exhaust the other two rules first. After the work above, the slowest gate in the collection
is Multi Meters at 6.34s and the median is 3.6s. Every repo is comfortably under the line, so
`--jobs` stays off in all nine and no `Kit.run{ ... jobs = "auto" }` was added anywhere.

This is the rule being followed, not a corner being cut. Consumable Master is the case that shows
why the order matters: sharded eight ways, its 25.59s would have come down to something respectable
while the 28,768 redundant file opens sat there untouched, and the repo would have looked fixed.

## Correction: the "before" column flatters this, and the repos' own records say so

The table above compares against the adoption prompt's figures. Those were taken on a state none of
these repos can evidence from the inside, and taking them at face value tells a nicer story than the
evidence supports. Each repo's **own** last recorded run, from its `docs/automated-tests/`
manifests, gives a second comparison — and for most of the collection it points the other way.

`tests`-suite duration and vendored-payload size, previous recorded run against today's:

| Addon | Previous run | Then | Payload | Now | Payload |
|---|---|---|---|---|---|
| Ka0s Consumable Master | `20260807-114612` | 72.78s / 675 | 54 files | **3.87s** / 698 | 182 files |
| Ka0s KickCD | `20260807-114618` | 45.20s / 756 | 68 | **5.66s** / 780 | 196 |
| Ka0s Multi Meters | `20260825-021705` | 8.25s / 1,246 | 194 | **6.50s** / 1,257 | 197 |
| Ka0s Bank Ledger | `20260807-115101` | 2.45s / 727 | 52 | 3.49s / 791 | 180 |
| Ka0s Panel Master | `20260807-160022` | 2.80s / 717 | 66 | 3.66s / 731 | 194 |
| Ka0s Loot History | `20260807-114650` | 2.07s / 594 | 52 | 3.23s / 644 | 180 |
| Ka0s WhatGroup | `20260807-121935` | 1.45s / 462 | 49 | 3.11s / 485 | 177 |
| Ka0s Pretty Chat | `20260807-114404` | 1.36s / 260 | 43 | 3.21s / 271 | 171 |
| Ka0s Absorb Tracker | — | no comparable prior run | | 4.21s / 508 | 199 |

**Five of the nine are slower than they were in August**, and the reason is in the last column: the
vendored payload grew from roughly 50 files to roughly 180 as `LibKa0s-Media-1.0` and its icon set
were adopted across the collection. Pretty Chat vendored **zero** icons at `836beb5` and vendors
**114** now. The payload gate verifies every file in the payload against the tag, so the work it
does grew with it.

So the batch did not make every gate faster than it has ever been. What it did was **make the
payload gate affordable at the size the payload has now reached**. The two readings are both true
and they answer different questions:

- Against the same tree with unbatched reads — the prompt's column — today is much faster, and
  WhatGroup measures that directly: `popen` 147 to 9 across a 177-file payload.
- Against each repo's own August record, the five small suites gave back some of that to payload
  growth, and the two that had drifted to 45s and 73s came down by an order of magnitude.

None of this changes a decision made here. Every gate is still well under the ten-second line, so
`--jobs` stays off either way, and Consumable Master's `resolve()` finding stands on measurements
taken minutes apart on one tree. It changes what may honestly be claimed: **the fast gate stopped
the payload growth from being felt, rather than making every suite faster than it used to be.**

The figure worth watching is that ~3.1s floor the five small suites have converged on. It is not
their cases — WhatGroup burns 0.27s of CPU to produce it. It is the payload gate, and it will grow
again the next time the payload does.
