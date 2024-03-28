import argparse
import csv
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='Path to the CSV file')

args = parser.parse_args()

template = env.get_template('template.html')

with open(args.file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    # rendered_template = template.render({'rows': reader})
    rows = [[datetime.strptime(row[0], '%H:%M')] + row[1:] for row in reader]
    rendered_template = template.render({'rows': rows})

with open('output.html', 'w', encoding='utf-8') as html_file:
    html_file.write(rendered_template)
