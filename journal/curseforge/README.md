# CurseForge journal

A running record of every Ka0s addon's CurseForge page: the files released, their download counts over
time, and the comments, each classified as a bug report, feature request, feedback or general. A
dev-copilot command fills it. Nothing here is written by hand except the `override` field on a comment.

This is a **living** dataset, not a dated bundle. The frozen-bundle rule does not apply to it.

## Where the data lives, and where it never goes

All journal data is written here, under `journal/curseforge/`, and nowhere else. It is never written into
an addon repo or into `dev-copilot`. The plugin holds the command, the fetch script, the classification
rubric and the schema; this folder holds only data.

## Layout

```
journal/curseforge/
  journal.config.json        roster source, project-id source, owner, schema version
  runs.jsonl                 append-only: one line per run
  <Addon>/                   created by the first run that covers the addon
    project.jsonl            append-only: project totals per run
    files.json               keyed by fileId: written once per file
    downloads.jsonl          append-only: per-file download counts per run
    comments.json            keyed by commentId, rewritten sorted on every run
  reports/<YYYY-MM-DD>.md    generated: what changed since the previous run
```

The addon folders are named exactly as in `../WowAddonStandards/standards/ADDONS.md`, which is the
roster. The CurseForge project id comes from the `## X-Curse-Project-ID` line in each addon's TOC. No
list of addons or ids is kept here.

## Records

`runs.jsonl`:
`{ts, schemaVersion, addons:[...], filesSource:"api", commentsSource:"browser", newFiles, newComments, editedComments, deletedComments, issuesFiled, errors:[...]}`

`<Addon>/project.jsonl`:
`{ts, projectId, totalDownloads}`

`<Addon>/files.json` (object keyed by `fileId`):
`{fileId, displayName, fileName, releaseType, fileDate, gameVersions:[...], changelog}`. `changelog` is
markdown converted from the API's HTML.

`<Addon>/downloads.jsonl`:
`{ts, fileId, downloadCount}`

`<Addon>/comments.json` (object keyed by `commentId`):
`{commentId, parentId, author, isOwner, postedAt, editedAt, text, firstSeen, lastSeen, deleted, class, confidence, reason, classifiedBy, override, issueRef}`

- `class` is one of `bug`, `feature`, `feedback` or `general`. `confidence` is 0 to 1, and `reason` is
  one line.
- `override` is the owner's correction. When it is set, it wins, and a run never reclassifies the comment.
- `issueRef` is the GitHub issue filed from the comment (`<repo>#<n>`). When it is set, the comment is
  never offered for filing again.
- A comment that disappears from the page is kept and gets `deleted: true`. Rows are never removed.
- `parentId` threads replies, and `isOwner` marks the owner's own comments, so "reported, then answered"
  can be computed.

## Rules

- Append-only files are only ever appended to. Keyed files are rewritten with their keys sorted, so a
  run's diff shows exactly what changed.
- One run is one commit, made directly on the default branch, with the subject
  `curseforge: run <ts>: <n> new comments, <m> new files`. Journal runs are data and do not use a
  feature branch.
- `*.db` files are local query caches, rebuilt from these files and never committed.
- A schema change bumps `schemaVersion` in `journal.config.json` and is described here.
