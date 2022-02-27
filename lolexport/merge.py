import re
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, Iterator, Union, Set, Sequence, cast

from .log import logger


def parse_datetime_sec(d: Union[str, float, int]) -> datetime:
    return datetime.fromtimestamp(int(d), tz=timezone.utc)


def parse_datetime_millis(d: Union[str, float, int]) -> datetime:
    return parse_datetime_sec(int(d) / 1000)


class Game:
    def __init__(self, raw: Dict[str, Any], username: str) -> None:
        self.raw: Dict[str, Any] = raw
        self.username: str = username

    def __repr__(self) -> str:
        return f"Game({self._serialize()})"

    __str__ = __repr__

    @property
    def _stats_v4(self) -> Optional[Dict[str, Any]]:
        if "stats" in self.raw and "playerNames" in self.raw:
            uids = {int(uid): name for uid, name in self.raw["playerNames"].items()}
            _uid_matches = [k for k, v in uids.items() if self.username == v]
            assert (
                len(_uid_matches) == 1
            ), f"Couldn't extract id for {self.username} from {uids}"
            my_uid = _uid_matches[0]
            _stats_matches = [
                ustats
                for ustats in self.raw["stats"]
                if ustats["participantId"] == my_uid
            ]
            assert (
                len(_stats_matches) == 1
            ), f"Couldn't extract stats for game {self.raw} using {uids}"
            data = _stats_matches[0]
            assert isinstance(data, dict)
            return data
        return None

    @property
    def _stats_v5(self) -> Optional[Dict[str, Any]]:
        if "info" in self.raw:
            info = self.raw["info"]
            if "participants" in info:
                _stats_matches = [
                    s
                    for s in info["participants"]
                    if s["summonerName"] == self.username
                ]
                assert (
                    len(_stats_matches) == 1
                ), f"Couldn't extract stats for game {self.raw} using {self.username}"
                data = _stats_matches[0]
                assert isinstance(data, dict)
                return data
        return None

    @property
    def won(self) -> bool:
        sv4 = self._stats_v4
        if sv4 is not None:
            won = sv4["win"]
            assert won in {True, False}, str(sv4)
            return cast(bool, won)
        else:
            sv5 = self._stats_v5
            assert (
                sv5 is not None
            ), f"Could not determine if data was v4 of v5 {self.raw}"
            won = sv5["win"]
            assert won in {True, False}, str(sv5)
            return cast(bool, won)

    @staticmethod
    def _clean_champion_name(ss: Any) -> str:
        assert isinstance(ss, str)
        return re.sub(r"\s", "", ss)

    @property
    def champion(self) -> str:
        sv4 = self._stats_v4
        if sv4 is not None:
            return self.__class__._clean_champion_name(sv4["champion"]["name"])
        else:
            sv5 = self._stats_v5
            assert (
                sv5 is not None
            ), f"Could not determine if data was v4 of v5 {self.raw}"
            return self.__class__._clean_champion_name(sv5["championName"])

    @property
    def _info(self) -> Dict[str, Any]:
        info = self.raw
        if "info" in self.raw:
            info = self.raw["info"]
        return info

    @property
    def game_started(self) -> datetime:
        return parse_datetime_millis(self._info["gameCreation"])

    @property
    def game_id(self) -> int:
        return int(self._info["gameId"])

    @property
    def game_duration(self) -> timedelta:
        return timedelta(seconds=int(self._info["gameDuration"]))

    @property
    def game_ended(self) -> datetime:
        return self.game_started + self.game_duration

    @property
    def game_mode(self) -> str:
        gm = self._info["gameMode"]
        assert isinstance(gm, str)
        return gm

    def _serialize(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "game_id": self.game_id,
            "won": self.won,
            "champion": self.champion,
            "game_started": self.game_started,
            "game_ended": self.game_ended,
            "game_mode": self.game_mode,
        }

    @classmethod
    def from_file(cls, pp: Path, username: str) -> Iterator["Game"]:
        data = json.loads(pp.read_text())
        for blob in data:
            yield cls(raw=blob, username=username)


def merge_game_histories(files: Sequence[Path], username: str) -> Iterator[Game]:
    emitted: Set[int] = set()
    skipped = 0
    for f in files:
        for g in Game.from_file(f, username):
            if g.game_id in emitted:
                skipped += 1
                continue
            emitted.add(g.game_id)
            yield g
    logger.debug(f"Skipped {skipped} items, returning {len(emitted)} items...")
