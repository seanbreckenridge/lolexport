# lolexport

Exports League of Legends Match History metadata using the RiotGames API

I don't play league of legends that often anymore, this is to export my entire match history so I can do some analysis as part of [`HPI`](https://github.com/seanbreckenridge/HPI). Like:

```python
>>> from my.games.league import history
>>> import pprint, collections
>>> league_game_history = list(history())
# whats my winrate?
>>> collections.Counter(map(lambda g: g.won, league_game_history))
Counter({True: 265, False: 241})
# most common champions?
>>> pprint.pprint(collections.Counter(map(lambda g: g.champion_name, league_game_history)).most_common(10))
[('Lee Sin', 114),
 ('Yasuo', 29),
 ('Master Yi', 25),
 ('Riven', 20),
 ('Gragas', 19),
 ('Thresh', 13),
 ('Lux', 12),
 ('Twisted Fate', 12),
 ('Rengar', 11),
 ('Bard', 11)]
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

---

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
