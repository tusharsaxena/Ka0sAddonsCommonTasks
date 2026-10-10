# CurseForge journal

A running record of every Ka0s addon's CurseForge page: the files released, their download counts over
time, and the comments, each classified as a bug report, feature request, feedback or general.
`/dev-copilot:wow-curseforge-releases` and `/dev-copilot:wow-curseforge-comments` fill it. Nothing
here is written by hand except the `override` field on a comment.

This is a **living** dataset, not a dated bundle. The frozen-bundle rule does not apply to it.

## Where the data lives, and where it never goes

All journal data is written here, under `journal/curseforge/`, and nowhere else. It is never written into
an addon repo or into `dev-copilot`. The plugin holds the command, the fetch script, the classification
rubric and the schema; this folder holds only data.

## Layout

```
journal/curseforge/
  journal.config.json        roster source, owner, report timezone, schema version
  runs.jsonl                 append-only: one line per run of either command
  <Addon>/                   created by the first run that covers the addon
    project.jsonl            append-only: project totals per releases run
    files.json               keyed by fileId: one record per file
    downloads.jsonl          append-only: per-file download counts per releases run
    comments.json            keyed by commentId: one record per comment or reply
  reports/<YYYYMMDD-HHMMSS>-<releases|comments>.md
                             generated: what changed in that run, named and dated
                             in local time
```

The addon folders are named exactly as the Folder column of `../WowAddonStandards/standards/ADDONS.md`,
which is the roster. The CurseForge project id comes from the `## X-Curse-Project-ID` line in each
addon's TOC. No list of addons or ids is kept here. An addon with no comments has no `comments.json`.

## Sources

- **Releases** come from the CurseForge Core API (`api.curseforge.com`), which needs the owner's API key.
- **Comments** come from the CurseForge site's own endpoint (`www.curseforge.com/api/v1/mods/<id>/comments`).
  It is undocumented and needs no key. It exposes no edit date, which is why `editedAt` below is the
  run that first saw a change.

## Times

Every timestamp in the data files is UTC (`2026-10-10T09:18:02Z`). Every time a person reads is local:
the report titles, release and comment dates, the report file names, and what the commands show in
chat. Local means `timezone` in `journal.config.json` (`Asia/Kolkata`), or the machine's own timezone
when that is unset.

The releases report is one table for the run, with the addons ordered by total downloads. Each addon
has a `Total` row followed by one row per file, newest release first, with the columns Addon, Version,
Release Date, Downloads, and Changes since the previous run. Every report is derived from the journal
alone. Rebuild one with `ka0s-curseforge report-releases <run-ts> all` or `report-comments <run-ts> all`.

## Records

`runs.jsonl`:
`{ts, command, addons:[...], skipped:[...], errors:[{addon, error}], newFiles}` for `releases`, or
`{..., newComments, editedComments, deletedComments}` for `comments`.

`<Addon>/project.jsonl`:
`{ts, projectId, totalDownloads, websiteUrl}`

`<Addon>/files.json` (object keyed by `fileId`):
`{fileId, fileName, displayName, fileDate, releaseType, fileStatus, isAvailable, gameVersions:[...], changelog, changelogCommits, firstSeen, removed}`
- `releaseType` is `release`, `beta` or `alpha`.
- `changelog` is fetched once, when the file is first seen. The packager's changelog is the full
  `git log` since the previous tag, bodies included. That ran to about 200 KB per release, and the
  bodies are already in the addon's public history, so the journal keeps one `- subject (sha7)` line
  per commit, and `changelogCommits` counts them. A hand-written changelog with no commit lines is kept
  as written, up to 4000 characters, and its `changelogCommits` is `null`.
- `removed` is `true` once the file is no longer listed. The record is kept.

`<Addon>/downloads.jsonl`:
`{ts, fileId, downloadCount}`

`<Addon>/comments.json` (object keyed by `commentId`):
`{commentId, parentId, author, authorDisplay, isOwner, postedAt, text, pinned, url, firstSeen, editedAt, deleted, deletedAt, class, confidence, reason, classifiedBy, override, issueRef, issueAt}`

- `parentId` threads replies. `isOwner` marks the owner's own comments, which are never classified, so
  "reported, then answered" can be computed.
- `editedAt` is the run that first saw changed text. An edit clears `class`, so the comment is
  classified again.
- A comment that disappears from the page is kept with `deleted: true` and `deletedAt`. Rows are never
  removed.
- `class` is one of `bug`, `feature`, `feedback` or `general`. `confidence` is 0 to 1, `reason` is one
  line, and `classifiedBy` says who classified it.
- `override` is the owner's correction and the only field edited by hand. When it is set, it wins, and a
  run never reclassifies the comment.
- `issueRef` is either the GitHub issue filed from the comment (`owner/repo#n`) or `declined`. Once set,
  the comment is never offered for filing again. `issueAt` is when it was set.

## Rules

- Append-only files are only ever appended to. Keyed files are rewritten with their keys sorted, so a
  run's diff shows exactly what changed.
- One run is one commit, made directly on the default branch, with the subject
  `curseforge: <releases|comments> run <ts>: <summary>`. Journal runs are data and do not use a
  feature branch.
- `*.db` files are local query caches, rebuilt from these files and never committed.
- A schema change bumps `schemaVersion` in `journal.config.json` and is described here.
