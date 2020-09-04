#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse

__author__ = "marcornett"


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    names = []
    with open(filename, 'r') as f:
        text_to_search = f.read()

        year_pattern = re.compile(r'Popularity in (\d+)')
        name_rank_pattern = re.compile(
            r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>')

        year_lst = year_pattern.findall(text_to_search)
        names_rank_lst = name_rank_pattern.findall(text_to_search)

        names_dict = {}
        for name_rank in names_rank_lst:
            # print(name_rank)
            rank = name_rank[0]
            if name_rank[1] not in names_dict:
                names_dict[name_rank[1]] = rank
            if name_rank[2] not in names_dict:
                names_dict[name_rank[2]] = rank

        names_list = sorted(names_dict.items(),
                            key=lambda names_dict: names_dict[0])

        names.append(''.join(year_lst))
        for name in names_list:
            names.append(' '.join(name))
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).

    if create_summary:
        for ns_file in file_list:
            names = extract_names(ns_file)
            with open(f'{ns_file}.summary', 'w') as f:
                f.write('\n'.join(names))
    else:
        for ns_file in file_list:
            names = extract_names(ns_file)
            print('\n'.join(names))


if __name__ == '__main__':
    main(sys.argv[1:])
