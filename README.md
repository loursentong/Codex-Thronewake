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

[![Wiki](https://img.shields.io/badge/Wiki-loursentong.github.io-yellow?style=flat-square&logo=github)](https://loursentong.github.io/Codex-Thronewake/)

An interactive encyclopedia and comprehensive knowledge base for **Thronewake**, the persistent browser strategy game.

The Codex is designed as a standalone web application contained in a single HTML file. It works instantly in any modern browser—including offline—without requiring a backend server or installation.

---

## Features

* **Verified Game Data**: All statistics, costs, production rates, and research times are extracted directly from the September 14, 2026 client snapshot.
* **Enhanced Search Engine**:
  * Press `/` to focus search instantly from anywhere on the page.
  * Press `Esc` to close search.
  * Click the `↑` button to return to the top.
  * Search simultaneously across pages, buildings, resource fields, units, technologies, and factions.
* **Interactive Explorers & Calculators**:
  * Interactive data tables for resource costs, production curves, and training times.
  * Filters for the 3 playable tribes (*Embermark*, *Verdant*, *Stormfang*) and the *Ancients*.
* **Polished Interface (V15 Pass)**:
  * Fully responsive design (Desktop, Tablet, Mobile) with an optimized print stylesheet.
  * Sticky table headers, color-coded resource costs, accessible contrast, and distinct color accents per section.

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
