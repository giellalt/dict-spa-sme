# -*- coding:utf-8 -*-
'''
Script to convert csv into xml.
Usage:
    python3 csv2xml_pos.py <PATH_CSV_FILE>
For each pos, an xml file named <POS>_spasme.xml is generated in this folder.
'''

import sys
import csv
from lxml.etree import ElementTree as ET
from lxml.etree import Element, SubElement, XMLParser

read_file = sys.argv[1]

pos_dict = {}
# Define an Entry class containing lemma, pos, gender, lemma synonym, translation, and translation pos
class Entry:
    def __init__(self, lemma, pos, gen, lem_syn, trans, trans_pos):
        self.lemma = lemma
        self.pos = pos
        self.gen = gen
        self.lem_syn = lem_syn
        self.trans = trans
        self.trans_pos = trans_pos

# Read the csv file
with open(read_file) as f:
    lines = f.readlines()
f.close()

# Create a dictionary of entries collected by pos
for i in range(1, len(lines)):
    line = lines[i].split('\t')
    pos = line[4]
    if not pos in pos_dict:
        pos_dict[pos] = [Entry(line[0], line[4], line[1], line[2], line[9], line[11])]
    else:
        el = pos_dict[pos]
        pos_dict[pos].append(Entry(line[0], line[4], line[1], line[2], line[9], line[11]))

# Create an xml file per pos by reading the dictionary (dict_pos)
for key, value in pos_dict.items():
    out_file = "../src/" + key.replace(" ", "_").replace("/", "#").upper() + "_spasme.xml"
    write_file = open(out_file,"a+")
    out_tree = Element("r")
    added = []
    for val in value:
        # create first entry with lemma = val.lemma
        if not val.lemma in added:
            e_elem = SubElement(out_tree, "e")
            lg_elem = SubElement(e_elem, "lg")
            l_elem = SubElement(lg_elem, "l")
            l_elem.set("pos", val.pos)
            l_elem.set("gen", val.gen)
            l_elem.text = val.lemma
            mg_elem = SubElement(e_elem, "mg")
            tg_elem = SubElement(mg_elem, "tg")
            tg_elem.set("lang", "sme")
            re_elem = SubElement(tg_elem, "re")
            re_elem.text = val.lem_syn
            t_elem = SubElement(tg_elem, "t")
            t_elem.set("pos", val.trans_pos)
            t_elem.text = val.trans
            added.append(val.lemma)
        else:
            # select the already existing entry with lemma = val.lemma and add mg with different translation
            for l in out_tree.getiterator("l"):
                if l.text == val.lemma:
                    mg_elem = SubElement((l.getparent()).getparent(), "mg")
                    tg_elem = SubElement(mg_elem, "tg")
                    tg_elem.set("lang", "sme")
                    re_elem = SubElement(tg_elem, "re")
                    re_elem.text = val.lem_syn
                    t_elem = SubElement(tg_elem, "t")
                    t_elem.set("pos", val.trans_pos)
                    t_elem.text = val.trans
    ET(out_tree).write(out_file, encoding="UTF-8", pretty_print=True)
    write_file.close()
