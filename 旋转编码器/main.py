from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM
from utime import sleep
import time, math,array
#------------------------------------------------------------------
from rotary import Rotary
rotary = Rotary(20,21,22)

val = 0

def rotary_changed(change):
    global val
    if change == Rotary.ROT_CW:
        val = val + 1
        print(val)
    elif change == Rotary.ROT_CCW:
        val = val - 1
        print(val)

        
rotary.add_handler(rotary_changed)

#显示屏
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

#-------------------------------------------------------------------

#屏幕基本图形绘制

def display_init():  
  
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,6)
    display.set_pen(255,0,0)

    display.text("current", 150, 20, 194, 2)
    display.text("step", 150, 35, 194, 2)

    display.update()

    for i in range(6):
        display.set_pen(0,200,0)
        display.pixel_span(80,27 + i*30,10)
        display.text(str(50 - i *10), 100, 20+i*30, 194, 2)
        display.set_pen(0,0,220)
        if i < 5:
            for j in range(4):
                display.pixel_span(80,33 + j*6 + i * 30,5)
        display.update()
   
    display.update()

def main():
    color = [0,255,0]      #温度计颜色
    timer1 = Timer()
  
    #基本图形绘制
    display_init()
    
    #timer1初始化，以5Hz刷新温度计绘制yvis0z
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(round(val,1), color))
    
    while True:

        sleep(0.1 ) 
main()

