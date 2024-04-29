"""Program to parse a CSV file and generate an HTML file with the transcript"""

import os
import csv
from argparse import ArgumentParser
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
import rcssmin


def parse_file(input_filename: str):
    """Function to parse the CSV file and generate the HTML file"""

    basename = os.path.splitext(os.path.basename(input_filename))[0]
    output_filename = os.path.join(args.output, f"{basename}.html")

    with open(input_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        rows = []
        speakers = {}
        types = {}
        CURRENT_MINUTE = None
        for line_number, row in enumerate(reader, start=1):
            try:
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
            except Exception as e:
                    raise Exception(f"Error at line {line_number}: {e}")

        sorted_speakers = sorted(
            speakers.items(), key=lambda item: item[1], reverse=True
        )

        render_template(output_filename, rows, sorted_speakers, types)


def minify_css(input_file: str):
    """Minify the CSS file"""
    with open(input_file, "r", encoding="utf-8") as file:
        css = file.read()
        return rcssmin.cssmin(css)


def render_template(filename: str, rows: list, speakers: dict, types: dict):
    """Function to render the Jinja2 template"""
    TEMPLATE = env.get_template("template.html")
    rendered_template = TEMPLATE.render(
        {
            "title": filename,
            "rows": rows,
            "style": minify_css("style.css"),
            "speaker1": speakers[0],
            "speaker2": speakers[1],
            "types": types,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    with open(filename.lower(), "w", encoding="utf-8") as html_file:
        html_file.write(rendered_template)


env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())

parser = ArgumentParser()
parser.add_argument("-f", "--file", required=False, help="Path to the CSV file")
parser.add_argument("-d", "--directory", required=False, help="Path to the directory")
parser.add_argument(
    "-o", "--output", default="output", help="Path to the output directory"
)

args = parser.parse_args()

if args.file is None and args.directory is None:
    parser.error("Either --file or --directory must be provided.")

errors = []

if args.directory is not None:
    for filename in os.listdir(args.directory):
        if filename.endswith(".csv"):
            try:
                filepath = os.path.join(args.directory, filename)
                parse_file(filepath)
            except Exception as e:
                errors.append(f"Error processing {filename}: {e}")

if args.file is not None:
    try:
        parse_file(args.file)
    except Exception as e:
        errors.append(f"Error processing {args.file}: {e}")

if errors:
    print("\n".join(errors))
