"""
Convert spanish-sme xlsx to GT-style xml.
"""
import argparse
from itertools import islice
from collections import defaultdict, namedtuple
from pathlib import Path

MISSING_DEP_HELP = """
cannot run due to missing dependencies. hint, run:
python -m venv .venv && . .venv/bin/activate && pip install -r xlsx2xml-requirements.txt
...and then try again. (remember to run `deactivate` in the shell when you're done)
"""

try:
    from lxml.etree import Element, SubElement, tostring
    from openpyxl import load_workbook
except ImportError:
    exit(MISSING_DEP_HELP)


# UNUSED: SEE COMMENT in clean_pos()

# In the WORD_CLASS_SAAMI field, there are many poses
# where the lemma consists of many words, so we just
# treat them all as the giellatekno-known pos "Phrase"
PHRASE_POSES = {
    "Lc", "VLc", "AdvLc", "PronLc", "Pfs", "PrLc", "NLc",
    "ALc"
}


#  expected_column_names = (
#      "WORD",  # lemma, <l.text>
#      "GENDER",  # attribute on <l>
#      "LEMMA_SYNONYM",  # l.syn
#      "INFLECTION",  # mg / <l_sci>
#      "WORD_CLASS_SPANISH",  # pos, attribute "pos" on <l>
#      "BASIC_WORD",  # unused
#      "TRANSLATION_NUMBER",
#      "RESTRICTION",  # tg -> <re> if not none
#      "SCIENTIFIC_NAME",  # mg -> <l_sci> if not none
#      "SAAMI",  # t value  if not none, else:
#      "SAAMI_TRANSLATION_CASE_OR_FORM",  # .. this is t value
#      "WORD_CLASS_SAAMI",  # t.pos if not none
#      "EXPLANATION",   # tg -> <expl> if not none
#      "TRANS_SYNON1",
#      "TRANS_SYNON2",
#      "TRANS_SYNON3",
#      "TRANS_SYNON4",
#      "TRANS_SYNON5",
#      "TRANS_SYNON6",
#      "SPANISH_EX_1",
#      "SAAMI_EX_1",
#      "SPANISH_EX_2",
#      "SAAMI_EX_2",
#      "SPANISH_EX_3",
#      "SAAMI_EX_3",
#      "SPANISH_EX_4",
#      "SAAMI_EX_4",
#      "SPANISH_EX_5",
#      "SAAMI_EX_5",
#      "SPANISH_EX_6",
#      "SAAMI_EX_6",
#      "SPANISH_EX_7",
#      "SAAMI_EX_7",
#  )


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


def slice_until(string, char):
    """Slice the string from the beginning, up to (but not including) where
    the first `char` is found, or slice the entire string if char is not found.
    """
    i = string.find(char)
    if i == -1:
        i = len(string)
    return string[0:i]


def clean_pos(pos):
    # UNUSED
    # FOR NOW, THE DTD IS DEFINED TO TAKE POSES AS
    # A FREE TEXT FIELD (OPTIONAL ON <l>), INSTEAD OF
    # A GIVEN LIST. SO WE DONT NEED TO DO ANY SPECIAL
    # HANDLING OF POSES HERE

    # In WORD_CLASS_SAAMI, there are often more tags,
    # separated by commas, but the first one always
    # seems to be the actual pos
    #pos = slice_until(pos, ",")

    #if pos in PHRASE_POSES:
    #    pos = "Phrase"

    return pos


def t(entry, parent_tg, parent_mg):
    el = SubElement(parent_tg, "t")
    pos = entry.WORD_CLASS_SAAMI  # Previously WORD_CLASS_1
    if pos:
        el.set("pos", clean_pos(pos))
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
    for (lemma, pos, gender), entries in d.items():
        # all_synonyms_are_the_same = all(
        #     entry.LEMMA_SYNONYM == entries[0].LEMMA_SYNONYM
        #     for entry in entries
        # )
        # assert all_synonyms_are_the_same

        e = SubElement(root, "e")
        lg = SubElement(e, "lg")
        l = SubElement(lg, "l")
        if pos is not None:
            l.set("pos", clean_pos(pos))
        if gender is not None:
            l.set("gen", gender)
        if entries[0].LEMMA_SYNONYM is not None:
            l.set("syn", entries[0].LEMMA_SYNONYM)
        l.text = lemma

        for entry in entries:
            if not hasattr(entry, 'LEMMA'): # Protection against empty lines being parsed
                continue
            mg = SubElement(e, "mg")
            check_and_insert(entry.SCIENTIFIC_NAME, mg, "l_sci")
            tg = SubElement(mg, "tg")
            tg.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
            check_and_insert(entry.RESTRICTION, tg, "re")
            check_and_insert(entry.EXPLANATION, tg, "expl")
            check_and_insert(entry.INFLECTION, lg, "lsub")
            t(entry, tg, mg)
            previous = entry

    doctype = (
        '<!DOCTYPE r PUBLIC "-//DivvunGiellatekno//DTD '
        'Dictionaries//Multilingual" "../dtd/spasme.dtd">'
    )
    return tostring(root, encoding="utf-8", pretty_print=True, doctype=doctype)


def read_column_names(columns):
    field_counts = defaultdict(int)
    fields = []
    for col in columns:
        orig_field = field = col[0].value.replace(" ", "_")
        n = field_counts[orig_field]
        if n > 0:
            field = f"{field}_{n}"
        field_counts[orig_field] += 1
        fields.append(field)

    return fields


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputfile")
    parser.add_argument("outputfile", type=Path)

    return parser.parse_args()


def main(args):
    wb = load_workbook(args.inputfile)

    # assume this is the dictionary one
    ws = wb.active

    field_names = read_column_names(ws.columns)
    Entry = namedtuple("Entry", field_names=field_names)

    lemmas = defaultdict(list)
    for row in islice(ws.rows, 1, None):
        e = Entry(*(
            col.value.strip() if isinstance(col.value, str) else col.value
            for col in row
        ))

        lemmas[(e.WORD, e.WORD_CLASS_SPANISH, e.GENDER)].append(e)

    args.outputfile.parent.mkdir(exist_ok=True)
    xml_bytestring = dict2xml_bytestring(lemmas)
    with open(args.outputfile, "wb") as f:
        f.write(xml_bytestring)


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
