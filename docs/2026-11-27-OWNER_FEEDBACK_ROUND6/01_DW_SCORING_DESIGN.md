# Drop Watcher: a 0-100 verdict score that means "how sure" (design for owner approval, 2026-11-27)

The owner (image 45, Liferoot "Auction 0"): "Why is the score for this 0? If Auction i would have expected this to be
higher. Rework the scoring system so that it ends up being a normalized score from 0-100; higher is more confident;
should work across all verdicts (keep, toss, vendor, auction, etc). Before you build anything, design this scoring
system and show it to me."

## Why Liferoot reads 0 today

Today's number is a **use value**: how useful the item still is to this character. Liferoot's parts are +15 (other
professions use it), -6 (that part's cap), -20 (easy to buy again), -15 (every use is gray or done) = -26, clamped to 0.
A use value under 20 is exactly what makes it a disposal verdict (Auction, Vendor, Toss), so every disposal badge
shows a low number however clear the call is. The number answers "keep it?", while the word answers "what do I do
with it?".

## The design

Two numbers, with only one shown on the badge.

1. **Use value U** (unchanged parts, internal): the same parts as today (quests, recipes, gear, collection, dampers,
   poor cap, quest floor), summed *without* the 0-100 clamp. U picks the word, as today: Keep at 50+, Hold at 20-49,
   and under 20 a disposal (Auction / Vendor / Toss, by money).
2. **Score S, 0-100 (shown):** how sure Drop Watcher is of *the word it shows*.

   **S = round(100 x E x D)**

   - **D, data known (0-1):** today's confidence weights unchanged (ForeverDB loaded, quest states, profession
     ranks, item info, gear verdict, ForeverDB knows the item), as a fraction.
   - **E, evidence for the word (0.5-1, or 0.25):** how clearly the facts point at this word and not its neighbor.
     A call right on a boundary is 0.5; a clear call is 1.

   | Word | E |
   |---|---|
   | Keep | 0.5 + 0.5 x min(1, (U - 50) / 50): U 50 is 0.5, U 100 or more is 1 |
   | Hold (in its band) | 0.5 + 0.5 x (distance to the nearer edge, 20 or 50) / 15: edges 0.5, U 35 is 1 |
   | Hold (fallback: price unknown, gear still scoring, too little data to say Toss) | 0.25 |
   | Auction / Vendor / Toss | 0.5 + 0.5 x min(u, m) |

   **u, use part:** min(1, (20 - U) / 20), so U 0 or below is 1 and U 19 is 0.05.

   **m, money part** (r = net auction per unit / vendor price, X = the margin setting, default 10%):

   | Word | m |
   |---|---|
   | Auction | min(1, r - (1 + X)): beating vendor by X is 0; by X + 100% or more is 1. No vendor price: 1 |
   | Vendor, auction price known | min(1, ((1 + X) - r) / (1 + X)): a near tie is ~0; auction worth nothing is 1 |
   | Vendor, bound (can't be auctioned) | 1 |
   | Vendor, Auctionator loaded but no price for it | 0.8 |
   | Vendor, Auctionator absent or comparison off | 0.6 |
   | Toss (no vendor, no auction price), Auctionator loaded | 0.8 |
   | Toss, Auctionator absent | 0.6 |
   | Toss, bound and no vendor | 1 |

   Kept rules: under 50% data never says Toss (it holds, E 0.25); gear still scoring holds. Toss becomes Auction when an
   auction price exists (owner, 2026-11-27).

## Worked examples (D = 1 unless said)

| Item | Facts | Word | S |
|---|---|---|---|
| Liferoot (image 45) | U -26; vendor 75c; auction 3s 18c; 8h deposit 15c; net 287c, r 3.83 | Auction | 100 |
| Ruined Leather Scraps (image 44) | U -15; vendor 7c; auction 34c; deposit 5c (1s over a stack of 20); net 27c, r 3.9 | Auction | 100 |
| A gray item, Auctionator absent | U 0, vendor 20c | Vendor | 80 |
| Same, near tie on the auction house | U 0, r 1.05 (needs 1.10) | Vendor | 52 |
| Recipe reagent, yellow skill-up | U 35 | Hold | 100 |
| Quest item, one quest in log | U 60, D 0.9 | Keep | 50 |
| Gear upgrade + quest | U 130 | Keep | 100 |
| Item info still loading | price unknown, D 0.6 | Hold (fallback) | 15 |

## What the player sees

- Badge: "Auction 100", "Keep 50", "Hold 15" — always "how sure".
- Verdict panel, two sections:
  - **Why this word:** the use value's parts as today (+15, -20 ...), ending "Use value -26 (Auction, Vendor or Toss
    under 20)".
  - **How sure:** "Use value well under 20: 100%", "Auction beats vendor by 283% (needs 10%): 100%",
    "Data known: 100%", "Score 100".
- (?) help: the two numbers explained the same way, with the live margin, cut and duration.
- The tier word stays hidden, and the "under 80% a hint says what's missing" rule stays.

## Open for the owner

1. Is "Auction 100" for Liferoot what you expect, or should money margins cap lower (e.g. a full 1 only at 3x vendor)?
2. Should the Hold fallback show its low score (e.g. "Hold 15"), or show no number ("Hold ?")?
3. Ranking in Item Search's Matches/"Best for you" sort keys on the use value today; keep it on U (recommended), since
   S says how sure, not how valuable.
