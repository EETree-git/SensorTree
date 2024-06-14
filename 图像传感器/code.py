# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
Capture an image from the camera and display it on a supported LCD.
"""

import time
from displayio import (
    Bitmap,
    Group,
    TileGrid,
    FourWire,
    release_displays,
    ColorConverter,
    Colorspace,
)

from adafruit_st7789 import ST7789
import board
import busio
import digitalio
import adafruit_ov2640

release_displays()
# Set up the display (You must customize this block for your display!)
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)
display_bus = FourWire(spi, command=board.GP1, chip_select=board.GP4, reset=board.GP0,
                       baudrate = 80_000_000,
                       polarity = 1,phase = 1)
display = ST7789(display_bus, width=240, height=240, rowstart=80,rotation=90)
display.auto_refresh = False

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

# with digitalio.DigitalInOut(board.GP10) as reset:
#     reset.switch_to_output(False)
#     time.sleep(0.001)
bus = busio.I2C(scl=board.GP13, sda=board.GP12)

# Set up the camera (you must customize this for your board!)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=[
        board.GP15,
        board.GP16,
        board.GP17,
        board.GP18,
        board.GP19,
        board.GP20,
        board.GP21,
        board.GP22,
    ],  # [16]     [org] etc
    clock=board.GP14,  # [15]     [blk]
    vsync=board.GP26,  # [10]     [brn]
    href=board.GP27,  # [27/o14] [red]
#     mclk=board.GP20,  # [16/o15]
#     shutdown=None,
#     reset=board.GP10,
)  # [14]

width = display.width
height = display.height

cam.size = adafruit_ov2640.OV2640_SIZE_240X240 
cam.colorspace = adafruit_ov2640.OV2640_COLOR_RGB
# cam.test_pattern = True
bitmap = Bitmap(cam.width, cam.height, 65536)

print(width, height, cam.width, cam.height)
if bitmap is None:
    raise SystemExit("Could not allocate a bitmap")

g = Group(scale=1, x=(width - cam.width) // 2, y=(height - cam.height) // 2)
tg = TileGrid(
    bitmap, pixel_shader=ColorConverter(input_colorspace=Colorspace.RGB565_SWAPPED)
)
g.append(tg)
display.root_group = g

display.auto_refresh = False
while True:
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)

