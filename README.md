# Dictionary for spa — sme

This repository contains source files for a dictionary from Spanish to North Sámi. The content is licensed under the CC-BY-4.0 license.

Many of the dictionaries are published on [sátni.org](https://sátni.org) and [NDS](https://sanit.oahpa.no).

# Generating the XML file for use in NDS

The `/inc/` directory contains the original Excel source files. Whenever a Giellatekno-style XML file is needed, e.g. in NDS, this should be generated from the (newest) source using Python 3 and the script `scripts/xlsx2xml.py`.

Example usage: `python3 scripts/xlsx2xml.py inc/orig_do_not_change/A_Z_Spanish_Saami_19aug24.xlsx`. More documentation can be found by running the script with `-h`.

# Contributions

Contributions are welcome, just clone and submit a pull request. Or use the in-place editor in GitHub to make your contributions. All contributions must be licensed under the same license as the original code.

# Citing

This dictionary is the work of Ángel Díaz de Rada at UNED and Kjell Kemi at UiT.