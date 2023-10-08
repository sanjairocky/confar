from jinja2 import Environment, FileSystemLoader
import os

# Load the Jinja2 template environment
env = Environment(loader=FileSystemLoader(
    os.path.join(__path__[0], 'templates')))


def render_result(result: dict):

    flow_id = result['id']

    template = env.get_template('flow.html')

    # Render the HTML with the JSON data
    rendered_html = template.render(data=result)

    # Write the rendered HTML to an output file or use it as needed
    with open(f'{flow_id}.html', 'w') as output_file:
        output_file.write(rendered_html)

    return f"result generated at {os.getcwd()}/{flow_id}.html"
