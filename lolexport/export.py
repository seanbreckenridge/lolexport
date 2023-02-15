from time import sleep
from typing import Dict, List, Any

from riotwatcher import LolWatcher, ApiError  # type: ignore[import]
import backoff  # type: ignore[import]
import click

from .log import logger


def get_matches(lol_watcher: LolWatcher, region: str, my_puuid: str) -> List[str]:
    """
    > resp[0]
    'NA1_4078236924'
    """
    received_entries: bool = True
    beginIndex: int = 0
    entries: List[str] = []
    while received_entries:
        resp: List[str] = lol_watcher.match.matchlist_by_puuid(
            region=fix_region(region),
            puuid=my_puuid,
            start=beginIndex,
            count=100,
        )
        beginIndex += 100
        logger.debug(f"Got {len(resp)} matches from offset {beginIndex}...")
        for d in resp:
            entries.append(d)
        received_entries = len(resp) > 0
        sleep(1)
    return entries


@backoff.on_exception(backoff.expo, ApiError)
def get_match_data(
    lol_watcher: LolWatcher, region: str, match_id: str
) -> Dict[str, Any]:
    sleep(1)
    data: Dict[str, Any] = lol_watcher.match.by_id(
        region=fix_region(region), match_id=match_id
    )
    return data


def export_data(
    api_key: str, summoner_name: str, region: str, *, interactive: bool = True
) -> List[Dict[str, Any]]:
    # get my info
    logger.debug("Getting encrypted account id...")
    lol_watcher = LolWatcher(api_key)
    me: Dict[str, Any] = lol_watcher.summoner.by_name(region, summoner_name)
    my_puuid = me["puuid"]

    # get all matches
    matches: List[str] = get_matches(lol_watcher, region, my_puuid)

    data: List[Dict[str, Any]] = []

    # attach lots of metadata to each match Dict response
    for i, m in enumerate(matches, 1):
        logger.debug(f"[{i}/{len(matches)}] Requesting match_id => {m}")
        # option to continue after a failed game
        try:
            resp = get_match_data(lol_watcher, region, m)
        except (Exception, KeyboardInterrupt) as e:
            if not interactive:
                raise
            if not isinstance(e, KeyboardInterrupt):
                logger.exception(f"request failed: {e}")
            if click.confirm("Continue requesting?", default=True):
                continue
            else:
                break

        # make sure were not overwriting some key from the API
        assert "gameId" not in resp
        resp["gameId"] = m
        data.append(resp)
    return data


def fix_region(region: str) -> str:
    """
    handle older region names, convert to new API
    """
    region_upper = region.upper()
    if region_upper == "BR1":
        region = "americas"
    elif region_upper == "EUN1":
        region = "europe"
    elif region_upper == "EUW1":
        region = "europe"
    elif region_upper == "JP1":
        region = "asia"
    elif region_upper == "KR":
        region = "asia"
    elif region_upper == "LA1":
        region = "americas"
    elif region_upper == "LA2":
        region = "americas"
    elif region_upper == "NA1":
        region = "americas"
    elif region_upper == "OC1":
        region = "asia"
    elif region_upper == "TR1":
        region = "europe"
    elif region_upper == "RU":
        region = "europe"
    return region
