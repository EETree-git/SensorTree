from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM,I2C, SPI
from utime import sleep
import time, math,array,struct
import pmw3901
#------------------------------------------------------------------

######################################################################
pmw_cs = Pin(25)
pmw_sck=Pin(26)
pmw_mosi=Pin(27)
pmw_miso=Pin(28,Pin.IN,Pin.PULL_DOWN)
spi0=SPI(1,baudrate=400_000, phase=1, polarity=1, sck=pmw_sck, mosi=pmw_mosi,miso=pmw_miso)

PMW = pmw3901.PMW3901(spi0,pmw_cs)
Value = [0,0]
######################################################################    
#初始化

#显示屏
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

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
def display_change(temp, color):
    global current_temp_Y,current_temp_X
    current_temp_Y = temp[0]
    current_temp_X = temp[1]
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(30,30,13,160)
#     display.circle(64,190,6)
    display.set_pen(0,0,150)
    display.rectangle(30,20,13,7+int((25-temp[0]/2)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(145,50,100,40)
    display.set_pen(0,255,0)
    display.text(str(temp[0]), 145, 50, 5, 5)
#     display.update()
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(36,184,160,13)
    display.circle(36,184,6)
    display.set_pen(0,0,150)
    display.rectangle(7+int((50-temp[1]/2)/2)*6,184,160,13)
    display.set_pen(0,0,0)
    display.rectangle(145, 130, 100, 40)
    display.set_pen(0,255,0)
    display.text(str(-temp[1]), 145, 130, 5, 5)
    display.update()
#----------------------------------------------------------------------
def get_temp():
    global Value
    if PMW._read(pmw3901.REG_DATA_READY ) & 0x80 :
        shutter_up = PMW._read(0x0C)
        squal = PMW._read(0x07);
        if shutter_up < 15 and squal >100 :
            deltaX = (PMW._read(0x04) << 8) |  PMW._read(0x03)
            deltaY = (PMW._read(0x06) << 8) |  PMW._read(0x05)
            if deltaX > 32767 :
                deltaX -= 65535
            if deltaY > 32767 :
                deltaY -= 65535 
            Value[0] = (Value[0]+deltaX)/10.0
            Value[1] = (Value[1]+deltaY)/10.0
            
    return Value
#-----------------------------------------------------------------------

def main():
    
    global current_temp_Y,current_temp_X
    
    timer1 = Timer()

    color = [0,255,0]  
    display_init()
    
    #timer初始化
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(get_temp(), color))

    while True:
        sleep(0.1) 
main()

