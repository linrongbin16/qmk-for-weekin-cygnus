#!/usr/bin/env python3

import json
import logging
import typing


def is_json_item(line: str) -> bool:
    if not line.strip().startswith("-"):
        return False
    striped_line = line.strip()
    if not striped_line[1:].strip().startswith("{"):
        return False
    if not striped_line[-1:].strip().startswith("}"):
        return False
    return True


def json_to_string(o: typing.Any) -> str:
    return json.dumps(o, sort_keys=True, separators=(",", ":"))


def json_from_string(s: str) -> dict:
    return json.loads(s)


def replace_json_item(line: str, o: typing.Any) -> str:
    prefix = line.find("-")
    result = "".join([" " for i in range(prefix)]) + f"- " + json_to_string(o) + "\n"
    return result


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


def process_icon(line: str) -> str:
    try:
        for name, value in KeyboardIconsMap.items():
            if line.strip().startswith(f"- {name}"):
                result = line.replace(name, value)
                logging.debug(f"Replace keyboard icon: {name} => {value}")
                logging.debug(f"Line: {result}")
                return result
            elif is_json_item(line):
                line_json_data = json_from_string(line.replace("-", "", 1).strip())
                has_replaced = False
                for name, value in KeyboardIconsMap.items():
                    if "s" in line_json_data and line_json_data["s"] == name:
                        logging.debug(
                            f"Replace keyboard icon on 's'(shifted): {name} => {value}"
                        )
                        line_json_data["s"] = value
                        has_replaced = True
                    if "t" in line_json_data and line_json_data["t"] == name:
                        logging.debug(
                            f"Replace keyboard icon on 't'(tap): {name} => {value}"
                        )
                        line_json_data["t"] = value
                        has_replaced = True
                    if "h" in line_json_data and line_json_data["h"] == name:
                        logging.debug(
                            f"Replace keyboard icon on 'h'(hold): {name} => {value}"
                        )
                        line_json_data["h"] = value
                        has_replaced = True
                    if "k" in line_json_data and line_json_data["k"] == name:
                        logging.debug(
                            f"Replace keyboard icon on 'k'(combo): {name} => {value}"
                        )
                        line_json_data["k"] = value
                        has_replaced = True
                    if has_replaced:
                        result = replace_json_item(line, line_json_data)
                        logging.debug(f"Line: {result}")
                        return result
    except Exception as e:
        logging.error(f"Failed to replace keyboard icon for line: {line}")
        logging.error(e, exc_info=True)

    return line


def add_icons(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        outputs.append(process_icon(line))
    return outputs


def add_icons_for_combos(inputs: list[str]) -> list[str]:
    is_combos = False
    outputs = []
    for line in inputs:
        result = None
        if line.strip().startswith("combos"):
            is_combos = True
        if is_combos:
            result = process_icon(line)
        if not result:
            result = line
        outputs.append(result)
    return outputs


RemoveShiftedSymbolssMap = [
    "LSFT+",
    '"',
    "_",
    "+",
    "{",
    "}",
] + [f"TD({i})" for i in range(30)]


def process_shifted(line: str) -> str:
    if is_json_item(line):
        try:
            for sym in RemoveShiftedSymbolssMap:
                line_json_data = json_from_string(line.replace("-", "", 1).strip())
                if "s" in line_json_data and line_json_data["s"] == sym:
                    line_json_data.pop("s")
                    result = replace_json_item(line, line_json_data)
                    logging.debug(f"Remove shifted symbol: {sym}")
                    logging.debug(f"Line: {result}")
                    return result
        except Exception as e:
            logging.error(f"Failed to remove symbols for line: {line}")
            logging.error(e, exc_info=True)

    return line


def remove_shifted(inputs: list[str]) -> list[str]:
    outputs = []
    for line in inputs:
        result = process_shifted(line)
        outputs.append(result)

    return outputs


def remove_shifted_for_combos(inputs: list[str]) -> list[str]:
    RemoveSymbols = ["LSFT+", "{", "}"]

    is_combos = False
    outputs = []
    for line in inputs:
        result = None
        if line.strip().startswith("combos"):
            is_combos = True
        if is_combos and is_json_item(line):
            try:
                for symbol in RemoveSymbols:
                    line_json_data = json_from_string(line.replace("-", "", 1).strip())
                    if (
                        "k" in line_json_data
                        and "s" in line_json_data["k"]
                        and line_json_data["k"]["s"] == symbol
                    ):
                        line_json_data["k"].pop("s")
                        result = replace_json_item(line, line_json_data)
                        logging.debug(f"Remove symbols for combo: {symbol}")
                        logging.debug(f"Line: {result}")
                        break
            except Exception as e:
                logging.error(f"Failed to remove symbols for combo line: {line}")
                logging.error(e, exc_info=True)
        if not result:
            result = line
        outputs.append(result)

    return outputs


def replace_t_symbols(inputs: list[str]) -> list[str]:
    ReplaceSymbols = {
        "}  ]": {"t": "]", "s": "}"},
        "{  [": {"t": "[", "s": "{"},
        "\"  '": {"t": "'", "s": '"'},
        ":  ;": {"t": ";", "s": ":"},
    }

    outputs = []
    for line in inputs:
        result = None
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
        lines = add_icons_for_combos(lines)
        lines = remove_shifted(lines)
        lines = remove_shifted_for_combos(lines)
        lines = replace_t_symbols(lines)
        with open("vail-layout-processed.yml", "w") as dst:
            dst.writelines(lines)
