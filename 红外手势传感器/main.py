from machine import UART,Pin,Timer,PWM,SPI,time_pulse_us, I2C,freq
import _thread
from time import sleep_us,ticks_us,sleep
import uos
import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
import random
import  math,array
import struct
from apds9960.const import *
from device import APDS9960 as APDS9960

freq(150_000_000)
bus = I2C(0, scl=Pin(21), sda=Pin(20), freq=400_000)

apds = APDS9960(bus)

dirs = {
    APDS9960_DIR_NONE: "none",
    APDS9960_DIR_LEFT: "left",
    APDS9960_DIR_RIGHT: "right",
    APDS9960_DIR_UP: "up",
    APDS9960_DIR_DOWN: "down",
    APDS9960_DIR_NEAR: "near",
    APDS9960_DIR_FAR: "far",
}

apds.setProximityIntLowThreshold(250)

print("Gesture Test")
print("============")
apds.enableGestureSensor()

st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=60_000_000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)

display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=1)
display.fill(st7789.BLACK)

img_up = "/up.bin" #图片文件地址
img_down = "/down.bin" #图片文件地址
img_left = "/left.bin" #图片文件地址
img_right = "/right.bin" #图片文件地址

f_image = open(img_down, 'rb')
for column in range(1,240):
    buf=f_image.read(480)
    display.blit_buffer(buf, 1, column, 240, 1)

while True:
    sleep(0.5)
    if apds.isGestureAvailable():
        motion = apds.readGesture()
        print(motion)
        if (motion == 1) :
            f_image = open(img_left, 'rb')
            for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
        if (motion == 2) :
            f_image = open(img_right, 'rb')
            for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
        if (motion == 3) :
            f_image = open(img_up, 'rb')
            for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
        if (motion == 4) :
            f_image = open(img_down, 'rb')
            for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
        print("Gesture={}".format(dirs.get(motion, "unknown")))

    
  
    

