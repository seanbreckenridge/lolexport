# lolexport

Exports League of Legends Match History metadata using the RiotGames API

I don't play league of legends that often anymore, this is to export my entire match history so I can do some analysis as part of [`HPI`](https://github.com/seanbreckenridge/HPI).

I'm not sure how far back the match history goes. I've been playing on and off since 2015 but the history only goes back to 2018. May be a ~2/3 year limit, or that might just be when this API Version was supported/standardized.

Get an API key from [here](https://developer.riotgames.com/) and put it in a JSON file, with the same format as `./api_key_example.json`

Combines the results from <https://developer.riotgames.com/apis#match-v4/GET_getMatchlist> and <https://developer.riotgames.com/apis#match-v4/GET_getMatch>, and dumps all the info to a JSON file.

See [riotwatcher docs](https://github.com/pseudonym117/Riot-Watcher) for some data_dragon (riot metadata) helper functions that may be useful, to parse the resulting JSON file.

### Export

```
Usage: lolexport [OPTIONS]

  Download all of your match history

Options:
  --to PATH            JSON file to dump export to [required]
  --api-key-file PATH  json file with api key [required]
  --username TEXT      league of legends summoner name [required]
  --region TEXT        league of legends region name [required]
  --help               Show this message and exit.

```

```
$ lolexport --to data.json --api-key-file ./api_key_example.json --username summonerName --region na1
[D 200901 21:27:41 export:32] Getting encrypted account id...
[D 200901 21:27:43 export:17] Got 100 matches from offset 100...
[D 200901 21:27:44 export:17] Got 100 matches from offset 200...
[D 200901 21:27:46 export:17] Got 100 matches from offset 300...
[D 200901 21:27:47 export:17] Got 100 matches from offset 400...
[D 200901 21:27:49 export:17] Got 100 matches from offset 500...
[D 200901 21:27:54 export:17] Got 6 matches from offset 600...
[D 200901 21:27:55 export:17] Got 0 matches from offset 700...
[D 200901 21:27:56 export:42] [1/506] Requesting match_id => 3517403685
[D 200901 21:27:57 export:42] [2/506] Requesting match_id => 3517420654
[D 200901 21:27:58 export:42] [3/506] Requesting match_id => 3517369763
[D 200901 21:28:00 export:42] [4/506] Requesting match_id => 3517356497
......
$ head -c 1000 data.json
[{"platformId": "NA1", "gameId": 3517403685, "champion": 33, "queue": 1300, "season": 13, "timestamp": 1596305310886, "role": "DUO_SUPPORT", "lane": "NONE", "matchData": {"gameId": 3517403685, "platformId": "NA1", "gameCreation": 1596305310886, "gameDuration": 1026, "queueId": 1300, "mapId": 21, "seasonId": 13, "gameVersion": "10.15.330.344", "gameMode": "NEXUSBLITZ", "gameType": "MATCHED_GAME", "teams": [{"teamId": 100, "win": "Win", "firstBlood": false, "firstTower": true, "firstInhibitor": true, "firstBaron": false, "firstDragon": false, "firstRiftHerald": true, "towerKills": 3, "inhibitorKills": 1, "baronKills": 0, "dragonKills": 0, "vilemawKills": 0, "riftHeraldKills": 1, "dominionVictoryScore": 0, "bans": [{"championId": 157, "pickTurn": 1}, {"championId": 350, "pickTurn": 2}, {"championId": 64, "pickTurn": 3}, {"championId": 7, "pickTurn": 4}, {"championId": 875, "pickTurn": 5}]}, {"teamId": 200, "win": "Fail", "firstBlood": true, "firstTower": false, "firstInhibitor": false, "f
$ du -h data.json
16M	data.json
```

See [here](https://developer.riotgames.com/docs/lol) for region codes.

## Installation

Requires at least `python3.6`

To install with pip, run:

    pip install 'git+https://github.com/seanbreckenridge/lolexport'
