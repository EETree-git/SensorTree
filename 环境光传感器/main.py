from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import Pin, SPI
from utime import sleep
import math,array
#------------------------------------------------------------------
######################################################################




#全局变量
current_temp = 0     
#-------------------------------------------------------------------

#屏幕基本图形绘制
def display_init():  
  
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,6)
    display.set_pen(255,0,0)

    display.text("current", 150, 20, 194, 2)
    display.text("light", 150, 35, 194, 2)

    display.update()
  
    for i in range(6):
        display.set_pen(0,200,0)
        display.pixel_span(80,27 + i*30,10)
        display.text(str(100 - i *20), 100, 20+i*30, 194, 2)
        display.set_pen(0,0,220)
        if i < 5:
            for j in range(4):
                display.pixel_span(80,33 + j*6 + i * 30,5)
        display.update()
   
    display.update()
#---------------------------------------------------------------------
 
def display_change(temp, color):
    global current_temp
    current_temp = temp
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(58,30,13,160)
    display.circle(64,190,5)
    display.set_pen(0,0,150)
    display.rectangle(58,20,13,7+int((50-temp/2)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(150,50,90,40)
    display.set_pen(0,255,0)
    display.text(str(temp), 150, 50, 5, 5)
    display.update()

#-----------------------------------------------------------------------

def read_adc():
    CS.off()
    data = TEMP_spi.read(2)
    value = (data[1]) | (data[0]<<8)
    value = value / 4096 *100
    CS.on()
    return value

#显示屏
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)

display = BreakoutColourLCD240x240(display_buffer)

color = [0,255,0]     

display_init()
while True:
    TEMP_spi = SPI(0,1000000,miso = Pin(20,Pin.OUT),sck = Pin(22,Pin.OUT))
    CS = Pin(21,Pin.OUT)
    display_change(round(read_adc(),1), color)
    


