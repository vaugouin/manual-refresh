#!/bin/bash
#
# Interactive container to refresh one entity (TMDb + Wikipedia) by its id, in
# parallel with the always-on tmdb-crawler and wikipedia-crawler containers.
# The folder is mounted on /app, so a file copied onto the VPS is live at once,
# without waiting for a rebuild (the build only matters when requirements.txt changes).
#
# Usage:
#   ./manual-refresh.sh
#   then, in the REPL:
#     >>> import update_entity as ue
#     >>> ue.f_updatemovie(21266)
#     >>> ue.f_updateserie(171802)
#     >>> ue.f_updateperson(13472)
#     >>> ue.f_updateqids("Q1092,Q845176,", "collection")
#
# WIKIPEDIA_CRAWLER_MAX_RPS / WIKIPEDIA_CRAWLER_WORKERS are forwarded from the host,
# so a manual run can stay gentler than the main crawler (the rate limiter is per
# process: two containers at the default 20 rps add up to 40 rps):
#   WIKIPEDIA_CRAWLER_MAX_RPS=5 ./manual-refresh.sh

strcontainername="${CONTAINER_NAME:-manual-refresh}"
if [ "$(docker ps -q -f name=^${strcontainername}$)" ]; then
    echo "$strcontainername is already running: docker stop $strcontainername"
    exit 1
fi

cd /home/debian/docker/manual-refresh
docker build -t manual-refresh-app .

arrenv=()
if [ -n "$WIKIPEDIA_CRAWLER_MAX_RPS" ]; then
    arrenv+=(-e "WIKIPEDIA_CRAWLER_MAX_RPS=$WIKIPEDIA_CRAWLER_MAX_RPS")
fi
if [ -n "$WIKIPEDIA_CRAWLER_WORKERS" ]; then
    arrenv+=(-e "WIKIPEDIA_CRAWLER_WORKERS=$WIKIPEDIA_CRAWLER_WORKERS")
fi

docker run -it --rm --network="host" \
    --env-file /home/debian/docker/manual-refresh/.env \
    "${arrenv[@]}" \
    -v "$(pwd)":/app \
    -v /home/debian/docker/shared_data:/shared \
    --name "$strcontainername" manual-refresh-app python
