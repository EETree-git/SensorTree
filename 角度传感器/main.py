from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM
from utime import sleep
import time, math,array
#------------------------------------------------------------------
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

timer1 = Timer() 

stemp = ADC(2)                       
current_temp = 0                   
#-------------------------------------------------------------------
def display_init():
    
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,10)
    display.set_pen(255,0,0)
  
    display.text("current", 150, 20, 194, 2)
    display.text("angle", 150, 35, 194, 2)
    display.update()
  
    for i in range(6):
        display.set_pen(0,200,0)
        display.pixel_span(80,27 + i*30,10)
        display.text(str(300 - i *60), 100, 20+i*30, 194, 2)
        display.set_pen(0,0,220)
        if i < 5:
            for j in range(4):
                display.pixel_span(80,33 + j*6 + i * 30,5)
        display.update()
    
#---------------------------------------------------------------------
def display_change(temp, color):
    global current_temp
    current_temp = temp
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(58,30,13,160)
    display.circle(64,190,10)
    display.set_pen(0,0,150)
    display.rectangle(58,20,13,7+int((300-temp)/2))
    display.set_pen(0,0,0)
    display.rectangle(140,50,100,40)
    display.set_pen(0,255,0)
    display.text(str(int(temp)), 140, 50, 5, 5)
    display.update()
#----------------------------------------------------------------------
#温度获取
def get_temp():
    
    Analogvalue=stemp.read_u16()
    voltage=300*float(Analogvalue)/65535

    return voltage
#----------------------------------------------------------------------
def main():
    
    color = [0,255,0] 
    timer1 = Timer()
    display_init()
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(round(get_temp(),1), color))

    while True:
      sleep(0.1) 
main()

