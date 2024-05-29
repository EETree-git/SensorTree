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

freq(180_000_000)
alarm_pin = Pin(20,Pin.IN)

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
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.WHITE)

water_empty = "/water_empty.bin" #图片文件地址
water_full = "/water_full.bin" #图片文件地址

display.text(font2, "STATE OF WATER CUP", 10, 190, color=st7789.GREEN, background=st7789.WHITE)
display.text(font2, "EMPTY", 130, 100, color=st7789.RED, background=st7789.WHITE)
while True:
    if (alarm_pin.value() == 1) :
        display.text(font2, "FULL  ", 130, 100, color=st7789.BLUE, background=st7789.WHITE)
        f_image = open(water_full, 'rb')
        for column in range(1,128):
            buf=f_image.read(256)
            display.blit_buffer(buf, 1, column, 128, 1)
    else :
        display.text(font2, "EMPTY", 130, 100, color=st7789.RED, background=st7789.WHITE)
        f_image = open(water_empty, 'rb')
        for column in range(1,128):
            buf=f_image.read(256)
            display.blit_buffer(buf, 1, column, 128, 1)
        
    
  
    

