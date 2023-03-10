"""
Convert spanish-sme xlsx to GT-style xml.
"""
import argparse
from itertools import islice
from collections import defaultdict, namedtuple

MISSING_DEP_HELP = """
cannot run due to missing dependencies. hint, run:
python -m venv .venv && . .venv/bin/activate && pip install -r xlsx2xml-requirements.txt
...and then try again. (remember run `deactivate` in the shell when you're done)
"""

try:
    from lxml.etree import Element, SubElement, tostring
    from openpyxl import load_workbook
except ImportError:
    exit(MISSING_DEP_HELP)


def check_and_insert(
    value,
    parent,
    tag_name,
    ppar=None,
    ppar_tag_name=None,
    t_element=None,
):
    if value is None:
        return
    value = str(value).strip()
    if value and t_element:
        if t_element[0]:
            if ppar is not None and ppar_tag_name is not None:
                parent = SubElement(ppar, ppar_tag_name)
            element = SubElement(parent, tag_name)
            element.text = value
            element = SubElement(parent, t_element[1])
            element.text = t_element[0]
            return element
    elif value:
        if ppar is not None and ppar_tag_name is not None:
            parent = SubElement(ppar, ppar_tag_name)
        element = SubElement(parent, tag_name)
        element.text = value
        return element


def t(entry, parent_tg, parent_mg):
    el = SubElement(parent_tg, "t")
    if entry.WORD_CLASS_1:
        el.set("pos", entry.WORD_CLASS_1)
    if entry.SCIENTIFIC_NAME:
        el.set("sci", entry.SCIENTIFIC_NAME)
    el.text = entry.SAAMI if entry.SAAMI else entry.SAAMI_TRANS
    for n in range(1, 8):
        ex = getattr(entry, f"SPANISH_EX_{n}")
        if ex is not None:
            saami_ex = getattr(entry, f"SAAMI_EX_{n}")
            check_and_insert(ex, "", "x", parent_tg, "xg", [saami_ex, "xt"])
        if n <= 6:
            syn = getattr(entry, f"TRANS_SYNON{n}")
            check_and_insert(syn, "", "syn", parent_mg, "syng")


def dict2xml_bytestring(d):
    root = Element("r")
    for (lemma, pos), entries in d.items():
        print(lemma, pos)
        e = SubElement(root, "e")
        lg = SubElement(e, "lg")
        l = SubElement(lg, "l")
        if pos is not None:
            l.set("pos", pos)
        l.text = lemma

        for entry in entries:
            mg = SubElement(e, "mg")
            tg = SubElement(mg, "tg")
            tg.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
            check_and_insert(entry.RESTRICTION, tg, "re")
            check_and_insert(entry.EXPLANATION, tg, "expl")
            t(entry, tg, mg)

    return tostring(root, encoding="utf-8", pretty_print=True)


def read_column_names(columns):
    field_counts = defaultdict(int)
    fields = []
    for col in columns:
        field = col[0].value.replace(" ", "_")
        n = field_counts[field]
        if n > 0:
            field = f"{field}_{n}"
        field_counts[field] += 1
        fields.append(field)

    return fields


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputfile")
    parser.add_argument(
            "-o", "--output",
            type=argparse.FileType("wb"),
            help="output file. if not given, assume -, which is stdout",
            default="-")

    return parser.parse_args()


def main(args):
    wb = load_workbook(args.inputfile)

    # assume this is the dictionary one
    ws = wb.active

    field_names = read_column_names(ws.columns)
    Entry = namedtuple("Entry", field_names=field_names)

    lemmas = defaultdict(list)
    n_rows = 0
    for row in islice(ws.rows, 1, None):
        n_rows += 1
        r = Entry(*(col.value for col in row))
        lemmas[(r.WORD, r.WORD_CLASS)].append(r)

    xml_bytestring = dict2xml_bytestring(lemmas)
    args.output.write(xml_bytestring)


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
