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

# Define an Entry class containing all elements from csv file keeping (almost) same names
class Entry:
    def __init__(self, word, gen, lem_syn, infl, word_cls_5, basic_form, trans_num, restr, sci_name, saami, saami_trans, word_cls_12, expl, trans_syn_1, trans_syn_2, trans_syn_3, trans_syn_4, trans_syn_5, trans_syn_6, spa_ex_1, saami_ex_1, spa_ex_2, saami_ex_2, spa_ex_3, saami_ex_3, spa_ex_4, saami_ex_4, spa_ex_5, saami_ex_5, spa_ex_6, saami_ex_6, spa_ex_7, saami_ex_7):
        self.word = word
        self.gen = gen
        self.lem_syn = lem_syn
        self.infl = infl
        self.word_cls_5 = word_cls_5
        self.basic_form = basic_form
        self.trans_num = trans_num
        self.restr = restr
        self.sci_name = sci_name
        self.saami = saami
        self.saami_trans = saami_trans
        self.word_cls_12 = word_cls_12
        self.expl = expl
        self.trans_syn_1 = trans_syn_1
        self.trans_syn_2 = trans_syn_2
        self.trans_syn_3 = trans_syn_3
        self.trans_syn_4 = trans_syn_4
        self.trans_syn_5 = trans_syn_5
        self.trans_syn_6 = trans_syn_6
        self.spa_ex_1 = spa_ex_1
        self.saami_ex_1 = saami_ex_1
        self.spa_ex_2 = spa_ex_2
        self.saami_ex_2 = saami_ex_2
        self.spa_ex_3 = spa_ex_3
        self.saami_ex_3 = saami_ex_3
        self.spa_ex_4 = spa_ex_4
        self.saami_ex_4 = saami_ex_4
        self.spa_ex_5 = spa_ex_5
        self.saami_ex_5 = saami_ex_5
        self.spa_ex_6 = spa_ex_6
        self.saami_ex_6 = saami_ex_6
        self.spa_ex_7 = spa_ex_7
        self.saami_ex_7 = saami_ex_7

# Check if value exists, if yes create element (optional t_element to add saami_ex together with spa_ex)
def check_and_insert(value, parent, tag_name, t_element=None):
    if value:
        element = SubElement(parent, tag_name)
        element.text = value
        if t_element:
            if t_element[0]:
                element = SubElement(t_element[1], t_element[2])
                element.text = t_element[0]
    return

# Read the csv file
with open(read_file) as f:
    lines = f.readlines()
f.close()

# Create a dictionary of entries collected by pos
for i in range(1, len(lines)):
    line = lines[i].split('\t')
    pos = line[4]
    if not pos in pos_dict:
        pos_dict[pos] = [Entry(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], line[20], line[21], line[22], line[23], line[24], line[25], line[26], line[27], line[28], line[29], line[30], line[31], line[32])]
    else:
        el = pos_dict[pos]
        pos_dict[pos].append(Entry(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], line[20], line[21], line[22], line[23], line[24], line[25], line[26], line[27], line[28], line[29], line[30], line[31], line[32]))

# Create an xml file per pos by reading the dictionary (dict_pos)
for key, value in pos_dict.items():
    out_file = "../src/" + key.replace(" ", "_").replace("/", "#").upper() + "_spasme.xml"
    write_file = open(out_file,"a+")
    out_tree = Element("r")
    added = []
    for val in value:
        # create first entry with word = val.word
        if not val.word in added:
            e_elem = SubElement(out_tree, "e")
            lg_elem = SubElement(e_elem, "lg")
            l_elem = SubElement(lg_elem, "l")
            l_elem.set("pos", val.word_cls_5)
            l_elem.set("gen", val.gen)
            l_elem.set("syn", val.lem_syn)
            l_elem.text = val.word
            check_and_insert(val.infl, lg_elem, "lsub")
            mg_elem = SubElement(e_elem, "mg")
            tg_elem = SubElement(mg_elem, "tg")
            tg_elem.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
            check_and_insert(val.restr, tg_elem, "re")
            t_elem = SubElement(tg_elem, "t")
            t_elem.set("pos", val.word_cls_12)
            t_elem.set("re", val.restr)
            t_elem.set("sci", val.sci_name)
            t_elem.text = val.saami
            xg_elem = SubElement(tg_elem, "xg")
            check_and_insert(val.spa_ex_1, xg_elem, "x", [val.saami_ex_1, xg_elem, "xt"])
            check_and_insert(val.spa_ex_2, xg_elem, "x", [val.saami_ex_2, xg_elem, "xt"])
            check_and_insert(val.spa_ex_3, xg_elem, "x", [val.saami_ex_3, xg_elem, "xt"])
            check_and_insert(val.spa_ex_4, xg_elem, "x", [val.saami_ex_4, xg_elem, "xt"])
            check_and_insert(val.spa_ex_5, xg_elem, "x", [val.saami_ex_5, xg_elem, "xt"])
            check_and_insert(val.spa_ex_6, xg_elem, "x", [val.saami_ex_6, xg_elem, "xt"])
            check_and_insert(val.spa_ex_7, xg_elem, "x", [val.saami_ex_7, xg_elem, "xt"])
            syng_elem = SubElement(mg_elem, "syng")
            check_and_insert(val.trans_syn_1, syng_elem, "syn")
            check_and_insert(val.trans_syn_2, syng_elem, "syn")
            check_and_insert(val.trans_syn_3, syng_elem, "syn")
            check_and_insert(val.trans_syn_4, syng_elem, "syn")
            check_and_insert(val.trans_syn_5, syng_elem, "syn")
            check_and_insert(val.trans_syn_6, syng_elem, "syn")
            added.append(val.word)
        else:
            # select the already existing entry with word = val.word and add mg with different translation
            for l in out_tree.getiterator("l"):
                if l.text == val.word:
                    mg_elem = SubElement((l.getparent()).getparent(), "mg")
                    tg_elem = SubElement(mg_elem, "tg")
                    tg_elem.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
                    check_and_insert(val.restr, tg_elem, "re")
                    t_elem = SubElement(tg_elem, "t")
                    t_elem.set("pos", val.word_cls_12)
                    t_elem.set("re", val.restr)
                    t_elem.set("sci", val.sci_name)
                    t_elem.text = val.saami
                    xg_elem = SubElement(tg_elem, "xg")
                    check_and_insert(val.spa_ex_1, xg_elem, "x", [val.saami_ex_1, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_2, xg_elem, "x", [val.saami_ex_2, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_3, xg_elem, "x", [val.saami_ex_3, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_4, xg_elem, "x", [val.saami_ex_4, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_5, xg_elem, "x", [val.saami_ex_5, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_6, xg_elem, "x", [val.saami_ex_6, xg_elem, "xt"])
                    check_and_insert(val.spa_ex_7, xg_elem, "x", [val.saami_ex_7, xg_elem, "xt"])
                    syng_elem = SubElement(mg_elem, "syng")
                    check_and_insert(val.trans_syn_1, syng_elem, "syn")
                    check_and_insert(val.trans_syn_2, syng_elem, "syn")
                    check_and_insert(val.trans_syn_3, syng_elem, "syn")
                    check_and_insert(val.trans_syn_4, syng_elem, "syn")
                    check_and_insert(val.trans_syn_5, syng_elem, "syn")
                    check_and_insert(val.trans_syn_6, syng_elem, "syn")
    ET(out_tree).write(out_file, encoding="UTF-8", pretty_print=True)
    write_file.close()
