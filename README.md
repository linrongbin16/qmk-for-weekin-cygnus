# QMK keymap for Weekin's cygnus keyboard

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

## Layout

The layout is based on the standard **QWERTY** layout, working for macOS. Three layers are been created:

![keymap](my_keymap.png)

## Drawer

1. Create the layout by [Vial](https://get.vial.today/), and save to the `vial-layout.vil` file.
2. Use the [Vial layout to Keymap Drawer converter](https://yal-tools.github.io/vial-to-keymap-drawer/) to convert the `vail-layout.vil` file to yaml contents.

   - Set _**"Keyboard Kind"**_ as `splitkb/aurora/corne/rev1`.
   - Set _**"Layout Name"**_ as `LAYOUT_split_3x6_3`.
   - In _**"Keys out of order or too many keys?"**_ section, select "Omit -1 keys".

3. Use the [Keymap Drawer](https://keymap-drawer.streamlit.app/) to generate SVG picture.

   - Copy the converted yaml contents, and paste into the _**"Keymap YAML"**_ section.
   - Click the _**"Run"**_ button, then expand the _**"Export"**_ section and download the SVG file.
