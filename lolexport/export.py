from time import sleep
from typing import List

from riotwatcher import LolWatcher, ApiError  # type: ignore[import]
import backoff  # type: ignore[import]

from .log import logger
from .common import Json

# (Pdb) resp['matches'][0]
# {'platformId': 'NA1', 'gameId': 3517403685, 'champion': 33, 'queue': 1300, 'season': 13, 'timestamp': 1596305310886, 'role': 'DUO_SUPPORT', 'lane': 'NONE'}
def get_matches(
    lol_watcher: LolWatcher, region: str, encrypted_account_id: str
) -> List[Json]:
    received_entries: bool = True
    beginIndex: int = 0
    entries: List[Json] = []
    while received_entries:
        resp = lol_watcher.match.matchlist_by_account(
            region=region,
            encrypted_account_id=encrypted_account_id,
            begin_index=beginIndex,
            end_index=beginIndex + 100,
        )
        beginIndex += 100
        logger.debug(f"Got {len(resp['matches'])} matches from offset {beginIndex}...")
        for d in resp["matches"]:
            entries.append(d)
        received_entries = len(resp["matches"]) > 0
        sleep(1)
    return entries


@backoff.on_exception(backoff.expo, ApiError)
def get_match_data(
    lol_watcher: LolWatcher, region: str, match_id: int
) -> Json:
    sleep(1)
    data: Json = lol_watcher.match.by_id(region=region, match_id=match_id)
    return data


def export_data(api_key: str, summoner_name: str, region: str) -> List[Json]:
    # get my info
    logger.debug("Getting encrypted account id...")
    lol_watcher = LolWatcher(api_key)
    me = lol_watcher.summoner.by_name(region, summoner_name)
    encrypted_account_id = me["accountId"]

    # get all matches
    matches: List[Json] = get_matches(
        lol_watcher, region, encrypted_account_id
    )

    # attach lots of metadata to each match Dict response
    for i, m in enumerate(matches, 1):
        logger.debug(f"[{i}/{len(matches)}] Requesting match_id => {m['gameId']}")
        # make sure were not overwriting some key from the API
        assert "matchData" not in m
        m["matchData"] = get_match_data(lol_watcher, region, m["gameId"])

    return matches
