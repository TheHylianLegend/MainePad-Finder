### Repo: MainePad-Finder — AI assistant guidance

This file gives concise, actionable guidance to AI coding agents working on the MainePad-Finder repository. Keep changes small and focused; preserve existing SQL and scraping behavior unless asked to restructure.

Summary (big picture)
- This repository stores a small web-scraping prototype and SQL schema/DB procedures for a rental listing matcher called "MainePad-Finder".
- Major areas:
  - Phase2/Web Scraping/: Selenium-based Python scraper prototype (`apartment_finder.py`).
  - Phase2/Schema/ and Phase2/Procedures/: SQL schema files and stored-procedure SQL scripts for the database.
  - Phase1/: research and interview notes (read-only context for product intent).

What an AI agent should know immediately
- The Python scraper is a small, interactive Selenium script that expects the user to input a listing index page URL and uses Firefox WebDriver. It runs headless via `MOZ_HEADLESS=1`.
- The scraper is incomplete and contains placeholders and obvious bugs (undefined variables like `candidates`, `el`, and incomplete parsing logic). Only refactor with testable changes and preserve current UX unless the user requests otherwise.
- SQL files under `Phase2/Schema/` and `Phase2/Procedures/` define the database shape and operations. Treat them as canonical authoritative definitions when implementing or migrating data models.

Key files to reference
- `Phase2/Web Scraping/apartment_finder.py` — primary scraper prototype (examples: finds `a.property-link[href]`, extracts `propertyAddressContainer`).
- `Phase2/Schema/*.sql` — table definitions and indexes. Use these to understand column names and relationships when adding scraping outputs or ETL code.
- `Phase2/Procedures/*.sql` and `Procedures/*.sql` — stored procedures for notifications, messages, reviews. When adding integration tests or wiring, call these as the backend contract.
- `Phase1/` — interviews and notes useful for product intent; prefer non-destructive edits.

Developer workflows and commands
- There is no automated build in the repo. For Python scraping changes, verify locally:
  - Ensure geckodriver and Firefox are installed and compatible with Selenium.
  - Run the script from the `Phase2/Web Scraping/` directory with a Python 3.8+ virtualenv and `selenium` installed.
  - Example (local manual): set MOZ_HEADLESS=1 and run `python apartment_finder.py` then paste a listing page URL when prompted.
- For SQL changes, apply them to a test Postgres/MySQL instance (match the project's DB used by developers). No migration tooling is present — modify SQL files directly and document schema changes.

Project-specific conventions and patterns
- Small, prototype-first code: the scraper is written as an imperative script (global driver instances, interactive input()). When improving, prefer keeping a small CLI wrapper to preserve the existing manual run workflow.
- SQL-as-source: schema and procedures live in plain `.sql` files. Treat these files as the source of truth (edit them instead of creating migrations elsewhere).
- Minimal dependency list: avoid adding heavy frameworks without user approval. Prefer small, focused changes and document added dependencies in a `requirements.txt` placed next to the script.

Integration points and external dependencies
- Scraper: depends on Selenium, Firefox (geckodriver). Network access is required for scraping.
- Database: schema and procedures assume a relational DB. The repo doesn't include connection code — any ETL or ingestion code should add configurable DB credentials (env vars) and be non-destructive by default.

Safe-edit checklist for AI edits
Before making edits, ensure you:
- Read and cite the specific file(s) you plan to change (e.g., `Phase2/Web Scraping/apartment_finder.py`).
- Run the updated script locally (Selenium + Firefox) and report observed behavior or errors.
- When touching SQL files, keep original files intact and add a comment header describing the change.

Concrete examples to follow
- When extracting addresses in `apartment_finder.py`, the script currently locates `.propertyAddressContainer` and cleans lines. Keep that approach but fix undefined refs (example: replace `for xp in candidates` with a defined list of XPaths).
- When adding dependencies, create `Phase2/Web Scraping/requirements.txt` with pinned versions (e.g., selenium==4.x) and document run steps in the file header.

Do NOT do
- Do not delete or reformat SQL schema files without user confirmation.
- Do not switch to a different browser driver (Chrome) unless the user asks — the code and env use Firefox/geckodriver.

If something is missing
- Ask for which DB engine (Postgres/MySQL/SQLite) to target for ingestion and whether to add tests or CI.

If you update this file
- Keep it short (20–50 lines) and focused on actionable, repo-specific guidance. Add one-line references to files you changed.

---
Files referenced: `Phase2/Web Scraping/apartment_finder.py`, `Phase2/Schema/`, `Phase2/Procedures/`, `Phase1/`.
