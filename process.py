#!/usr/bin/env python3

import json
import logging
import typing


KeyboardIconsMap = {
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
}



def add_icons(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        for name, value in KeyboardIconsMap.items():
            result = line.replace(name, value)
        outputs.append(result)
    return outputs


RemoveShiftedMap = ["LSFT+"] + [f"TD({i})" for i in range(30)]


def remove_shifted(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        for sym in RemoveShiftedMap:
            target = '"s":"' + sym + ','
            result = line.replace(target, "")
        outputs.append(result)

    return outputs

RemoveShiftedCombosMap = RemoveShiftedMap + [
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
            for sym in RemoveShiftedCombosMap:
                target = '"s":"' + sym + ','
                result = line.replace(target, "")
        outputs.append(result)

    return outputs

ReplaceSymbols = {
        "}  ]": {"t": "]", "s": "}"},
        "{  [": {"t": "[", "s": "{"},
        "\"  '": {"t": "'", "s": '"'},
        ":  ;": {"t": ";", "s": ":"},
}

def replace_tap_symbols(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = line
        if is_json_item(line):
            try:
                for skey, svalue in ReplaceSymbols.items():
                    line_json_data = json_from_string(line.replace("-", "", 1).strip())
                    if "t" in line_json_data and line_json_data["t"] == skey:
                        line_json_data["t"] = svalue["t"]
                        if "s" not in line_json_data or len(line_json_data["s"]) == 0:
                            line_json_data["s"] = svalue["s"]
                        result = replace_json_item(line, line_json_data)
                        logging.debug(f"Replace symbols: {skey} => {svalue}")
                        logging.debug(f"Line: {result}")
                        break
            except Exception as e:
                logging.error(f"Failed to replace symbols for line: {line}")
                logging.error(e, exc_info=True)
        if not result:
            result = line
        outputs.append(result)

    return outputs


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
    with open("vail-layout.yml", "r") as src:
        lines = src.readlines()
        lines = add_icons(lines)
        lines = remove_shifted(lines)
        lines = remove_shifted_combos(lines)
        lines = replace_tap_symbols(lines)
        with open("vail-layout-processed.yml", "w") as dst:
            dst.writelines(lines)
