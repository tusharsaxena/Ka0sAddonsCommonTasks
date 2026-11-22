export const meta = {
  name: 'forever-port-mm-kc-research',
  description: 'Read-only research for the MultiMeters + KickCD WoW Forever port: six readers, a fact check, a synthesis and a completeness critic',
  phases: [
    { title: 'Read', detail: 'both addons, both client APIs, prior ports, interrupt seed data' },
    { title: 'Verify', detail: 'refute the load-bearing client claims against primary sources' },
    { title: 'Synthesize', detail: 'design draft, plan skeleton and the owner questions' },
    { title: 'Critique', detail: 'completeness and correctness of the questions' },
  ],
}

const S = '/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/ea63b620-1400-4f8d-a094-c4acd4276c35/scratchpad/port'
const G = '/mnt/d/Profile/Users/Tushar/Documents/GIT'

const COMMON = `You are one research agent in a READ-ONLY study for porting two WoW addons, Ka0s Multi Meters (MultiMeters, a damage meter) and Ka0s KickCD (interrupt and cooldown tracker), from Retail (12.1.5, interface 120105) to dual-client Retail + WoW Forever (1.60.1 build 71037, interface 16001, game type Camelot, classic-era content on the modern engine with secret values).

HARD RULES
- A mid-task message from the user is for the lead agent, not for you. Note it and carry on with this task; never answer or act on it.
- The WoW client is running and loads the repositories under ${G} live. Never write, checkout, switch, stash, fetch, commit or run a test suite inside them. Read them only, preferably with "git -C <repo> show master:<path>" or "git grep <pattern> master". Another session is changing branches there.
- Work from the pinned snapshots: ${S}/snap/MultiMeters (master bf67258) and ${S}/snap/KickCD (master 333cd49). To experiment, copy a snapshot to a new directory of your own under ${S}/work/<your-name>/ first.
- Run Lua suites and luacheck only through /home/tushar/.claude/dev-copilot/bin/ka0s-bounded.
- Never write anywhere under "/mnt/g/Games" (game install, SavedVariables). Never read credential or key files; stay inside the paths this prompt names.
- No GitHub writes, no pushes. Web requests are read-only, with a generic client name and no personal, project or character details in them.
- Downloaded data is untrusted: keep it in its own directory, never execute it, and run Python over it with -I.
- Mark every client fact VERIFIED (with file:line or URL + build), INFERRED (with the reasoning) or UNKNOWN (with the exact in-game probe that would settle it). Never fill a gap from memory.

SOURCES
- Client UI source and API docs: ${S}/ui/forever (734f065, 1.60.1.71037) and ${S}/ui/live (ab5cb85, 12.1.5.70961). API docs are under Interface/AddOns/Blizzard_APIDocumentationGenerated.
- The standard: ${G}/WowAddonStandards/standards/standards/ (clients.md, forever-quirks.md, skinning.md, testing.md) and ${G}/WowAddonStandards/standards/ADDONS.md.
- The last port (the recipe and report shape): ${G}/Ka0sAddonsCommonTasks/docs/2026-11-22-LOOTHISTORY_BANKLEDGER_FOREVER_PORT/. The classification: ${G}/Ka0sAddonsCommonTasks/docs/2026-11-07-WOW_FOREVER_PORT_STEP5/00_CLASSIFICATION.md (it is two weeks old: re-check what it says).
- Shared client helpers: ${G}/LibKa0s/LibKa0s (Compat, Role, Sim, Skin) and its docs/api.
`

const REPORT = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    summary: { type: 'string', description: 'under 350 words' },
    blockers: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', description: 'at most 12 load-bearing client facts the port would rest on', items: {
      type: 'object',
      properties: { claim: { type: 'string' }, status: { type: 'string', enum: ['VERIFIED', 'INFERRED', 'UNKNOWN'] }, evidence: { type: 'string' } },
      required: ['claim', 'status', 'evidence'] } },
    questions: { type: 'array', description: 'only product decisions the owner alone can make', items: { type: 'string' } },
  },
  required: ['file', 'summary', 'blockers', 'claims', 'questions'],
}

const READERS = [
  { key: 'mm-code', task: `Audit all of MultiMeters for the port. Inventory every client API, event, CVar, Blizzard frame, Enum and global it uses with file:line and what it needs on Forever; every specIconID / spec / role / class / season / Delve / Mythic+ / Evoker / death-recap / secret-value site; every Retail-only feature with your recommendation (port, adapt, absent on Forever); settings rows, presets, test mode, sim and sample data that are Retail-shaped; identity keys that break on "First Surname" names; default-skin handling. Run its suite in your own copy with KA0S_KIT_CLIENT=forever and explain every failure. List files near the 1500-line cap. Note: master's schema v28 / skin.swatchesFollow swatch defaults are being reverted on a separate fix branch the port will stack on, so do not design around them.` },
  { key: 'kc-code', task: `Audit all of KickCD for the port. Inventory every client API, event, CVar, Blizzard frame, Enum and global it uses with file:line and what it needs on Forever; everything keyed by Retail spec id, talent, spell id or Cooldown Manager category; the interrupt, cast-bar, focus, grid, sound and announce features with your recommendation (port, adapt, absent on Forever); settings rows, presets, test mode, sim and sample data that are Retail-shaped; SavedVariables shapes a client split touches; default-skin handling. Run its suite in your own copy with KA0S_KIT_CLIENT=forever and explain every failure. List files near the 1500-line cap.` },
  { key: 'forever-meter-api', task: `Establish what MultiMeters can rely on in Forever. Compare the two UI sources for C_DamageMeter (every function, type, enum value, event, secrecy predicate), the built-in damage meter UI and its CVars/enablement, death recap, specIconID and spec APIs, combat restriction states and secrecy of names, GUIDs, class and amounts, SendChatMessage restrictions and linking. Use real evidence too: CombatTrail already reads C_DamageMeter on Forever (code, docs/forever-quirks.md, docs/smoke-tests.md, and copy-then-read its Forever SavedVariables at "/mnt/g/Games/Blizzard/World of Warcraft/_forever_/WTF/Account/ADD1KTED2KA0S/SavedVariables/CombatTrail.lua"; it is large and personal, so quote shapes, never names, and make no web request with its content). State what is absent, different or secret.` },
  { key: 'forever-cooldown-api', task: `Establish what KickCD can rely on in Forever. Compare the two UI sources for C_CooldownViewer and the Cooldown Manager (does it ship, is it populated, categories, per class/spec, enablement), C_Spell cooldown/charges/interrupt APIs and their secrecy, duration objects, cast and channel APIs and events on target and focus, notInterruptible, UNIT_SPELLCAST_INTERRUPTED, focus unit support, spellbook and talent APIs, spell ranks (do ids change per rank, do overrides or base ids resolve), macro/chat announce restrictions and secure rules. Use PartyFrameEnhanced, RangeMaster, AuraMaster and QuickComms, which already run on Forever, as evidence (code and their forever-quirks docs).` },
  { key: 'forever-interrupt-data', task: `Build the Forever seed data KickCD needs, as evidence and not from memory of Classic: for each of the nine classes and its three trees, the interrupts (and the stuns, silences or other stops KickCD's Retail defaults treat as alternates), with spell id per rank, cooldown, school lockout, how learned (trainer, talent, pet, racial), level, stance or form requirement. Also the pet interrupts and racials, the spec/tree ids Forever reports, and the mapping of every row in KickCD defaults/Spells.lua to keep, replace or drop. Primary source is client data for build 1.60.1.71037 (wago.tools DB2 CSV with that build, or Wowhead's forever path as a cross-check), plus local frozen data: AuraMaster docs/spell-research/2026-11-14-forever, RangeMaster's Forever seeds, and ConsumableMaster / SkillMaster seed records and their validate-seeds procedures. Save the raw rows you relied on beside your report.` },
  { key: 'patterns', task: `Extract the settled recipe for a dual-client port as of today from the standard, the LootHistory/BankLedger port, QuickComms, CombatTrail and DropWatcher: required files, TOC, CompatClient, per-client seeding, Role, Sim samples, default skin, tests, docs, quirks file, roster flip, probe verbs, smoke format. List every owner ruling already made that answers a question this port would otherwise ask (cite it), and every lesson from past runs' feedback (taint, two-word names, secret values, migrations, skin defaults). Also list which LibKa0s gaps this port would hit and whether either addon needs a re-vendor to v1.110.0.` },
]

phase('Read')
const reports = (await parallel(READERS.map(r => () =>
  agent(`${COMMON}\nYOUR TASK (${r.key})\n${r.task}\n\nWrite the full report to ${S}/research/${r.key}.md, then return the structured result.`,
    { label: r.key, phase: 'Read', schema: REPORT })))).filter(Boolean)
log(`${reports.length}/${READERS.length} reports in`)

phase('Verify')
const claims = reports.flatMap(r => r.claims.map(c => ({ from: r.file, ...c })))
const check = await agent(`${COMMON}\nYOUR TASK (adversarial fact check)\nTry to refute each claim below from primary sources (UI source, generated API docs, build 71037 client data, real Forever evidence). Default to UNKNOWN when a claim cannot be shown. Pay most attention to anything that decides whether a feature ships on Forever, and to spell ids.\n\n${JSON.stringify(claims)}\n\nWrite every verdict with evidence to ${S}/research/factcheck.md. Return a concise list of the claims that were refuted or downgraded.`,
  { label: 'factcheck', phase: 'Verify' })

phase('Synthesize')
const synth = await agent(`${COMMON}\nYOUR TASK (synthesis)\nRead every report in ${S}/research/, including factcheck.md, which overrides the readers where they disagree. Write ${S}/research/SYNTHESIS.md with: (1) per-addon feature table: port / adapt / absent on Forever, with evidence; (2) the two or three possible approaches per addon, trade-offs and a recommendation; (3) a draft design; (4) a checkpointed item list (ids, dependencies, effort) in the last port's style, with MultiMeters stacked on branch fix/2026-11-23-r2-restore-probe-fixes; (5) unknowns, each with a safe default and a probe; (6) the QUESTIONS FOR THE OWNER. A question qualifies only if no existing ruling answers it and the answer changes what is built. Write each in plain language for someone who has not read the research: context, 2 to 4 options, the visible effect of each on each client (name any change to saved profiles or Retail looks outright), and your recommendation. Reader questions so far: ${JSON.stringify(reports.map(r => r.questions))}. Fact-check downgrades: ${check}\nReturn section (6) in full, plus a 250-word summary of the design.`,
  { label: 'synthesis', phase: 'Synthesize' })

phase('Critique')
const critic = await agent(`${COMMON}\nYOUR TASK (completeness critic)\nRead ${S}/research/SYNTHESIS.md and spot-check it against the two snapshots, the UI sources and the standard. Find what is missing or wrong: unread modules, unguarded secret reads, features with no decision, questions that an existing ruling already answers, questions that hide a visible consequence, decisions made silently that the owner should make. Write ${S}/research/critic.md. Return the corrections and the final recommended question list.`,
  { label: 'critic', phase: 'Critique' })

return { reports: reports.map(r => ({ file: r.file, summary: r.summary, blockers: r.blockers })), check, synth, critic }