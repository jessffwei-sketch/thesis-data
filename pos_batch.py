#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import re

TAG2COARSE = {
    "CC": "CONJ",
    "CD": "NUM",
    "DT": "DET",
    "PDT": "DET",
    "WDT": "DET",

    "EX": "EXIST",
    "FW": "FOREIGN",

    "IN": "PREP",
    "IN/that": "PREP",

    "JJ": "ADJ",
    "JJR": "ADJ",
    "JJS": "ADJ",

    "LS": "LIST",
    "MD": "VERB",

    "NN": "NOUN",
    "NNS": "NOUN",
    "NP": "NOUN",
    "NPS": "NOUN",

    "POS": "GENITIVE",

    "PP": "PRON",
    "PP$": "PRON",
    "WP": "PRON",
    "WP$": "PRON",

    "RB": "ADV",
    "RBR": "ADV",
    "RBS": "ADV",
    "WRB": "ADV",

    "RP": "PARTICLE",
    "TO": "TO",
    "UH": "INTERJ",

    "VB": "VERB",
    "VBD": "VERB",
    "VBG": "VERB",
    "VBN": "VERB",
    "VBZ": "VERB",
    "VBP": "VERB",

    "VD": "VERB",
    "VDD": "VERB",
    "VDG": "VERB",
    "VDN": "VERB",
    "VDZ": "VERB",
    "VDP": "VERB",

    "VH": "VERB",
    "VHD": "VERB",
    "VHG": "VERB",
    "VHN": "VERB",
    "VHZ": "VERB",
    "VHP": "VERB",

    "VV": "VERB",
    "VVD": "VERB",
    "VVG": "VERB",
    "VVN": "VERB",
    "VVP": "VERB",
    "VVZ": "VERB",

    "SENT": "PUNCT_SENT",
    "SYM": "SYMBOL",
    ":": "JOINER",
    "$": "CURRENCY",
}

# POS 本身如果是纯符号（比如 "," ":" "--"）就删掉
PUNCT_ONLY = re.compile(r"^(?:[,.;:!?()\[\]{}\"“”‘’'`]+|``|''|--|—|-)+$")

# “只统计词性”：这些直接不输出
EXCLUDE_POS = {"SENT", "SYM", ":", "$", "POS"}


def tagged_line_to_coarse(line: str) -> str:
    out = []
    for tok in line.split():
        fine = tok.rsplit("_", 1)[-1] if "_" in tok else tok

        if PUNCT_ONLY.match(fine):
            continue
        if fine in EXCLUDE_POS:
            continue

        out.append(TAG2COARSE.get(fine, "UNK"))
    return " ".join(out)


def main():
    here = Path(__file__).resolve().parent
    files = sorted(here.glob("*.TAGGED.txt"))
    if not files:
        print("No *.TAGGED.txt found in:", here)
        return

    for inp in files:
        text = inp.read_text(encoding="utf-8", errors="replace")
        out_lines = [tagged_line_to_coarse(ln) for ln in text.splitlines()]
        outp = inp.with_name(inp.name.replace(".TAGGED.txt", ".COARSEonly_wordsOnly.txt"))
        outp.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print("Wrote:", outp.name)

    print("Done. Converted:", len(files), "files.")


if __name__ == "__main__":
    main()