# AGENTS.md - Agent Guide for manual-refresh

Single canonical guide for coding agents in this repository. `CLAUDE.md` (and any future tool-specific file) only points here. What a refresh covers, configuration, usage and return codes: @README.md; the launcher is documented in the header of `manual-refresh.sh`.

## What this repo is

Interactive one-off console (Agent BBB, "Maintenance & tooling"; an untracked folder named `python` until 2026-10-17) that refreshes one entity by hand, beside the always-on `tmdb-crawler` and `wikipedia-crawler` containers, writing to the same `T_WC_*` tables. Only `update_entity.py` and `manual-refresh.sh` are its own.

## Copies, never edited here

Every other module is a **byte-for-byte copy** of a sibling public repo. Fix a bug upstream, then re-copy:

| File | Upstream |
| --- | --- |
| `tmdb_functions.py` | `tmdb-crawler` |
| `wikipedia_functions.py`, `wikipedia_page_writer.py`, `wikipedia_http.py`, `wikipedia_queries.py`, `wikipedia_content_md.py`, `wikipedia_images.py`, `wikipedia_crawler_helpers.py` | `wikipedia-crawler` |
| `citizenphil.py` | identical in both |

Check the copies are in sync (from `%USERPROFILE%/Code/manual-refresh`):

```bash
for f in *.py; do for d in ../tmdb-crawler ../wikipedia-crawler; do [ -f $d/$f ] && (cmp -s $f $d/$f || echo "DIFF $f ($d)"); done; done
```

`wikipedia_functions` needs all seven `wikipedia_*` modules side by side: when upstream adds a module to that import chain, copy it too. The schema DDL lives upstream (`tmdb-crawler/doc/sql`, `wikipedia-crawler/doc/sql`), not here.

## Public repo: what must never enter it

- `.env` and any real credential, host, IP or personal address. `WIKIMEDIA_USER_AGENT` carries a contact address: `.env` only, never as a default in code.
- One-off scripts and unrelated files. Keep a local-only file out with `.git/info/exclude`, not `.gitignore` (which is published and would name it).

## Conventions

- Hungarian notation (`str`, `lng`, `int`, `arr`, `bln` prefixes), public functions prefixed `f_`, as in the upstream crawlers.
- LF line endings everywhere (`.gitattributes`); a CRLF `.sh` fails on the VPS.
- Python 3.12 image; upstream crawlers run 3.10, the copied modules must keep working on both.
- Version: this file's footer. Bump it with every change (global rule `version-bump.md`).
- On the VPS, `~/docker/manual-refresh` is a clone: `git pull --ff-only`, then `./manual-refresh.sh`.

---

**Last Updated**: 2026-10-31
**Current Version**: 1.1.2
