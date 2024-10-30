# Cygnus-Keymap

My cygnus split keyboard keymap, 3x6 + 3 thumb keys.

<p align="center">
  <img
    alt="left.jpg"
src="https://github.com/user-attachments/assets/77818f71-ea55-4e1b-a305-c8182c44927f"
    width="45%"
  />
  <img
    alt="right.jpg"
src="https://github.com/user-attachments/assets/62fb9ab4-f29f-4834-9fdf-3b0d631bacac"
    width="45%"
  />
</p>

## Layers

The keymap is based on the standard **QWERTY** layout, which I am used to. Three layers are been created:

- L0: Alphabet keys (`a`-`z`) and some keys around them (`ctrl`, `cmd`, `enter`, etc).
- L1: Symbol (`-`, `=`, `,`, `"`, etc), number (`1`-`9`) and navigation (`Up`, `Down`, `Left`, `Right`) keys around the alpha keys.
- L2: Function (`F1`-`F12`), numpad (`1`-`9`, `+`, `-`, `.`, etc) and other keys.

![keymap](my_keymap.svg)

## Special Keys

There are 2 special keys to switch between different layers: `MO(x)` on the left thumb, `TO(x)` on the right thumb.

- To momentarily typing some symbols/numbers/etc, press `MO(x)` to switch to other layers, then release it to go back to default layer-0.
- To long time typing symbols/numbers/etc, press `TO(x)` to go to other layers and done the work, then press `TO(x)` to go back to default layer-0.

## Generate Keymap Layout

1. Create the keymap by [Vial](https://get.vial.today/), and save the keymap into the `Cygnus-Keymap.vil` file.
2. Use the [Vial layout to Keymap Drawer converter](https://yal-tools.github.io/vial-to-keymap-drawer/) to convert the `Cygnus-Keymap.vil` file to yaml contents.
   - Set _**"Keyboard Kind"**_ as `splitkb/aurora/corne/rev1`.
   - Set _**"Layout Name"**_ as `LAYOUT_split_3x6_3`.
   - In _**"Keys out of order or too many keys?"**_ section, select "Omit -1 keys".
3. Use the [Keymap Drawer](https://keymap-drawer.streamlit.app/) to generate SVG picture.
   - Copy the converted yaml contents, and paste into the _**"Keymap YAML"**_ section.
   - Update the _**Configuration**_ with larger size:
     - `key_w=74` (key width)
     - `key_h=70` (key height)
     - `combo_w=38` (combo key width)
     - `combo_h=36` (combo key height)
   - Click the _**"Run"**_ button, then expand the _**"Export"**_ section and download the SVG file.
4. Use the [librsvg](https://wiki.gnome.org/Projects/LibRsvg) to convert SVG to PNG.
   - Install _**librsvg**_ with `brew install librsvg`.
   - Run command `rsvg-convert -z 2 my_keymap.svg > my_keymap.png`.
