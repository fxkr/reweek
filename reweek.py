#!/usr/bin/env python2
# Copyright (C) 2011 Felix Kaiser
# License: revised BSD

import argparse
import datetime
import re
import sys


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SINGLE_DAY_TMPL  = "{y1:04}-{m1:02}-{d1:02} ({day1})"
DAY_RANGE_TMPL   = "{y1:04}-{m1:02}-{d1:02}..{d2:02} ({day1}-{day2})"
MONTH_RANGE_TMPL = "{y1:04}-{m1:02}-{d1:02}..{m2:02}-{d2:02} ({day1}-{day2})"
YEAR_RANGE_TMPL  = "{y1:04}-{m1:02}-{d1:02}..{y2:02}-{m2:02}-{d2:02} ({day1}-{day2})"
HINT_WRONG_HINT  = "??"

EXPR = re.compile(r"""
    # Start date: yyyy-mm-dd
    (?P<y1>\d{4})-
    (?P<m1>\d{2})-
    (?P<d1>\d{2})

    # End date: [:[yyyy-]mm-]dd]
    (?:\.\.(?:(?:
            (?P<y2>\d{4})-)?
        (?P<m2>\d{2})-)?
    (?P<d2>\d{2}))?

    # Hints: [(day[??][-day[??]])]
    (?:\ \(
        (?P<day1>[A-Z][a-z][a-z])
        (?:\?\?)?
        (?:-
            (?P<day2>[A-Z][a-z][a-z])
            (?:\?\?)?
        )?
    \))?""", re.VERBOSE)


def change(text):
    return EXPR.sub(_replace_match, text)


def _replace_match(match):
    groups = match.groupdict()
    to_int = lambda x: x if x is None else int(x)
    return _replace_datespec(
        (to_int(groups["y1"]), to_int(groups["m1"]), to_int(groups["d1"])),
        (to_int(groups["y2"]), to_int(groups["m2"]), to_int(groups["d2"])),
        (groups["day1"], groups["day2"]))


def _replace_datespec(date1, date2, hints):
    y1, m1, d1 = date1
    y2, m2, d2 = date2
    orig_hint1, orig_hint2 = hints
    if y2 and not m2:
        raise ValueError()
    elif m2 and not d2:
        raise ValueError()

    # Autocomplete end date
    if not y2:
        y2 = y1
    if not m2:
        m2 = m1
    if not d2:
        d2 = d1

    # Create hints
    hint1 = DAYS[datetime.date(y1, m1, d1).weekday()]
    hint2 = DAYS[datetime.date(y2, m2, d2).weekday()]
    if orig_hint1 and orig_hint1.lower() != hint1.lower():
        hint1 = orig_hint1 + HINT_WRONG_HINT
    if orig_hint2 and orig_hint2.lower() != hint2.lower():
        hint2 = orig_hint2 + HINT_WRONG_HINT

    # Select template
    if y1 != y2:
        template = YEAR_RANGE_TMPL
    elif m1 != m2:
        template = MONTH_RANGE_TMPL
    elif d1 != d2:
        template = DAY_RANGE_TMPL
    else:
        template = SINGLE_DAY_TMPL

    # Compile result
    return template.format(
        y1=y1, m1=m1, d1=d1,
        y2=y2, m2=m2, d2=d2,
        day1=hint1, day2=hint2)


def main(text):
    par = argparse.ArgumentParser(
        description='Reformat date strings in a text.')
    par.add_argument("file", nargs="?",
        type=argparse.FileType('r'), default=sys.stdin,
        help="Path of the file. Defaults to standard input.")
    args = par.parse_args()
    sys.stdout.write(change(args.file.read()))
    sys.stdout.flush()
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)

