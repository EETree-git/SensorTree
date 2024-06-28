from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM,I2C
from utime import sleep
import time, math,array
from INA219 import INA219
#------------------------------------------------------------------
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

timer1 = Timer() 

ina219_reading_mA = 1000
ext_meter_reading_mA = 1000

'''
  @param i2caddr  I2C address
  @n INA219_I2C_ADDRESS1  0x40   A0 = 0  A1 = 0
  @n INA219_I2C_ADDRESS2  0x41   A0 = 1  A1 = 0
  @n INA219_I2C_ADDRESS3  0x44   A0 = 0  A1 = 1
  @n INA219_I2C_ADDRESS4  0x45   A0 = 1  A1 = 1
'''
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
ina = INA219(i2c, INA219.INA219_I2C_ADDRESS4)                                #Change I2C address by dialing DIP switch
#begin return True if succeed, otherwise return False
while not ina.begin():
    time.sleep(2)
'''
Revise the following two paramters according to actula reading of the INA219 and the multimeter
for linearly calibration
'''
ina.linear_cal(ina219_reading_mA, ext_meter_reading_mA)

ina.set_bus_RNG(ina.bus_vol_range_32V)
ina.set_PGA(ina.PGA_bits_8)
ina.set_bus_ADC(ina.adc_bits_12, ina.adc_sample_8)
ina.set_shunt_ADC(ina.adc_bits_12, ina.adc_sample_8)
ina.set_mode(ina.shunt_and_bus_vol_con)

#ina.reset()                                     #Resets all registers to default values                    
current_temp = 0                   
#-------------------------------------------------------------------
def display_init():
    
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,10)
    display.set_pen(255,0,0)
  
    display.text("current", 150, 20, 194, 2)
    display.text("value", 150, 35, 194, 2)
    display.text("mA", 200, 90, 194, 2)
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
    
#---------------------------------------------------------------------
def display_change(temp, color):
    global current_temp
    current_temp = temp
    #print(temp)
    display.set_pen(color[0], color[1], color[2])
    display.rectangle(58,30,13,160)
    display.circle(64,190,10)
    display.set_pen(0,0,150)
    display.rectangle(58,20,13,7+int((50-temp)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(150,50,90,40)
    display.set_pen(0,255,0)
    display.text(str(temp), 150, 50, 5, 5)
    display.update()
#----------------------------------------------------------------------
def get_temp():
    Currentvalue=ina.get_current_mA()
    return Currentvalue
#----------------------------------------------------------------------
def main():
    
    color = [0,255,0] 
    timer1 = Timer()
    display_init()
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(round(get_temp(),1), color))

    while True:
      sleep(0.1) 
main()



