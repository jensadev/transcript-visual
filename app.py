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

speakers = {}
types = {}

with open(args.file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    # rendered_template = template.render({'rows': reader})
    rows = []
    CURRENT_MINUTE = None
    for row in reader:  # 00:00 MM:SS
        time = datetime.strptime(row[0], "%M:%S")
        if time.minute != CURRENT_MINUTE:
            print(time)
            # Insert a separator row with just the timestamp
            rows.append([time, "", "Separator"])
            CURRENT_MINUTE = time.minute
        rows.append([time] + row[1:])

        if row[1] not in speakers:
            speakers[row[1]] = 1
        else:
            speakers[row[1]] += 1

        if row[2] != "":
            if row[2] not in types:
                types[row[2]] = 1
            else:
                types[row[2]] += 1

    print(types)

    sorted_speakers = sorted(speakers.items(), key=lambda item: item[1], reverse=True)

    with open("style.css", "r", encoding="utf-8") as file:
        css = file.read()
        minified_css = rcssmin.cssmin(css)

        rendered_template = template.render(
            {
                "title": output_filename,
                "rows": rows,
                "style": minified_css,
                "speakers": sorted_speakers,
                "types": types,
            }
        )

with open(output_filename, "w", encoding="utf-8") as html_file:
    html_file.write(rendered_template)
