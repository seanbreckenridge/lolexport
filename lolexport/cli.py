import json
from pathlib import Path
from typing import Sequence

import click

from .log import logger
from .export import export_data
from .parse import parse_export
from .merge import merge_game_histories


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
@click.option(
    "--interactive/--non-interactive",
    default=True,
    is_flag=True,
    help="interactive - if a request fails, prompts you to continue. In non-interactive mode, fails if theres a network error",
)
@click.option("--username", "-u", required=True, help="league of legends summoner name")
@click.option("--region", "-r", required=True, help="league of legends region name")
def export(
    to: str, api_key_file: str, username: str, region: str, interactive: bool
) -> None:
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
    data = export_data(api_key, username, region, interactive=interactive)

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
    parsed_info = list(parse_export(Path(from_)))
    click.echo(json.dumps(parsed_info))


@main.command()
@click.option(
    "-u", "--username", type=str, help="your league summoner name", required=True
)
@click.argument(
    "JSON_FILE",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    nargs=-1,
)
def merge(json_file: Sequence[Path], username: str) -> None:
    """
    parse/merge results from multiple JSON files
    """
    res = list(merge_game_histories(json_file, username))  # noqa
    import IPython  # type: ignore[import]

    IPython.embed(header=f"Use {click.style('res', fg='green')} to access visit data")
