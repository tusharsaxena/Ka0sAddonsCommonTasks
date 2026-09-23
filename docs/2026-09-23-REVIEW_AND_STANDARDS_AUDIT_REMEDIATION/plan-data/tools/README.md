# Plan generators

Rebuild the plan from the planners' raw output, in this order:

    python3 plan-data/tools/apply_amendments.py <bundle>   # runs build_items.py, then applies reconcile + review fixes
    python3 plan-data/tools/gen_docs.py <bundle>           # items.tsv, 01, 05, plan-data/04_tables.md

Then 04_EXECUTION_PLAN.md = plan-data/04_head.md + plan-data/04_tables.md.
Inputs: plan-data/raw_plan.json (planning workflow), plan-data/docs_workflow_output.json (reconcile + critique).
Do not re-run after execution starts: items.json is then the frozen plan of record.
