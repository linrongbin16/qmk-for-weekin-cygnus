#!/usr/bin/env python3

import json
import logging
import typing

IconsMap = {
    "LGui": "$$mdi.apple-keyboard-command$$",
    "RGui": "$$mdi.apple-keyboard-command$$",
    "LShift": "$$mdi.apple-keyboard-shift$$",
    "RShift": "$$mdi.apple-keyboard-shift$$",
    "LSFT": "$$mdi.apple-keyboard-shift$$",
    "RSFT": "$$mdi.apple-keyboard-shift$$",
    "LCtrl": "$$mdi.apple-keyboard-control$$",
    "RCtrl": "$$mdi.apple-keyboard-control$$",
    "LCTL": "$$mdi.apple-keyboard-control$$",
    "RCTL": "$$mdi.apple-keyboard-control$$",
    "LAlt": "$$mdi.apple-keyboard-option$$",
    "RAlt": "$$mdi.apple-keyboard-option$$",
    "Bksp": "$$mdi.backspace-outline$$",
    "Tab": "$$mdi.keyboard-tab$$",
    "Space": "$$mdi.keyboard-space$$",
    "Enter": "$$mdi.keyboard-return$$",
    "Left": "$$mdi.arrow-left$$",
    "Up": "$$mdi.arrow-up$$",
    "Down": "$$mdi.arrow-down$$",
    "Right": "$$mdi.arrow-right$$",
    "USER00": "U00",
    "USER01": "U01",
    "USER02": "U02",
    "USER03": "U03",
    "USER04": "U04",
    "USER05": "U05",
}


def add_icons(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        for name, value in IconsMap.items():
            pattern = f"- {name}"
            target = f"- {value}"
            result = result.replace(pattern, target)
            pattern = '"' + name + '"'
            target = '"' + value + '"'
            result = result.replace(pattern, target)
        logging.debug(f"Add icon:{result}")
        outputs.append(result)
    return outputs


ShiftedMap = ["LSFT+"] + [f"TD({i})" for i in range(30)]


def remove_shifted(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        for sym in ShiftedMap:
            target = '"s":"' + sym + '",'
            result = result.replace(target, "")
        logging.debug(f"Remove shifted:{result}")
        outputs.append(result)

    return outputs


ShiftedCombosMap = ShiftedMap + [
    '"',
    "_",
    "+",
    "{",
    "}",
]


def remove_shifted_combos(inputs: list[str]) -> list[str]:
    is_combos = False
    outputs = []
    for line in inputs:
        result = line
        if line.strip().startswith("combos"):
            is_combos = True
        if is_combos:
            for sym in ShiftedCombosMap:
                target = '"s":"' + sym + '",'
                result = result.replace(target, "")
        logging.debug(f"Remove shifted combo:{result}")
        outputs.append(result)

    return outputs


TapsMap = {
    "}  ]": {"t": "]", "s": "}"},
    "{  [": {"t": "[", "s": "{"},
    "\"  '": {"t": "'", "s": '"'},
    ":  ;": {"t": ";", "s": ":"},
    "+  =": {"t": "=", "s": "+"},
}


def replace_taps(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        for name, value in TapsMap.items():
            pattern = '"t":"' + name + '"'
            target = '"s":"' + value["s"] + '","t":"' + value["t"] + '"'
            result = result.replace(pattern, target)
        logging.debug(f"Replace tap:{result}")
        outputs.append(result)

    return outputs


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
    with open("vail-layout.yml", "r") as src:
        lines = src.readlines()
        lines = remove_shifted(lines)
        lines = remove_shifted_combos(lines)
        lines = add_icons(lines)
        lines = replace_taps(lines)
        with open("vail-layout-processed.yml", "w") as dst:
            dst.writelines(lines)
