import argparse
import csv
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime, timedelta
import os
import rcssmin

env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, help="Path to the CSV file")

args = parser.parse_args()

input_filename = args.file
basename = os.path.splitext(os.path.basename(input_filename))[0]
output_filename = f"output/{basename}.html"

template = env.get_template("template.html")

with open(args.file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    # rendered_template = template.render({'rows': reader})
    rows = []
    CURRENT_MINUTE = None
    for row in reader: # 00:00 MM:SS
        time = datetime.strptime(row[0], '%M:%S')
        if time.minute != CURRENT_MINUTE:
            print(time)
            # Insert a separator row with just the timestamp
            rows.append([time, '', 'Separator'])
            CURRENT_MINUTE = time.minute
        rows.append([time] + row[1:])

    with open("style.css", "r", encoding="utf-8") as file:
        css = file.read()
        minified_css = rcssmin.cssmin(css)

        rendered_template = template.render(
            {"title": output_filename, "rows": rows, "style": minified_css}
        )

with open(output_filename, "w", encoding="utf-8") as html_file:
    html_file.write(rendered_template)
