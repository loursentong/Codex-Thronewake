# Contributing to this first slice

Players: use **Suggest a correction** on a reference page, or open a GitHub issue.
Include the observation/source, game version and conditions. Do not attach private
reports or account information. Your GitHub identity attributes your proposal.

Maintainers:

1. Read the exact claim; distinguish developer confirmation, catalogue values,
   player experience and inference. Ask for missing context rather than guessing.
2. Record acceptance/rejection and reasons in the issue. Do not equate acceptance
   with successful publication. Do not infer a developer endorsement from a reaction.
3. For a fact correction, update the reviewed TW base and importer pin first;
   preserve source attribution and regenerate the bundle. Formal community ownership
   of public knowledge has not yet transferred. See README.
4. For prose/style changes, edit `content/`, `layouts/` or `static/`. Never patch a
   generated table in `next/` as an alternative factual authority.
5. Run the tests and build. Include regenerated `next/` and the source change in
   the same pull request. The CI comparison detects stale generated content.
6. Review the rendered change, evidence, public boundaries and credits. Merge after
   successful checks and verify the served page. Link issue, PR and deployment.

Record proposer, evidence author and reviewer in the discussion/commit; they need
not be the same person. Until dedicated roles are agreed, no duty is assigned to
Wynfir merely because he develops the game. No automatic content approval is present.

Rollback: revert the deployment commit in a new commit and verify Pages. Do not
force-push or silently rewrite history. The old root wiki is preserved separately.
