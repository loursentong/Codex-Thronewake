# Help keep the Codex accurate

## Found something wrong?

Open the relevant reference page and choose **Suggest a correction**. The form adds the entity and data revision for you. Explain the change and its evidence, then review and submit the draft on GitHub. A GitHub account is required.

For a general issue, [open a proposal]([URL_DE_VOTRE_LIEN_ICI](https://loursentong.github.io/Codex-Thronewake/next/contribute/)). If you prefer Discord, share the correction with the community thread organizer for relay. Do not publish private reports, player coordinates or account details.

## What happens next?

1. A maintainer checks the claim, source, game version and context.
2. If anything is unclear, they ask for the missing detail.
3. An accepted factual correction enters the reviewed knowledge base before rebuilding.
4. Checks run, the change is reviewed, and the update is published with attribution.

Acceptance and publication are separate steps. Automated checks verify structure and consistency, not whether a player’s assertion is true. Changes retain their source author, proposer, reviewer and version history.

## Editing and review

Experienced contributors may propose a pull request. Do not edit generated HTML to change a statistic. The maintainer workflow and source repository files accompany this release; a broader community ownership transfer has not happened yet.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Thronewake Codex

[![Site](https://img.shields.io/badge/Site-loursentong.github.io-gold?style=flat-square&logo=github)](https://loursentong.github.io/Codex-Thronewake/)
[![Snapshot](https://img.shields.io/badge/Data%20Snapshot-14%20Sep%202026-blue?style=flat-square)](https://loursentong.github.io/Codex-Thronewake/)
[![Format](https://img.shields.io/badge/Format-Standalone%20HTML-green?style=flat-square)](https://loursentong.github.io/Codex-Thronewake/)
[![Tests](https://img.shields.io/badge/Test%20Suite-131%20PASSED-brightgreen?style=flat-square)](https://loursentong.github.io/Codex-Thronewake/)

An interactive encyclopedia and comprehensive knowledge base for **Thronewake**, the persistent browser strategy game.

The Codex is designed as a standalone web application contained in a single HTML file. It works instantly in any modern browser—including offline—without requiring a backend server or installation.

---

## Features

* **Certified Accuracy**: Every statistic, cost, and research time is extracted directly from the official client snapshot dated September 14, 2026.
* **Enhanced Search Engine**:
  * `/` key to focus the search bar.
  * `Esc` key to dismiss search.
  * `↑` button to jump back to the top.
  * Search across buildings, units, technologies, artefacts, and mechanics simultaneously.
* **Explorers & Calculators**:
  * Automated calculation of costs, production times, and resource rates.
  * Comparative filters by faction (*Embermark*, *Verdant*, *Stormfang*, *Ancients*).
* **Polished Interface (V15)**:
  * Responsive layout (Desktop, Tablet, Mobile) with a dedicated print stylesheet.
  * Sticky headers, readable tables, and color-coded costs.

---

## Content Overview

| Domain | Modeled Items | Details |
| :--- | :--- | :--- |
| **Economy** | 39 Buildings & 4 Fields | Levels 1 to 22, City/Capital constraints, production curves. |
| **Military** | 40 Units | Attack, defense (infantry/cavalry), speed, carry capacity, upkeep. |
| **Technologies** | 63 Research Trees | Full upgrade paths for the Smithy and Academy across all factions. |
| **City Guard** | 20 Rangs | Defense milestones and associated costs. |
| **Endgame** | 9 Artefact Types | Scopes (Village/Account), strategic effects, and Ancient Monument mechanics. |

---

## Repository Structure

```text
.
├── codex-thronewake.html    # Final compiled build (single-file HTML)
├── build_codex.py           # Assembly build script
├── POLISH-NOTES.md          # UX/UI polish log and non-regression benchmarks
├── 00_PILOTAGE/             # Project management, master plan, and quality logs
├── tools/                   # Integrity check and comparison tooling
└── tests/                   # Automated integration test suite
