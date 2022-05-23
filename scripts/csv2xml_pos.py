# -*- coding:utf-8 -*-
'''
Script to convert csv into xml.
Usage:
    python3 csv2xml_pos.py <PATH_CSV_FILE>
For each pos, an xml file named <POS>_spasme.xml is generated in this folder.

These files still need to be compiled into a single xml file to be used 
in the dictionary. Read the NDS documentation if you are unsure.
'''

import sys
import csv
import lxml.etree
from lxml.etree import ElementTree as ET
from lxml.etree import Element, SubElement, XMLParser

# Initial checks before running.
if (len(sys.argv) != 2):
    print("Usage: python3 {} <PATH_CSV_FILE>".format(sys.argv[0]))
    exit()

if (sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help"):
    print(__doc__)
    exit()

read_file = sys.argv[1]
pos_dict = {}

# Define an Entry class containing all elements from csv file keeping (almost) same names
class Entry:
    def __init__(self, word, gen, lem_syn, infl, word_cls_5, basic_form, trans_num, restr, sci_name, saami, saami_trans, word_cls_12, expl, trans_syn_1, trans_syn_2, trans_syn_3, trans_syn_4, trans_syn_5, trans_syn_6, spa_ex_1, saami_ex_1, spa_ex_2, saami_ex_2, spa_ex_3, saami_ex_3, spa_ex_4, saami_ex_4, spa_ex_5, saami_ex_5, spa_ex_6, saami_ex_6, spa_ex_7, saami_ex_7):
        self.word = word.strip()
        self.gen = gen.strip()
        self.lem_syn = lem_syn.strip()
        self.infl = infl.strip()
        self.word_cls_5 = word_cls_5.strip()
        self.basic_form = basic_form.strip()
        self.trans_num = trans_num.strip()
        self.restr = restr.strip()
        self.sci_name = sci_name.strip()
        self.saami = saami.strip()
        self.saami_trans = saami_trans.strip()
        self.word_cls_12 = word_cls_12.strip()
        self.expl = expl.strip()
        self.trans_syn_1 = trans_syn_1.strip()
        self.trans_syn_2 = trans_syn_2.strip()
        self.trans_syn_3 = trans_syn_3.strip()
        self.trans_syn_4 = trans_syn_4.strip()
        self.trans_syn_5 = trans_syn_5.strip()
        self.trans_syn_6 = trans_syn_6.strip()
        self.spa_ex_1 = spa_ex_1.strip()
        self.saami_ex_1 = saami_ex_1.strip()
        self.spa_ex_2 = spa_ex_2.strip()
        self.saami_ex_2 = saami_ex_2.strip()
        self.spa_ex_3 = spa_ex_3.strip()
        self.saami_ex_3 = saami_ex_3.strip()
        self.spa_ex_4 = spa_ex_4.strip()
        self.saami_ex_4 = saami_ex_4.strip()
        self.spa_ex_5 = spa_ex_5.strip()
        self.saami_ex_5 = saami_ex_5.strip()
        self.spa_ex_6 = spa_ex_6.strip()
        self.saami_ex_6 = saami_ex_6.strip()
        self.spa_ex_7 = spa_ex_7.strip()
        self.saami_ex_7 = saami_ex_7.strip()

# Check if value exists, if yes create element (optional t_element to add saami_ex together with spa_ex)
#def check_and_insert(value, parent, tag_name, t_element=None):
def check_and_insert(value, parent, tag_name, ppar=None, ppar_tag_name=None, t_element=None):
    value = value.strip()
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
    return

# Read the csv file
with open(read_file) as f:
    lines = f.readlines()

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
            #l_elem = SubElement(lg_elem, "l")
            l_elem = check_and_insert(val.word, lg_elem, "l") # inserted
            l_elem.set("pos", val.word_cls_5)
            l_elem.set("gen", val.gen)
            l_elem.set("syn", val.lem_syn)
            #l_elem.text = val.word
            check_and_insert(val.infl, lg_elem, "lsub")
            mg_elem = SubElement(e_elem, "mg")
            check_and_insert(val.sci_name, mg_elem, "l_sci")
            tg_elem = SubElement(mg_elem, "tg")
            tg_elem.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
            check_and_insert(val.restr, tg_elem, "re")
            check_and_insert(val.expl, tg_elem, "expl")
            t_elem = SubElement(tg_elem, "t")
            t_elem.set("pos", val.word_cls_12)
            t_elem.set("re", val.restr)
            t_elem.set("sci", val.sci_name)
            if val.saami:
                t_elem.text = val.saami
            else:
                t_elem.text = val.saami_trans
            #xg_elem = SubElement(tg_elem, "xg")
            check_and_insert(val.spa_ex_1, "", "x", tg_elem, "xg", [val.saami_ex_1, "xt"])
            check_and_insert(val.spa_ex_2, "", "x", tg_elem, "xg", [val.saami_ex_2, "xt"])
            check_and_insert(val.spa_ex_3, "", "x", tg_elem, "xg", [val.saami_ex_3, "xt"])
            check_and_insert(val.spa_ex_4, "", "x", tg_elem, "xg", [val.saami_ex_4, "xt"])
            check_and_insert(val.spa_ex_5, "", "x", tg_elem, "xg", [val.saami_ex_5, "xt"])
            check_and_insert(val.spa_ex_6, "", "x", tg_elem, "xg", [val.saami_ex_6, "xt"])
            check_and_insert(val.spa_ex_7, "", "x", tg_elem, "xg", [val.saami_ex_7, "xt"])
            #syng_elem = SubElement(mg_elem, "syng")
            check_and_insert(val.trans_syn_1, "", "syn", mg_elem, "syng")
            check_and_insert(val.trans_syn_2, "", "syn", mg_elem, "syng")
            check_and_insert(val.trans_syn_3, "", "syn", mg_elem, "syng")
            check_and_insert(val.trans_syn_4, "", "syn", mg_elem, "syng")
            check_and_insert(val.trans_syn_5, "", "syn", mg_elem, "syng")
            check_and_insert(val.trans_syn_6, "", "syn", mg_elem, "syng")
            added.append(val.word)
        else:
            # select the already existing entry with word = val.word and add mg with different translation
            for l in out_tree.getiterator("l"):
                if l.text == val.word or (val.word.endswith(" ") and l.text == val.word[:-1]): 
                    mg_elem = SubElement((l.getparent()).getparent(), "mg")
                    tg_elem = SubElement(mg_elem, "tg")
                    tg_elem.set('{http://www.w3.org/XML/1998/namespace}lang', "sme")
                    check_and_insert(val.restr, tg_elem, "re")
                    t_elem = SubElement(tg_elem, "t")
                    t_elem.set("pos", val.word_cls_12)
                    t_elem.set("re", val.restr)
                    check_and_insert(val.expl, tg_elem, "expl")
                    t_elem.set("sci", val.sci_name)
                    if val.saami:
                        t_elem.text = val.saami
                    else:
                        t_elem.text = val.saami_trans
                    #xg_elem = SubElement(tg_elem, "xg")
                    check_and_insert(val.spa_ex_1, "", "x", tg_elem, "xg", [val.saami_ex_1, "xt"])
                    check_and_insert(val.spa_ex_2, "", "x", tg_elem, "xg", [val.saami_ex_2, "xt"])
                    check_and_insert(val.spa_ex_3, "", "x", tg_elem, "xg", [val.saami_ex_3, "xt"])
                    check_and_insert(val.spa_ex_4, "", "x", tg_elem, "xg", [val.saami_ex_4, "xt"])
                    check_and_insert(val.spa_ex_5, "", "x", tg_elem, "xg", [val.saami_ex_5, "xt"])
                    check_and_insert(val.spa_ex_6, "", "x", tg_elem, "xg", [val.saami_ex_6, "xt"])
                    check_and_insert(val.spa_ex_7, "", "x", tg_elem, "xg", [val.saami_ex_7, "xt"])
                    #syng_elem = SubElement(mg_elem, "syng")
                    check_and_insert(val.trans_syn_1, "", "syn", mg_elem, "syng")
                    check_and_insert(val.trans_syn_2, "", "syn", mg_elem, "syng")
                    check_and_insert(val.trans_syn_3, "", "syn", mg_elem, "syng")
                    check_and_insert(val.trans_syn_4, "", "syn", mg_elem, "syng")
                    check_and_insert(val.trans_syn_5, "", "syn", mg_elem, "syng")
                    check_and_insert(val.trans_syn_6, "", "syn", mg_elem, "syng")

    # sort according translation number
    value.sort(key=lambda x: x.trans_num)

    ET(out_tree).write(out_file, encoding="UTF-8", pretty_print=True)
    write_file.close()
