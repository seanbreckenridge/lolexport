# lolexport

Exports League of Legends Match History metadata using the RiotGames API

I don't play league of legends that often anymore, this is to export my entire match history so I can do some analysis as part of [`HPI`](https://github.com/seanbreckenridge/HPI). With [`group-and-termgraph`](https://github.com/seanbreckenridge/core/blob/main/shellscripts/group-and-termgraph)

```bash
$ hpi query my.league.export -s | jq '.game_mode' -r | group-and-termgraph
ODYSSEY   : ▏ 3.00
ULTBOOK   : ▇▇ 12.00
GAMEMODEX : ▇▇▇▇ 29.00
NEXUSBLITZ: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 110.00
ARAM      : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 159.00
CLASSIC   : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 203.00
URF       : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 293.00
$ hpi query my.league.export -s | jq '.champion' -r | group-and-termgraph | tail -n 10
Rengar      : ▇▇▇▇▇ 17.00
TwistedFate : ▇▇▇▇▇ 17.00
Lux         : ▇▇▇▇▇▇ 20.00
Thresh      : ▇▇▇▇▇▇ 20.00
Bard        : ▇▇▇▇▇▇▇ 25.00
Riven       : ▇▇▇▇▇▇▇▇ 26.00
MasterYi    : ▇▇▇▇▇▇▇▇▇ 29.00
Gragas      : ▇▇▇▇▇▇▇▇▇ 30.00
Yasuo       : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 68.00
LeeSin      : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 159.00
```

Though, more interesting to me is that this tells me when/how long every match was, which means I can graph my activity.

I'm not sure how far back the match history goes. I've been playing on and off since 2015 but the history only goes back to 2018. May be a ~2/3 year limit, or that might just be when this API Version was supported/standardized.

Get an API key from [here](https://developer.riotgames.com/) and put it in a JSON file, with the same format as `./api_key_example.json`

Combines the results from `matchlist_by_puuid` and `matches/by-puuid`, and dumps all the info to a JSON file.

## Installation

Requires at least `python3.7`

To install with pip, run:

    pip install git+https://github.com/seanbreckenridge/lolexport

This is accessible as `lolexport` and using `python3 -m lolexport`

## Usage

Theres 2 commands here, `export` (which does the majority of the work, exporting info from your matches to a JSON file) and then `parse` which takes that as input and extracts (what I consider to be) useful data from it.

### Export

```
python3 -m lolexport export --help
Usage: lolexport export [OPTIONS]

  Download all of your match history

Options:
  -t, --to PATH            JSON file to dump export to  [required]
  -k, --api-key-file PATH  json file with api key  [required]
  -u, --username TEXT      league of legends summoner name  [required]
  -r, --region TEXT        league of legends region name  [required]
  --help                   Show this message and exit.

```

```
$ python3 -m lolexport export --to data.json --api-key-file ./api_key.json --username yourSummonnerName --region na1
[D 220226 19:27:00 export:44] Getting encrypted account id...
[D 220226 19:27:00 export:23] Got 100 matches from offset 100...
[D 220226 19:27:01 export:23] Got 100 matches from offset 200...
[D 220226 19:27:02 export:23] Got 100 matches from offset 300...
[D 220226 19:27:03 export:23] Got 3 matches from offset 400...
[D 220226 19:27:04 export:23] Got 0 matches from offset 500...
[D 220226 19:27:05 export:56] [1/303] Requesting match_id => NA1_4078236924
[D 220226 19:27:07 export:56] [2/303] Requesting match_id => NA1_4078245874
[D 220226 19:27:08 export:56] [3/303] Requesting match_id => NA1_4076309908
[D 220226 19:27:09 export:56] [4/303] Requesting match_id => NA1_4076197909
[D 220226 19:27:10 export:56] [5/303] Requesting match_id => NA1_4074607857
...
$ du -h data.json
9.2M	data.json
```

See [here](https://developer.riotgames.com/docs/lol) for region codes.

### Merge

Takes multiple JSON files as input and loads them into memory, removing duplicates

```
$ python3 -m lolexport merge -u yourSummonnerName ~/data/league_of_legends/*.json
[D 220227 04:38:41 merge:152] Skipped 438 items, returning 809 items...
Python 3.10.2 (main, Jan 15 2022, 19:56:27) [GCC 11.1.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.1.0 -- An enhanced Interactive Python. Type '?' for help.

Use res to access visit data
```

```Python
In [1]: res[0]._serialize()
Out[1]:
{'username': 'yourSummonnerName',
 'game_id': 3517403685,
 'won': False,
 'champion': 'Rammus',
 'game_started': datetime.datetime(2020, 8, 1, 18, 8, 30, tzinfo=datetime.timezone.utc),
 'game_ended': datetime.datetime(2020, 8, 1, 18, 25, 36, tzinfo=datetime.timezone.utc),
 'game_mode': 'NEXUSBLITZ'}

In [2]: res[0].raw
Out[2]: {'gameId': 3517403685, 'champion': {'name': 'Rammus', 'title': 'the Armordillo', 'blurb': 'Idolized by many, dismissed by some, mystifying to all, the curious being Rammus is an enigma. Protected by a spiked shell, he inspires increasingly disparate theories on his origin wherever he goes—from demigod, to sacred oracle, to a mere beast...', 'tags': ['Tank', 'Fighter'], 'partype': 'Mana'}, 'queue': None, 'season': 13, 'role': 'DUO_SUPPORT', 'lane': 'NONE', 'gameCreation': 1596305310886, 'gameDuration': 1026, 'map': 'Nexus Blitz', 'gameMode': 'NEXUSBLITZ'
```

### Parsing

This command is deprecated, it was used for the v4 API -- v5 now includes the relevant static data

The export above saves all the data, but I'm not interested in tons of the specifics, so `lolexport.parse` is what I'd use, you're free to parse the data however.

```
python3 -m lolexport parse --help
Usage: lolexport parse [OPTIONS]

  Parses the exported data to attach additional metadata

  Prints results to STDOUT

Options:
  -f, --from PATH  exported JSON file to process  [required]
  --help           Show this message and exit.
```

It prints the parsed data to STDOUT, so you can do:

`python3 -m lolexport parse --from ./data.json > parsed.json`

That removes some of the fields I'm not interested in, and replaces champion/map/queue IDs with their names.
