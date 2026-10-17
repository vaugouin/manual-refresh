"""
Ad-hoc refresh of one entity (TMDb + Wikipedia) by its id, from a REPL on the VPS.

Replaces the copy-pasted snippets: each function chains the TMDb "everything" call
(details, credits, keywords, similar / recommendations, release dates, watch providers,
images, videos, as the tmdb-crawler does it today) with the Wikipedia refresh of the
entity's Qid (sections with CONTENT_MD, links, references, images).

Usage, inside the container started by manual-refresh.sh:
    >>> import update_entity as ue
    >>> ue.f_updatemovie(21266)
    >>> ue.f_updateserie(171802)
    >>> ue.f_updateperson(13472)
    >>> ue.f_updateqids("Q1092,Q845176,", "collection")

WIKIMEDIA_USER_AGENT comes from .env (--env-file) and must be set before
wikipedia_crawler_helpers is imported, which reads it at import time. Wikimedia asks
for a contact in it: https://meta.wikimedia.org/wiki/User-Agent_policy
"""

import os

from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("WIKIMEDIA_USER_AGENT"):
    raise RuntimeError("WIKIMEDIA_USER_AGENT is not set: add it to .env (see .env.example)")

import citizenphil as cp
import tmdb_functions as tf
import wikipedia_functions as wf


def _f_wikipedia(strtable, strfieldid, lngid, strcontent):
    """Refresh the Wikipedia pages of a TMDb entity through its ID_WIKIDATA."""
    strwikidataid = cp.f_descfromcode(strtable, strfieldid, "ID_WIKIDATA", lngid)
    if not strwikidataid:
        print(f"No ID_WIKIDATA in {strtable} for {strfieldid}={lngid}: Wikipedia skipped")
        return None
    return wf.f_wikipediaqidtosqleverything(strwikidataid, strcontent=strcontent)


def _f_tmdb(strentitytype, lngid, fn, blnforce):
    """Run a TMDb everything call; blnforce first forgets an id recorded as gone."""
    if blnforce:
        tf.f_tmdbidnotfoundclear(strentitytype, lngid)
    intresult = fn(lngid)
    if intresult == tf.INT_TMDB_FETCH_GONE:
        print(f"TMDb {strentitytype} {lngid}: gone (T_WC_TMDB_ID_NOT_FOUND); blnforce=True to retry")
    elif intresult == tf.INT_TMDB_FETCH_ERROR:
        print(f"TMDb {strentitytype} {lngid}: transient error, retry later")
    return intresult


def f_updatemovie(lngid, blnwikipedia=True, blnforce=False):
    """TMDb movie (incl. release dates and watch providers), then its Wikipedia pages."""
    intresult = _f_tmdb("movie", lngid, tf.f_tmdbmovietosqleverything, blnforce)
    arrwiki = None
    if blnwikipedia and intresult == tf.INT_TMDB_FETCH_OK:
        arrwiki = _f_wikipedia("T_WC_TMDB_MOVIE", "ID_MOVIE", lngid, "movie")
    return {"tmdb": intresult, "wikipedia": arrwiki}


def f_updateserie(lngid, blnwikipedia=True, blnforce=False, blnseasons=True):
    """TMDb series (incl. watch providers), its changed seasons/episodes, then Wikipedia."""
    intresult = _f_tmdb("serie", lngid, tf.f_tmdbserietosqleverything, blnforce)
    arrwiki = None
    if intresult == tf.INT_TMDB_FETCH_OK:
        if blnseasons:
            tf.f_tmdbserieselectiveseasonsepisodestosql(lngid)
        if blnwikipedia:
            arrwiki = _f_wikipedia("T_WC_TMDB_SERIE", "ID_SERIE", lngid, "serie")
    return {"tmdb": intresult, "wikipedia": arrwiki}


def f_updateperson(lngid, blnwikipedia=True, blnforce=False):
    """TMDb person (details, credits, images), then its Wikipedia pages."""
    intresult = _f_tmdb("person", lngid, tf.f_tmdbpersontosqleverything, blnforce)
    arrwiki = None
    if blnwikipedia and intresult == tf.INT_TMDB_FETCH_OK:
        arrwiki = _f_wikipedia("T_WC_TMDB_PERSON", "ID_PERSON", lngid, "person")
    return {"tmdb": intresult, "wikipedia": arrwiki}


def f_updateqids(strwikidataidlist, strcontent):
    """Wikipedia refresh of a comma-separated Qid list, one family (CONTENT_CONFIG key).

    strcontent: movie, serie, person, item, list, movement, collection (T2S collection),
    tmdbcollection, group, death, award, nomination, topic, technical, character,
    wikidatacharacter, episode, keyword, season, sourcework, other.
    """
    arrwikidataids = [s.strip() for s in strwikidataidlist.split(",") if s.strip()]
    arrsummaries, arrfailures = [], []
    for intrank, strwikidataid in enumerate(arrwikidataids, start=1):
        print(f"--- {intrank}/{len(arrwikidataids)} {strwikidataid} ---")
        try:
            arrsummaries.append(wf.f_wikipediaqidtosqleverything(strwikidataid, strcontent=strcontent))
        except Exception as err:
            print(f"FAILED {strwikidataid}: {err}")
            arrfailures.append((strwikidataid, str(err)))
    print(f"OK {len(arrsummaries)}/{len(arrwikidataids)} ; failures: {arrfailures}")
    return arrsummaries, arrfailures
