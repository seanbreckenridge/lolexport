"""
some code to parse though the export, extracting interesting info
and replacing IDs with the corresponding data

not exactly sure how the datadragon exports work, so I
do this after I export, not sure if it'd break in the
future if the IDs dont match
"""

import json
from pathlib import Path
from functools import partial
from typing import List, Dict, Any, NamedTuple, Iterator

import requests
from riotwatcher import LolWatcher  # type: ignore[import]

from .log import logger


def pick_keys(d: Dict[str, Any], wanted_keys: List[str]) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if k in wanted_keys}


IDMap = Dict[int, Any]


class DataDog(NamedTuple):
    champions: IDMap
    maps: IDMap
    queues: IDMap


def get_datadog_info(region: str) -> DataDog:
    l = LolWatcher("<dummy key>")
    versions = l.data_dragon.versions_for_region(region)
    # I did this on:
    # not sure if the interface changes
    # In [8]: datadog_versions
    # Out[8]: {'champion': '10.16.1', 'map': '10.16.1'}
    datadog_versions = {
        k: versions["n"][k]
        for k in [
            "champion",
            "map",
        ]
    }

    logger.debug("requesting data_dragon info...")

    # request metadata
    champion_data = l.data_dragon.champions(datadog_versions["champion"])["data"]
    map_data = l.data_dragon.maps(datadog_versions["map"])["data"]
    queue_resp = requests.get(
        "http://static.developer.riotgames.com/docs/lol/queues.json"
    )
    queue_resp.raise_for_status()
    queue_data = queue_resp.json()

    # parse useful info from metadata
    logger.debug("requesting champ info...")
    champion_info = {
        int(v["key"]): pick_keys(v, ["tags", "partype", "name", "title", "blurb"])
        for k, v in champion_data.items()
    }
    logger.debug("requesting map info...")
    map_data = {int(k): v["MapName"] for k, v in map_data.items()}
    logger.debug("requesting queue info...")
    queue_info = {
        d["queueId"]: pick_keys(d, ["map", "description"]) for d in queue_data
    }

    return DataDog(
        champions=champion_info,
        maps=map_data,
        queues=queue_info,
    )


def _parse_participant(d: Dict, dd: DataDog) -> Dict[str, Any]:
    s = d["stats"]
    return {
        "champion": dd.champions[d["championId"]],
        **pick_keys(d, ["spellId1", "spellId2", "teamId", "participantId"]),
        **pick_keys(
            s,
            [
                "win",
                "kills",
                "deaths",
                "assists",
                "largestKillingSpree",
                "largestMultiKill",
                "killingSprees",
                "longestTimeSpentLiving",
                "doubleKills",
                "tripleKills",
                "quadraKills",
                "pentaKills",
                "totalDamageDealt",
                "magicDamageDealt",
                "physicalDamageDealt",
                "trueDamageDealt",
                "totalDamageDealtToChampions",
                "totalHeal",
                "damageDealtToObjectives",
                "totalDamageTaken",
                "visionScore",
                "timeCCingOthers",
                "totalDamageTaken",
                "goldEarned",
                "goldSpent",
                "turretKills",
                "inhibitorKills",
                "totalMinionsKilled",
                "neutralMinionsKilled",
                "neutralMinionsKilledTeamJungle",
                "neutralMinionsKilledEnemyJungle",
                "totalTimeCrowdControlDealt",
                "champLevel",
                "wardsPlaced",
                "firstBloodKill",
                "firstTowerKill",
            ],
        ),
    }


def _parse_game_data(d: Dict[str, Any], dd: DataDog) -> Dict[str, Any]:
    """
    Parses stuff I think is interesting/useful from each game
    """
    m = d["matchData"]
    all_players = {
        d["participantId"]: d["player"]["summonerName"]
        for d in m["participantIdentities"]
    }
    participant_data = [_parse_participant(pdat, dd) for pdat in m["participants"]]
    # set summoner name on stats
    for pdat in participant_data:
        pdat["summonerName"] = all_players[pdat["participantId"]]

    return {
        "gameId": d["gameId"],  # to uniquely identify games
        "champion": dd.champions[d["champion"]],  # champion metadata
        "queue": dd.queues.get(d["queue"]),
        "season": d["season"],
        "role": d["role"],
        "lane": d["lane"],
        "gameCreation": m["gameCreation"],
        "gameDuration": m["gameDuration"],
        "map": dd.maps.get(m["mapId"]),
        "gameMode": m["gameMode"],
        "gameType": m["gameType"],
        "playerNames": all_players,
        "stats": participant_data,
    }


def parse_export(path: Path, region: str = "na1") -> Iterator[Dict]:
    assert path.exists()

    # get datadog (league metadata)
    dd: DataDog = get_datadog_info(region)

    logger.debug("loading JSON...")
    # load info
    with path.open("r") as pf:
        items = json.load(pf)

    # map parse func
    _pgame = partial(_parse_game_data, dd=dd)
    yield from map(_pgame, items)
