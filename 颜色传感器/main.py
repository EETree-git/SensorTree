import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
from machine import Pin, SPI, ADC,PWM ,I2C
import time, math,array
from utime import sleep_ms
from test.ltr381 import LTR381

def CalcValue(value,minval,maxval):
    if (value < minval):
        value = minval
    if (value >maxval):
        value = maxval
    calvalue = int( (value - minval) * 255 / (maxval - minval) )   
    return calvalue

def DetecColor(Rval,Gval,Bval):
    if ((Rval>130)and(Gval<50)and(Bval<10) ):
        return "Red    "
    if ((Rval<60)and(Gval>150)and(Bval<60) ):
        return "Green  "
    if ((Rval<60)and(Gval<40)and(Bval>150) ):
        return "Blue   "
    if ((Rval>170)and(Gval>170)and(Bval<60) ):
        return "Yellow "
    if ((Rval<60)and(Gval>170)and(Bval>170) ):
        return "Cyan   "
    if ((Rval>150)and(Gval<100)and(Bval>180) ):
        return "Magenta"
    if ((Rval>200)and(Gval>200)and(Bval>200) ):
        return "White  "
    if ((Rval<30)and(Gval<30)and(Bval<30) ):
        return "Black  "    
    else:
        return "       "    
    
sensor = LTR381()
st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=4000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.BLACK)
display.text(font2, "Color Meter 1.0", 0, 0)
display.text(font2, "by:tinySDR     ", 0, 30)
display.text(font2, "EETREE Feb.2024", 0, 200)
display.text(font2, "R: ", 0, 70)
display.text(font2, "G: ", 0, 100)
display.text(font2, "B: ", 0, 130)

while True:
    
    REDS = sensor.REDS()
    GREENS = sensor.GREENS()
    BLUES = sensor.BLUES()
    REDH= CalcValue(REDS,60,300)
    GREENH = CalcValue(GREENS,160,550)
    BLUEH = CalcValue(BLUES,90,350)
    
    display.text(font2, str(REDS)+"  ", 48, 70)
    display.text(font2, str(GREENS)+"  ", 48, 100)
    display.text(font2, str(BLUES)+"  ", 48, 130)
    display.fill_rect(160, 70, 80,120, st7789.color565(REDH,GREENH,BLUEH))
    display.text(font2, "C: "+ DetecColor(REDH,GREENH,BLUEH), 0, 160)

