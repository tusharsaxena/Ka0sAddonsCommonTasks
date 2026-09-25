# Plan generators

Rebuild the plan from the planners' raw output, in this order:

    python3 plan-data/tools/apply_amendments.py <bundle>   # runs build_items.py, then applies reconcile + review fixes
    python3 plan-data/tools/gen_docs.py <bundle>           # items.tsv, 01, 05, plan-data/04_tables.md

Then 04_EXECUTION_PLAN.md = plan-data/04_head.md + plan-data/04_tables.md.
Inputs: plan-data/raw_plan.json (planning workflow), plan-data/docs_workflow_output.json (reconcile + critique).
Do not re-run after execution starts: items.json is then the frozen plan of record.

## Executing a milestone

`execute_milestone.js` is the Workflow script that runs a milestone. Pass `args.items` = the milestone's
`[{id, repo, deps}]` (from items.json). It schedules by dependency, one item at a time per repo and
repos in parallel. For each item it runs implement (test-first, commit "<ID>: …"), then an independent
review, then one fix round if the review finds problems. An item already landed in git is detected and
skipped, so a re-run after an interruption is safe. Check progress with ../../resume-state.sh.
