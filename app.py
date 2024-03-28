import argparse
import csv
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import os
import csscompressor

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='Path to the CSV file')

args = parser.parse_args()

input_filename = args.file
basename = os.path.splitext(os.path.basename(input_filename))[0]
output_filename = f'output/{basename}.html'

template = env.get_template('template.html')

with open(args.file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    # rendered_template = template.render({'rows': reader})
    rows = [[datetime.strptime(row[0], '%H:%M')] + row[1:] for row in reader]

    with open('style.css', 'r', encoding="utf-8") as file:
        css = file.read()
    minified_css = csscompressor.compress(css)

    rendered_template = template.render({'rows': rows, 'style': minified_css})


with open(output_filename, 'w', encoding='utf-8') as html_file:
    html_file.write(rendered_template)
