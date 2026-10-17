# AGENTS.md - Agent Guide for manual-refresh

Single canonical guide for coding agents in this repository. `CLAUDE.md` (and any future tool-specific file) only points here. Human-facing usage is in @README.md.

## What this repo is

`manual-refresh` is a small interactive console to refresh **one entity by hand**: a TMDb movie, series or person by its TMDb id, then its Wikipedia pages through its Wikidata Qid; or a list of Qids for one Wikipedia content family. It runs as a one-off Docker container beside the always-on `tmdb-crawler` and `wikipedia-crawler` containers, and writes to the same `T_WC_*` tables.

It belongs to the **Agent BBB** ecosystem (github.com/vaugouin), stage "Maintenance & tooling". Until 2026-10-17 it was an untracked folder named `python`.

## Copies, never edited here

Every module except `update_entity.py` is a **byte-for-byte copy** of a sibling public repo. Fix a bug upstream, then re-copy:

| File | Upstream |
| --- | --- |
| `tmdb_functions.py` | `tmdb-crawler` |
| `wikipedia_functions.py`, `wikipedia_page_writer.py`, `wikipedia_http.py`, `wikipedia_queries.py`, `wikipedia_content_md.py`, `wikipedia_images.py`, `wikipedia_crawler_helpers.py` | `wikipedia-crawler` |
| `citizenphil.py` | identical in both |

Check the copies are in sync (from `%USERPROFILE%/Code/manual-refresh`):

```bash
for f in *.py; do for d in ../tmdb-crawler ../wikipedia-crawler; do [ -f $d/$f ] && (cmp -s $f $d/$f || echo "DIFF $f ($d)"); done; done
```

`wikipedia_functions` needs all seven `wikipedia_*` modules side by side. When upstream adds a module to that import chain, copy it too. The schema DDL lives upstream (`tmdb-crawler/doc/sql`, `wikipedia-crawler/doc/sql`), not here.

## Own files

- `update_entity.py`: `f_updatemovie`, `f_updateserie`, `f_updateperson` (TMDb "everything" call, then Wikipedia through `ID_WIKIDATA`) and `f_updateqids` (Wikipedia only). Return `{"tmdb": code, "wikipedia": summary}`, code `1` OK, `0` gone, `-1` transient error. `blnforce=True` first clears an id recorded in `T_WC_TMDB_ID_NOT_FOUND`.
- `manual-refresh.sh`: builds the image and opens a Python REPL with the folder mounted on `/app` (a pulled file is live without rebuild), env from `/home/debian/docker/manual-refresh/.env`, `/shared` mounted.

## Public repo: what must never enter it

- `.env` and any real credential, host, IP or personal address. `WIKIMEDIA_USER_AGENT` carries a contact address: it lives in `.env` only, never as a default in code.
- One-off scripts and unrelated files. Keep a local-only file out with `.git/info/exclude`, not `.gitignore` (which is published and would name it).

## Conventions

- Hungarian notation (`str`, `lng`, `int`, `arr`, `bln` prefixes), public functions prefixed `f_`, as in the upstream crawlers.
- LF line endings everywhere (`.gitattributes`); a CRLF `.sh` fails on the VPS.
- Python 3.12 image (`Dockerfile`); upstream crawlers run 3.10, the copied modules work on both.
- Version: this file's footer. Bump it with every change (global rule `version-bump.md`).

## Deployment

On the VPS, `~/docker/manual-refresh` is a clone of this repo: `git pull --ff-only`, then `./manual-refresh.sh`. Only a `requirements.txt` change needs the image rebuilt, which the launcher does on every start anyway.

---

**Last Updated**: 2026-10-17
**Current Version**: 1.1.1
