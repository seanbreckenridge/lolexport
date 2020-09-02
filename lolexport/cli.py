import json
from pathlib import Path

import click

from .log import logger
from .export import export_data


@click.command()
@click.option(
    "--to", type=click.Path(), required=True, help="JSON file to dump export to"
)
@click.option(
    "--api-key-file",
    type=click.Path(exists=True),
    required=True,
    help="json file with api key",
)
@click.option("--username", required=True, help="league of legends summoner name")
@click.option("--region", required=True, help="league of legends region name")
def main(to, api_key_file, username, region):
    """
    Download all of your match history
    """
    # make sure we can write to 'to'
    p = Path(to)
    p.touch()

    # read API key
    with open(api_key_file) as f:
        api_key: str = json.load(f)["api_key"]

    # download all the data
    data = export_data(api_key, username, region)

    # write to file
    with p.open("w") as dump_f:
        json.dump(data, dump_f)
    logger.info(f"Wrote to {to} successfully")
