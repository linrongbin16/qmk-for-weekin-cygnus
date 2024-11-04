#!/usr/bin/env python3

import json

with open('Cygnus-Keymap.yml', 'r') as src:
    with open('Cygnus-Keymap-Processed.yml', 'w') as dst:
        combos_section = False
        for line in src:
            dst_line = line
            if line.strip().startswith("combos:"):
                combos_section = True
            elif line.strip().startswith("- USER"):
                prefix_pos = line.find("- USER")
                index = str(int(line[prefix_pos+6:].strip()))
                # print(f"prefix_pos:{prefix_pos}, suffix:{index}")
                dst_line = "".join([' ' for i in range(prefix_pos)]) + "- \"User\\n" + index + "\"\n"
            elif combos_section and line.strip().startswith("- {"):
                prefix_pos = line.find("- {")
                # print(f"prefix_pos:{prefix_pos}")
                data = line[prefix_pos+2:]
                # print(f"data-1:{data}")
                data = json.loads(data)
                data['d'] = True
                if isinstance(data['k'], dict) and isinstance(data['k']['s'], str):
                    data['k'].pop('s')
                # print(f"data-2:{data}")
                dst_line = "".join([' ' for i in range(prefix_pos)]) + "- " + json.dumps(data, sort_keys=True) + "\n"
            dst.write(dst_line)

