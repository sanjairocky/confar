#!/usr/bin/env python3

from typer import Typer
import json
from .aggregate import Aggregator
from .runner import Runner
from .utils.renderer import render_result

app = Typer()


@app.command()
def parse(file_path: str):
    config = Aggregator().parse_file(file_path)

    print(config)


@app.command()
def run(file_path: str, flow: str = 'default'):
    config = Aggregator().parse_file(file_path)

    result = Runner(config).execute_flow(flow=flow, confar_id=config['id'])

    # Write the rendered HTML to an output file or use it as needed
    with open(f'{result["id"]}.json', 'w') as output_file:
        output_file.write(json.dumps(result))

    result = render_result(result=result)

    print(result)


if __name__ == "__main__":
    app()
