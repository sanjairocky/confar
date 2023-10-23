#!/usr/bin/env python3

from typer import Typer
from .aggregate import Aggregator
from .runner import Runner
from uuid import uuid4 as uuid

app = Typer()


@app.command()
def parse(file_path: str):
    config = Aggregator().parse_file(file_path)

    print(config)


@app.command()
def run(file_path: str, flow: str = 'default'):
    config = Aggregator().parse_file(file_path)

    if 'id' not in config:
        config['id'] = str(uuid())

    runner = Runner(config)

    def on_event_fired(evt):
        print(f"{evt.timestamp} - {evt.event}  : {evt.data}")

    runner.on_any(on_event_fired)

    runner.execute_flow(flow=flow, confar_id=config['id'])


if __name__ == "__main__":
    app()
