from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM,I2C
from utime import sleep
import time, math,array
#------------------------------------------------------------------

#初始化

width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)


stemp = ADC(2)  

global x,current_temp                
current_temp = 0               
#-------------------------------------------------------------------
#屏幕基本图形绘制
def display_init():  
  
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,6)
    display.set_pen(255,0,0)

    display.text("current", 150, 20, 194, 2)
    display.text("volume", 150, 35, 194, 2)
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
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(58,30,13,160)
    display.circle(64,190,6)
    display.set_pen(0,0,150)
    display.rectangle(58,20,13,7+int((50-temp/2)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(150,50,90,40)
    display.set_pen(0,255,0)
    display.text(str(temp), 150, 50, 5, 5)
    display.update()
#----------------------------------------------------------------------
def get_temp():
    Analogvalue=stemp.read_u16()
    voltage=100*float(Analogvalue)/65535
    #print(voltage)
    return voltage

#----------------------------------------------------------------------

def main():
    
    global current_temp, temp,alarm,x
    color = [0,255,0]     
    timer1 = Timer()

    #基本图形绘制
    display_init()

    #timer1初始化
    timer1.init(freq=15,mode=Timer.PERIODIC, callback=lambda t:display_change(round(get_temp(),1), color))

    while True:
      sleep(0.1) 
main()
