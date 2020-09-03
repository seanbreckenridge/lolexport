import pathlib, json
import lolexport.parse

parsed_info = list(lolexport.parse.parse_export(pathlib.Path('~/data/league_of_legends/raw_data.json').expanduser()))
with open('parsed_info.json', 'w') as jf:
    json.dump(parsed_info, jf)
