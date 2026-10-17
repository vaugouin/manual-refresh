# manual-refresh

Interactive console to refresh one TMDb movie, series or person by its id, then its Wikipedia pages, outside the always-on [tmdb-crawler](https://github.com/vaugouin/tmdb-crawler) and [wikipedia-crawler](https://github.com/vaugouin/wikipedia-crawler) containers. The crawler modules here are copies of those two repos. Agent conventions: [AGENTS.md](AGENTS.md).

## What a refresh covers

- **Movie**: TMDb details, French texts, credits, keywords, similar titles and recommendations, release dates per country, watch providers, images, videos; then the English and French Wikipedia pages (sections in plain text and Markdown, internal links, references, images).
- **Series**: the same minus release dates, plus the seasons and episodes TMDb reports as changed.
- **Person**: TMDb details, credits, images; then Wikipedia.
- **Qid list**: Wikipedia only, for one content family.

## Configuration

Copy [.env.example](.env.example) to `.env` and fill it in. `.env` is git-ignored and docker-ignored.

| Variable | Purpose |
| --- | --- |
| `WIKIMEDIA_USER_AGENT` | User agent sent to Wikimedia APIs, with a contact ([policy](https://meta.wikimedia.org/wiki/User-Agent_policy)). Required. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MariaDB connection. |
| `DB_NAMESPACE` | Table prefix (default `T_WC_`). |
| `USER_TIMEZONE` | IANA timezone (e.g. `Europe/Paris`). |
| `TMDB_API_DOMAIN_URL`, `TMDB_API_KEY`, `TMDB_API_TOKEN` | TMDb API access. |
| `WIKIPEDIA_CRAWLER_WORKERS`, `WIKIPEDIA_CRAWLER_MAX_RPS` | Optional Wikipedia fetch workers and request rate (defaults 8 and 20). |

## Usage

```bash
cd ~/docker/manual-refresh
./manual-refresh.sh
```

```python
>>> import update_entity as ue
>>> ue.f_updatemovie(21266)
>>> ue.f_updateserie(171802)
>>> ue.f_updateperson(13472)
>>> ue.f_updateqids("Q1092,Q845176,", "collection")
```

Each call returns `{"tmdb": code, "wikipedia": summary}`, with code `1` OK, `0` gone, `-1` transient error. Options: `blnforce=True` retries an id TMDb once reported as gone, `blnwikipedia=False` skips Wikipedia, `blnseasons=False` (series) skips seasons and episodes.

Valid families for `f_updateqids`: movie, serie, person, item, list, movement, collection (T2S collection), tmdbcollection (TMDb collection), group, death, award, nomination, topic, technical, character, wikidatacharacter, episode, keyword, season, sourcework, other.

To stay gentler on Wikimedia than the main crawler (the rate limit is per process):

```bash
WIKIPEDIA_CRAWLER_MAX_RPS=5 ./manual-refresh.sh
```

## License

MIT, see [LICENSE](LICENSE).
