#!/usr/bin/env python3

import json

with open("Cygnus-Keymap.yml", "r") as src:
    with open("Cygnus-Keymap-Processed.yml", "w") as dst:
        combos_section = False
        layers_section = False
        for line in src:
            dst_line = line
            if line.strip().startswith("combos:"):
                combos_section = True
                layers_section = False
            elif line.strip().startswith("layers:"):
                combos_section = False
                layers_section = True

            print(f"layers:{layers_section}, line:{line}")
            is_item = line.strip().startswith("-")
            is_json_item_start = line.strip()[1:].strip().startswith("{")
            is_json_item_end = line.strip()[1:].strip().endswith("}")
            is_json_item = is_item and is_json_item_start and is_json_item_end
            print(
                f"line startswith -:{is_item}, startswith lbracket: {is_json_item_start}, endswith rbracket:{is_json_item_end}, final:{is_json_item}"
            )
            if layers_section and line.strip().startswith("- USER"):
                prefix_pos = line.find("- USER")
                index = str(int(line[prefix_pos + 6 :].strip()))
                # print(f"prefix_pos:{prefix_pos}, suffix:{index}")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + '- "User\\n'
                    + index
                    + '"\n'
                )
            elif layers_section and is_json_item:
                prefix = line.find("-")
                data_line = line[prefix + 1 :].strip()
                print(f"data_line:{data_line}")
                data = json.loads(data_line)
                print(f"data-1:{data}")
                if (
                    isinstance(data, dict)
                    and "s" in data
                    and isinstance(data["s"], str)
                    and data["s"] == "LSFT+"
                ):
                    data.pop("s")

                remove_symbols = [
                    {"s": "{", "t": "["},
                    {"s": "}", "t": "]"},
                    {"s": '"', "t": "'"},
                    {"s": "_", "t": "-"},
                    {"s": "+", "t": "="},
                ]
                for rs in remove_symbols:
                    if (
                        isinstance(data, dict)
                        and "s" in data
                        and data["s"] == rs["s"]
                        and "t" in data
                        and data["t"] == rs["t"]
                    ):
                        data.pop("s")
                print(f"data-2:{data}")
                dst_line = (
                    "".join([" " for i in range(prefix)])
                    + "- "
                    + json.dumps(data, separators=(",", ":"), sort_keys=True)
                    + "\n"
                )
                print(f"dst_line:{dst_line}")
            # elif combos_section and line.strip().startswith("- {"):
            #     prefix_pos = line.find("- {")
            #     # print(f"prefix_pos:{prefix_pos}")
            #     data = line[prefix_pos+2:]
            #     # print(f"data-1:{data}")
            #     data = json.loads(data)
            #     # data['d'] = True
            #     if isinstance(data['k'], dict) and isinstance(data['k']['s'], str):
            #         data['k'].pop('s')
            #     # print(f"data-2:{data}")
            #     dst_line = "".join([' ' for i in range(prefix_pos)]) + "- " + json.dumps(data, sort_keys=True) + "\n"
            dst.write(dst_line)
