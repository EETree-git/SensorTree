from ENS160 import myENS160
from machine import UART,Pin,Timer,PWM,SPI,time_pulse_us, I2C,freq
import _thread
from time import sleep_us,ticks_us,sleep,sleep_ms
import uos
import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
import random
import  math,array
import struct

freq(180_000_000)

obj=myENS160()

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
air_1 = "/air_1.bin" #图片文件地址
air_2 = "/air_2.bin" #图片文件地址
air_3 = "/air_3.bin" #图片文件地址
co2_1 = "/co2_1.bin" #图片文件地址
co2_2 = "/co2_2.bin" #图片文件地址
co2_3 = "/co2_3.bin" #图片文件地址
display.text(font2, "STATE OF AIR", 20, 190, color=st7789.BLUE, background=st7789.WHITE)
display.text(font1, "AQI level", 120, 20, color=st7789.BLUE, background=st7789.WHITE)
display.text(font1, "CO2 level", 120, 110, color=st7789.BLUE, background=st7789.WHITE)
while True:
    TVOC=obj.getTVOC()
    AQI=obj.getAQI()
    ECO2=obj.getECO2()
    print(AQI,TVOC,ECO2)
    if (AQI == 1 or AQI == 2) :
        display.text(font2, str(AQI), 145, 40, color=st7789.GREEN, background=st7789.WHITE)
        f_image = open(air_1, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+30, 48, 1)
    elif (AQI == 3 or AQI == 4)  :
        display.text(font2, str(AQI), 145, 40, color=st7789.YELLOW, background=st7789.WHITE)
        f_image = open(air_2, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+30, 48, 1)
    elif (AQI > 4)  :
        display.text(font2, str(AQI), 145, 40, color=st7789.RED, background=st7789.WHITE)
        f_image = open(air_3, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+30, 48, 1)   
    if (ECO2 < 800) :
        display.text(font2, str(ECO2)+"  ", 130, 130, color=st7789.GREEN, background=st7789.WHITE)
        f_image = open(co2_1, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+120, 48, 1)
    elif (ECO2 > 800 and ECO2 < 1500)  :
        display.text(font2, str(ECO2)+"  ", 130, 130, color=st7789.YELLOW, background=st7789.WHITE)
        f_image = open(co2_2, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+120, 48, 1)
    elif (ECO2 > 1500)  :
        display.text(font2, str(ECO2), 130, 130, color=st7789.RED, background=st7789.WHITE)
        f_image = open(co2_3, 'rb')
        for column in range(1,48):
            buf=f_image.read(96)
            display.blit_buffer(buf, 30, column+120, 48, 1)   
