This is a work in progress, still unfinished.

# Contributing (Help Keep the Codex Accurate)

## Found Something Wrong?
Open the relevant reference page and choose **Suggest a correction**. The form automatically adds the entity and data revision for you. Explain the change and its evidence, then review and submit the draft on GitHub (a GitHub account is required).

For a general issue, open a proposal : https://loursentong.github.io/Codex-Thronewake/next/contribute/. If you prefer Discord, share the correction with the community thread organizer for relay. **Do not publish private reports, player coordinates, or account details.**

## What Happens Next?
1. A maintainer checks the claim, source, game version, and context.
2. If anything is unclear, they ask for the missing detail.
3. An accepted factual correction enters the reviewed knowledge base before rebuilding.
4. Automated checks run, the change is reviewed, and the update is published with attribution.

*Acceptance and publication are separate steps. Automated checks verify structure and consistency, not whether a player’s assertion is true. Changes retain their source author, proposer, reviewer, and version history.*

## Editing and Review
Experienced contributors may propose a pull request. **Do not edit generated HTML to change a statistic.** The maintainer workflow and source repository files accompany this release; a broader community ownership transfer has not happened yet.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Thronewake Codex

[![Wiki](https://img.shields.io/badge/Wiki-loursentong.github.io--next-yellow?style=flat-square&logo=github)](https://loursentong.github.io/Codex-Thronewake/next/)

An interactive encyclopedia and comprehensive knowledge base for **Thronewake**, the persistent browser strategy game.

The Codex is engineered as a standalone, zero-dependency web application contained in a single HTML file (`codex-thronewake.html`). It operates instantly in any modern browser—fully functional offline—without requiring installation or a backend server.

---

## Features

* **Verified Game Data**: All statistics, costs, production rates, and research times are extracted directly from the official September 14, 2026 client snapshot.
* **Enhanced Search Engine**:
  * Press `/` to focus search instantly from anywhere on the page.
  * Press `Esc` to clear and exit search.
  * Click the `↑` button to return to the top.
  * Search simultaneously across pages, buildings, resource fields, units, technologies, and factions.
* **Interactive Explorers & Calculators**:
  * Dynamic calculators for building costs, production curves, training times, Smithy upgrades, and Ancient Monument progression.
  * Complete data tables for resource fields (levels 1 to 22) with exact production rates (`/h`).
  * Comparative filters for the 3 playable tribes (*Embermark*, *Verdant*, *Stormfang*) and the *Ancients*.
* **Polished Interface & UX (V15 Pass)**:
  * Fully responsive layout (Desktop, Tablet, Mobile) with a dedicated print stylesheet for clean paper or PDF exports.
  * Capped line length (~74ch) for optimal reading comfort.
  * Sticky headers on long tables, right-aligned tabular figures, zebra striping, and row hover states.
  * Color-coded resource costs for Lumber, Stone, Metal, and Food with explicit visual legends.
  * Full keyboard accessibility (`focus-visible`), screen reader ARIA labels, and OS reduced-motion compliance.

---

## Content Overview

| Domain | Modeled Items | Details |
| :--- | :--- | :--- |
| **Economy** | 39 Buildings & 4 Fields | Levels 1 to 22, Village / Non-capital City / Capital caps, and production curves. |
| **Military** | 40 Units | Attack power, infantry/cavalry defense, speed, carry capacity, and food upkeep. |
| **Technologies** | 63 Research Trees | Full upgrade paths for the Smithy and Academy across all factions. |
| **City Guard** | 20 Ranks | Defense milestones, troop bonuses, and associated costs. |
| **Endgame** | 9 Artefact Types | Scopes (Village/Account), strategic effects, Ancient Villages, and Monument level 100 victory condition. |

---

## Repository Structure

```text
.
├── codex-thronewake.html    # Final compiled deliverable (standalone single HTML file)
├── build_codex.py           # Assembly script compiling modules into single-file HTML
├── POLISH-NOTES.md          # UX/UI polish log, visual hierarchy, and non-regression benchmarks
├── README-v13.md            # Reference documentation for V13 release
├── SHA256SUMS.txt           # Integrity checksums for distribution files
├── 00_PILOTAGE/             # Master plan (PLAN-DIRECTEUR.md), quality state, and audit logs
├── screenshots/             # Reference captures of section palettes and responsive views
├── tools/                   # Integrity check tooling (compare.py, harness.py, polish.py)
└── tests/                   # Automated integration test suite (test_english.py)
```

---

## Usage & Development

### Browsing
* **Online**: [loursentong.github.io/Codex-Thronewake/next/](https://loursentong.github.io/Codex-Thronewake/next/)
* **Offline**: Clone the repository and open `codex-thronewake.html` directly in your browser.

### Building & Quality Assurance
If you modify canonical data or source modules, execute the verification pipeline:

```bash
# Rebuild the single-file HTML deliverable
python build_codex.py

# Execute the automated integration test suite
python tests/test_english.py

# Verify strict data non-regression against baseline
python tools/compare.py
```

---

## License & Disclaimer

Unofficial community project. 
All game values are verified against the official client snapshot dated September 18, 2026.
