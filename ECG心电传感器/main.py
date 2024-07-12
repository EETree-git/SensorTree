import uos
import st7789 as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import framebuf
from machine import Pin, SPI, ADC,PWM,freq
import time, math,array
from utime import sleep_ms
import struct
freq(200_000_000 )

st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=62_000_000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)


display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.BLACK)
display.text(font2, "ECG wave form", 10, 200)

temp = array.array('H', (0 for _ in range(480)))
dis_a=bytearray(480)
dis_b=bytearray(480)
ECG_ADC = ADC(Pin(28))

for i in range (480) :
    temp[i] = ECG_ADC.read_u16()
    dis_a[i]=int(temp[i]/65535*100)
    dis_b[i]=dis_a[i]
    display.pixel(i%240, dis_a[i]+int(i/240)*80, 0xFFFF)

while True:

    for i in range (480) :
        temp[i] = ECG_ADC.read_u16()
        display.pixel(i%240, dis_b[i]+int(i/240)*80, 0x0000)
        dis_a[i]=int(temp[i]/65535*100)
        display.pixel(i%240, dis_a[i]+int(i/240)*80, 0xFFFF)
        dis_b[i]=dis_a[i]

