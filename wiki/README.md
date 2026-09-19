# Codex Thronewake — first production slice

Dark-first Hugo reference with Pagefind search. Nine connected entities: Raider,
War Ram, Skullthrower, Stormfang Clans, Workshop, Academy, Town Hall, Barracks and
Rally Point. This is not the full wiki or completed community handoff.

## Build in a clean checkout

Requires Python 3.11+ and Windows/Linux x64. No AI service, private TW folder, npm,
database or global installation is needed to rebuild the checked-in public bundle.

```text
python -B scripts/bootstrap.py
python -B tests/test_release.py
python -B scripts/build.py --out artifacts/release-1
python -B scripts/serve.py artifacts/release-1
```

Open `http://127.0.0.1:8766/Codex-Thronewake/next/`. Build dependencies are downloaded
from official release/registry URLs and checked against pinned SHA-256/SHA-512 values.
Hugo 0.166.0 and Pagefind 1.5.2 are pinned in `toolchain.json`. No dependency install
script is executed. A build requires a **new** artifact directory and stops on errors.

The reference release and its comparison CI use Windows x64. Linux also builds
successfully with the pinned tools and passes the data tests, but the official
Pagefind platform packages embed different UI/WASM bytes and can serialize the
index differently. Cross-platform byte identity is not promised. Do not replace
the checked public artifact with a Linux build without its own browser review.

The Pagefind Default UI is explicitly supported by 1.5.2 and used here with dark
tokens and tested filters. Its newer Component UI remains an optional later change,
not a prerequisite or a second search engine.

## Where to work

```text
knowledge/        Reviewed public bundle and integrity manifest
content/          Authored scope, contribution and source explanations
layouts/          Hugo page templates and shared partials
static/           Dark CSS, small interactions and credited game artwork
scripts/          Verified setup, import, generation and recursive checking
tests/            Positive/negative data tests and browser interactions
generated/        Derived Hugo input — never edit facts here
artifacts/        New immutable build outputs; serve only one checked output
```

The data bundle is a bounded projection of P4 `tw-public-reference-v3`. It preserves
original evidence objects, values, IDs, qualifiers and prerequisites. Display names
are official English labels, not title-cased technical keys. The generated per-entity
JSON lets clients consume data without parsing HTML.

### Correcting a fact

Until the agreed community handoff, the reviewed TW knowledge base remains the
authority. A maintainer accepts the evidence, updates it there, verifies a new P4
export, reviews the importer pin, and re-imports the bounded bundle. Do not change
`bundle.json` and simply reseal its hash as a substitute for fact review. The public
manifest checks integrity; private source replay is an additional, different check.

```text
python -B scripts/import_tw.py <approved-P4-data.json> --tw <private-TW-root>
```

The original P4 release is pinned. A new upstream digest deliberately stops the
import until reviewed. Ordinary prose/style contributions do not require TW.

## Contribution entry point

`Suggest a correction` captures entity, revision and section, then prepares a real
GitHub issue draft. The player reviews/submits there under their GitHub identity.
There is no browser token, automatic issue submission or automatic approval. The
no-JavaScript fallback explains the same workflow. A full approval-to-data automation
and formal community ownership transfer remain future work; acceptance is not deployment.

## Checks and publishing

- Source contract, known values, typed prerequisite targets and negative cases.
- Hugo build errors/warnings stop the build; Pagefind failures are not swallowed.
- Generated manifest, recursive links/anchors and repository base-path checks.
- Rebuild comparison: exact HTML, JSON, scripts, artwork and search content.
  Pagefind 1.5.2 varies filter-value serialization order. The checker normalizes
  only that order and dependent metadata hashes; membership, index and fragments
  still must match. Outputs are not claimed byte-identical. Unknown formats fail.
- Browser tests: real search, responsive widths, dark search styling, disclosure
  deep links, form escaping, keyboard focus and no-JavaScript fallback.
- Public content only: no account data, private paths or original private captures.

Browser checks require Node, Playwright and Microsoft Edge. Set `PLAYWRIGHT_MODULE`
when using a nonstandard install; `TW_BASE` can test another served artifact.
Run `node tests/browser.cjs` against the loopback server. Tests never submit an issue.

Publish only the checked artifact beneath `/Codex-Thronewake/next/`, leaving the
existing root wiki intact. Recheck the remote commit before writing. Retain the
source and artifact hashes together. Rollback is a new revert commit restoring the
previous artifact, not a force push. A local build is not proof of successful hosting.
The publishing receipt records what was actually deployed and checked.

## Credits and limits

Game artwork: Thronewake / Wynfir, supplied through the Thronewake Compendium.
Project-owner confirmation of reuse with credits: 19 September 2026. File hashes and
provenance: `ASSETS.json`. No upstream source code was copied into these new templates.
Sources: [Hugo](https://gohugo.io/installation/windows/),
[Pagefind](https://pagefind.app/docs/ui-usage/).

This README describes this implemented slice; it does not certify the entire future
P5/P6 wiki, moderation system or in-game integration. All nine entities remain bounded
by their snapshot/version context and separately qualified later rules.
