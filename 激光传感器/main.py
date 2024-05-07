import uos
import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
import random
import framebuf
from machine import Pin, SPI, ADC,PWM,I2C,freq
import time, math,array
from utime import sleep_ms
import struct
import vl6180x
freq(180_000_000)

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
display.fill(st7789.BLACK)


buttonM = Pin(5,Pin.IN, Pin.PULL_UP) #B
buttonS = Pin(6,Pin.IN, Pin.PULL_UP) #A
buttonL = Pin(7,Pin.IN, Pin.PULL_UP) #A
buttonPRESS = Pin(8,Pin.IN, Pin.PULL_UP) #A
buttonR = Pin(9,Pin.IN, Pin.PULL_UP) #A

i2c = I2C(0, scl=Pin(21), sda=Pin(20))

TOF=vl6180x.Sensor(i2c)
TOF.init()
TOF.default_settings()


def light_dot(x,y,color):
   display.pixel(x,y,color)

def draw_circle(x,y,r,color,fill=0):
   '''
   绘制圆形
   :param x,y  圆心坐标
   :param r  圆心半径
   :param fill 0 不填充  1 填充
   '''
   angleList = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.7853981633974483, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.5707963267948966, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2.0, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3, 2.35, 2.356194490192345, 2.4, 2.45, 2.5, 2.55, 2.6, 2.65, 2.7, 2.75, 2.8, 2.85, 2.9, 2.95, 3.0, 3.05, 3.1, 3.141592653589793, 3.15, 3.2, 3.25, 3.3, 3.35, 3.4, 3.45, 3.5, 3.55, 3.6, 3.65, 3.7, 3.75, 3.8, 3.85, 3.9, 3.9269908169872414, 3.95, 4.0, 4.05, 4.1, 4.15, 4.2, 4.25, 4.3, 4.35, 4.4, 4.45, 4.5, 4.55, 4.6, 4.65, 4.7, 4.71238898038469, 4.75, 4.8, 4.85, 4.9, 4.95, 5.0, 5.05, 5.1, 5.15, 5.2, 5.25, 5.3, 5.35, 5.4, 5.45, 5.497787143782138, 5.5, 5.55, 5.6, 5.65, 5.7, 5.75, 5.8, 5.85, 5.9, 5.95, 6.0, 6.05, 6.1, 6.15, 6.2, 6.25, 6.283185307179586];
   for i in angleList:
     light_dot(x+round(math.sin(i)*r),y+round(math.cos(i)*r),color)
   if fill:
     powR = math.pow(r,2)
     for xx in range(x-r,x+r):
       for yy in range(y-r,y+r):
         if ( (math.pow(xx-x,2)+math.pow(yy-y,2)) < powR):
           light_dot(xx,yy,color)

current_r = 0
turn = 0
while True :
    print(TOF.range())
    turn += 1
    if TOF.range() <200 :
        current_r = TOF.range() 
    for i in range (current_r,current_r+3) :
        draw_circle(120,120,i,st7789.BLUE+0x10*current_r*turn,fill=0)
    if turn == 50 :
        turn = 0
