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

            # print(f"layers:{layers_section}, line:{line}")
            is_item = line.strip().startswith("-")
            is_json_item_start = line.strip()[1:].strip().startswith("{")
            is_json_item_end = line.strip()[1:].strip().endswith("}")
            is_json_item = is_item and is_json_item_start and is_json_item_end
            print(
                f"line startswith -:{is_item}, startswith lbracket: {is_json_item_start}, endswith rbracket:{is_json_item_end}, final:{is_json_item}"
            )

            is_command_key = line.strip().startswith(
                "- LGui"
            ) or line.strip().startswith("- RGui")
            is_shift_key = (
                line.strip().startswith("- LShift")
                or line.strip().startswith("- RShift")
                or line.strip().startswith("- LSFT")
                or line.strip().startswith("- RSFT")
            )
            is_control_key = (
                line.strip().startswith("- LCtrl")
                or line.strip().startswith("- RCtrl")
                or line.strip().startswith("- LCTL")
                or line.strip().startswith("- RCTL")
            )
            is_alt_key = (
                line.strip().startswith("- LAlt")
                or line.strip().startswith("- RAlt")
                or line.strip().startswith("- LALT")
                or line.strip().startswith("- RALT")
            )
            is_backspace_key = line.strip().startswith("- Bksp")
            is_tab_key = line.strip().startswith("- Tab")
            is_space_key = line.strip().startswith("- Space")
            is_enter_key = line.strip().startswith("- Enter")
            is_left_key = line.strip().startswith("- Left")
            is_right_key = line.strip().startswith("- Right")
            is_up_key = line.strip().startswith("- Up")
            is_down_key = line.strip().startswith("- Down")
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
            elif layers_section and is_command_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.apple-keyboard-command$$"
                )
            elif layers_section and is_shift_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.apple-keyboard-shift$$"
                )
            elif layers_section and is_control_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.apple-keyboard-control$$"
                )
            elif layers_section and is_alt_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.apple-keyboard-option$$"
                )
            elif layers_section and is_backspace_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.backspace-outline$$"
                )
            elif layers_section and is_tab_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)]) + "- $$mdi.keyboard-tab$$"
                )
            elif layers_section and is_space_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.keyboard-space$$"
                )
            elif layers_section and is_enter_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)])
                    + "- $$mdi.keyboard-return$$"
                )
            elif layers_section and is_left_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)]) + "- $$mdi.arrow-left$$"
                )
            elif layers_section and is_right_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)]) + "- $$mdi.arrow-right$$"
                )
            elif layers_section and is_up_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)]) + "- $$mdi.arrow-up$$"
                )
            elif layers_section and is_down_key:
                prefix_pos = line.find("- ")
                dst_line = (
                    "".join([" " for i in range(prefix_pos)]) + "- $$mdi.arrow-down$$"
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
                    and data["s"].strip().startswith("TD")
                ):
                    data.pop("s")

                if (
                    isinstance(data, dict)
                    and "s" in data
                    and isinstance(data["s"], str)
                    and data["s"].strip() == "LSFT+"
                ):
                    data.pop("s")

                if (
                    isinstance(data, dict)
                    and "t" in data
                    and isinstance(data["t"], str)
                    and data["t"] == "{  ["
                ):
                    data["t"] = "["

                if (
                    isinstance(data, dict)
                    and "t" in data
                    and isinstance(data["t"], str)
                    and data["t"] == "}  ]"
                ):
                    data["t"] = "]"

                if (
                    isinstance(data, dict)
                    and "t" in data
                    and isinstance(data["t"], str)
                    and data["t"] == "\"  '"
                ):
                    data["t"] = "'"
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
