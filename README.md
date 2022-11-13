# DSLightshow
A tool for controlling the front lights on the Dualsense (PS5) controller.

## Dependancies
- Python 3.10.6 or above
- [PySimpleGUI](https://www.pysimplegui.org/en/latest/)
- [pydualsense](https://github.com/flok/pydualsense)
- [HIDAPI](https://github.com/libusb/hidapi) (.dll in the same directory)

## Beginner Usage Guide
1. Run `dslightshow.py` or `dslightshow.pyw` (make sure your Dualsense controller is plugged in ***before*** running)
2. For a solid single color, change `Type` to "Solid", change `ColorA` to the desired colors (in RGB format, [simple converter here](https://g.co/kgs/316zKo)), and press `Apply Changes`.
3. For a moving color gradient, change `Type`  to "Pulse", change `ColorA` and `ColorB` to the desired colors (again, RGB format), and press `Apply Changes`
4. For a simple rainbow effect, change `Type` to "Rainbow" and press `Apply Changes`.
5. To save your settings for future use, press `Export` to save your settings as either a `.dsl` or `.txt` file.
6. To load saved settings, press `Import` and select the `.dsl` or `.txt` file created in step 5.

## Light Modes
| Type | Function |
|-|-|
| Solid | Uses `ColorA` as a solid, unchanging color. |
| Pulse | Smoothly interpolates between `ColorA` and `ColorB`, using `Speed` as an approximate speed. |
| Rainbow | Cycles through the rainbow, using `Speed` as an approximate speed. |
| InputDisplay | Not currently implemented. |
