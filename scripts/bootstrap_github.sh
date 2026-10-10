#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 OWNER/REPO" >&2
  exit 2
fi

REPO="$1"

gh auth status >/dev/null
gh repo view "$REPO" >/dev/null

create_label() {
  gh label create "$1" --color "$2" --description "$3" --repo "$REPO" --force
}

create_label "type:feature" "1d76db" "New behaviour"
create_label "type:bug" "d73a4a" "Something is broken"
create_label "type:docs" "0075ca" "Documentation"
create_label "type:chore" "cfd3d7" "Maintenance"
create_label "type:experiment" "a2eeef" "Experiment or design study"
create_label "type:dataset" "fbca04" "Dataset candidate or change"
create_label "module:A" "0e8a16" "Crop classification"
create_label "module:B" "5319e7" "Health monitoring"
create_label "module:C" "b60205" "Yield prediction"
create_label "module:platform" "006b75" "Shared packages"
create_label "module:infra" "bfd4f2" "CI, tooling, environment"
create_label "priority:high" "b60205" "Do first"
create_label "priority:normal" "fbca04" "Normal"
create_label "priority:low" "c5def5" "Later"
create_label "status:blocked" "e99695" "Waiting on something"
create_label "status:needs-decision" "d4c5f9" "Needs a decision from the maintainer"
create_label "good-first-task" "7057ff" "Small and well defined"
create_label "learning" "bfdadc" "Mainly for learning"
create_label "skip-changelog" "ededed" "Exclude from release notes"

create_milestone() {
  gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null
}

create_milestone "R Research and architecture" "Papers read, notes, hypotheses validated, architecture dossier approved"
create_milestone "M0 Scaffolding" "Repository, CI, docs system, charter, requirements"
create_milestone "M1 Module A pipeline and map" "First dataset, features, models, web map"
create_milestone "M2 Second dataset and Pakistan bridge" "Adapter test, bridge report"
create_milestone "M3 Health monitoring prototype" "Baselines, anomaly score, pipeline, map layer"
create_milestone "M4 Yield prototype or feasibility" "Gate C0 outcome"
create_milestone "M5 Integration and thesis" "End-to-end demo, thesis, defence pack"

gh api "repos/$REPO/rulesets" --method POST --input - <<'JSON'
{
  "name": "protect-main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [ { "context": "ci" } ]
      }
    }
  ]
}
JSON

seed_issue() {
  gh issue create --repo "$REPO" --title "$1" --label "$2" --milestone "$3" --body "$4"
}

seed_issue "Phase R: research plan, design questions and hypothesis register" "type:docs,module:platform" "R Research and architecture" "Acceptance: design_questions.md, hypothesis_register.md, search log and first paper notes exist; dossier outline agreed."
seed_issue "Scaffold repository layout and tooling" "type:chore,module:infra" "M0 Scaffolding" "Requirement: none (foundation). Acceptance: layout from CLAUDE.md exists; pinned environment installs; make check runs; pre-commit works."
seed_issue "Set up CI, CodeQL, Dependabot and labeler" "type:chore,module:infra" "M0 Scaffolding" "Acceptance: ci job named ci is green on a PR; CodeQL runs; Dependabot opens its first PRs."
seed_issue "Write charter, requirements register and ADR template" "type:docs" "M0 Scaffolding" "Acceptance: docs/charter.md, docs/requirements, docs/adr/0000-template.md exist and are linked from README."
seed_issue "Audit first dataset and score it with the rubric" "type:dataset,module:A" "M1 Module A pipeline and map" "Acceptance: audit report, rubric scores, recommendation, ADR draft."
seed_issue "Define label-adapter interface and first adapter" "type:feature,module:A" "M1 Module A pipeline and map" "Requirement: R-A-07."
seed_issue "Imagery pilot: STAC query, masking, per-parcel features for 1000 parcels" "type:feature,module:A" "M1 Module A pipeline and map" "Acceptance: pilot timings and disk growth reported; extrapolated cost approved."
seed_issue "Baseline models with spatial-block validation" "type:experiment,module:A" "M1 Module A pipeline and map" "Requirement: R-A-02."

echo "done"
