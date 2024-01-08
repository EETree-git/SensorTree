from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM,I2C
from utime import sleep
import time, math,array
#------------------------------------------------------------------

######################################################################

######################################################################    
#初始化

#显示屏
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

xtemp = ADC(2)    
ytemp = ADC(1)                      

current_temp_Y = 0              
current_temp_X = 0
#-------------------------------------------------------------------

#屏幕基本图形绘制

def display_init():  
  
   #绘制Y轴计
    display.set_pen(0,255,0)
    display.rectangle(30,30,13,160)
    display.circle(36,190,6)
    display.set_pen(255,0,0)
   #绘制X轴计
    display.set_pen(0,255,0)
    display.rectangle(36,184,160,13)
    display.circle(64,190,6)
    display.set_pen(255,0,0)
   #绘制文字 
    display.text("current", 150, 20, 194, 2)
    display.text("Y_axis", 150, 35, 194, 2)
    display.text("current", 150, 100, 194, 2)
    display.text("X_axis", 150, 115, 194, 2)
    display.update()
  
    display.update()
#---------------------------------------------------------------------
def display_change_Y(temp, color):
    global current_temp_Y
    current_temp_Y = temp
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(30,30,13,160)
#     display.circle(64,190,6)
    display.set_pen(0,0,150)
    display.rectangle(30,20,13,7+int((50-temp/2)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(145,50,100,40)
    display.set_pen(0,255,0)
    display.text(str(temp), 145, 50, 5, 5)
    display.update()
def display_change_X(temp, color):
    global current_temp_X
    current_temp_X = temp
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(36,184,160,13)
    display.circle(36,184,6)
    display.set_pen(0,0,150)
    display.rectangle(7+int((65-temp/2)/2)*6,184,160,13)
    display.set_pen(0,0,0)
    display.rectangle(145, 130, 100, 40)
    display.set_pen(0,255,0)
    display.text(str(100-temp), 145, 130, 5, 5)
    display.update()
#----------------------------------------------------------------------
def get_temp_x():
    Analogvalue=xtemp.read_u16()
    voltage=100*float(Analogvalue)/65535
    return voltage
def get_temp_y():
    Analogvalue=ytemp.read_u16()
    voltage=100*float(Analogvalue)/65535
    return voltage

#-----------------------------------------------------------------------

def main():
    
    global current_temp_Y,current_temp_X
    
    timer1 = Timer()
    timer2 = Timer()
    color = [0,255,0]  
    display_init()
    
    #timer初始化
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change_X(round(get_temp_x(),1), color))
    timer2.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change_Y(round(get_temp_y(),1), color))

    while True:
        sleep(0.1) 
main()
