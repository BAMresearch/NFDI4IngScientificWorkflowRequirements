"""Compile the paper with the values from this run"""

import string
import argparse
import subprocess

PARSER = argparse.ArgumentParser(description="Compile the paper")
PARSER.add_argument(
    "-f", "--paper-template-file",
    required=False,
    default="paper.tex.template",
    help="The template file for the paper"
)
PARSER.add_argument(
    "-s", "--domain-size",
    required=True,
    help="The computed domain size"
)
ARGS = vars(PARSER.parse_args())

# place domain size in paper
with open("paper.tex", "w") as out_file:
    with open(ARGS["paper_template_file"], "r") as in_file:
        raw = string.Template(in_file.read())
        out_file.write(raw.substitute([{
            "DOMAINSIZE": ARGS["domain_size"]
        }]))

# compile paper using tectonic
subprocess.run(["tectonic", "paper.tex"], check=True)
