# -*- coding:utf-8 -*-
import sys
import csv
from lxml.etree import ElementTree as ET
from lxml.etree import Element, SubElement, XMLParser

read_file = sys.argv[1]
out_file = "out.xml"
out_tree = Element("r")
write_file = open(out_file,"a+")

with open(read_file) as f:
    lines = f.readlines()

for i in range(1, len(lines)):
    line = lines[i].split('\t')
    if i == 1:
        prev = ''
        current = line[0]
    else:
        prev = lines[i-1].split('\t')[0].decode("utf-8")
        current = line[0].decode("utf-8")
    if not prev == current:
        e_elem = SubElement(out_tree, "e")
        lg_elem = SubElement(e_elem, "lg")
        l_elem = SubElement(lg_elem, "l")
        l_elem.set("pos", line[4].decode("utf-8"))
        l_elem.set("gen", line[1].decode("utf-8"))
        l_elem.text = line[0].decode("utf-8")
        mg_elem = SubElement(e_elem, "mg")
        tg_elem = SubElement(mg_elem, "tg")
        tg_elem.set("lang", "sme")
        re_elem = SubElement(tg_elem, "re")
        re_elem.text = line[2].decode("utf-8")
        t_elem = SubElement(tg_elem, "t")
        t_elem.set("pos", line[11].decode("utf-8"))
        t_elem.text = line[9].decode("utf-8")
    elif prev == current:
        for l in out_tree.getiterator("l"):
            if l.text == current:
                mg_elem = SubElement((l.getparent()).getparent(), "mg")
                tg_elem = SubElement(mg_elem, "tg")
                tg_elem.set("lang", "sme")
                re_elem = SubElement(tg_elem, "re")
                re_elem.text = line[2].decode("utf-8")
                t_elem = SubElement(tg_elem, "t")
                t_elem.set("pos", line[11].decode("utf-8"))
                t_elem.text = line[9].decode("utf-8")

ET(out_tree).write(out_file, encoding="UTF-8", pretty_print=True)
write_file.close()
