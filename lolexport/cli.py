import json
from pathlib import Path

import click

from .log import logger
from .export import export_data
from .parse import parse_export


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--to", "-t", type=click.Path(), required=True, help="JSON file to dump export to"
)
@click.option(
    "--api-key-file",
    "-k",
    type=click.Path(exists=True),
    required=True,
    help="json file with api key",
)
@click.option("--username", "-u", required=True, help="league of legends summoner name")
@click.option("--region", "-r", required=True, help="league of legends region name")
def export(to: str, api_key_file: str, username: str, region: str) -> None:
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


@main.command()
@click.option(
    "--from",
    "-f",
    "from_",
    type=click.Path(exists=True),
    required=True,
    help="exported JSON file to process",
)
def parse(from_: str) -> None:
    """
    Parses the exported data to attach additional metadata

    Prints results to STDOUT
    """
    export_file: Path = Path(from_)
    parsed_info = list(parse_export(export_file))
    click.echo(json.dumps(parsed_info))
