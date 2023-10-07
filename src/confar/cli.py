#!/usr/bin/env python3

from typer import Typer
from .aggregate import Aggregator
from .runner import Runner

app = Typer()


@app.command()
def parse(file_path: str):
    config = Aggregator().parse_file(file_path)

    print(config)


@app.command()
def run(file_path: str, flow: str = 'default'):
    config = Aggregator().parse_file(file_path)

    result = Runner(config).execute_flow(flow=flow)

    print(result)


if __name__ == "__main__":
    app()
