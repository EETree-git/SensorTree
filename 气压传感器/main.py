from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import I2C, ADC, Pin, Timer, PWM
import time, math,array
from utime import sleep
reset_pin = Pin(8,Pin.IN,Pin.PULL_UP)
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400_000)
ms5611_c = [0, 0, 0, 0, 0, 0, 0, 0]
GY63_ADDRESS = 0x77
print(i2c.scan())
def reset():
    i2c.writeto(GY63_ADDRESS, bytearray([0x1E]))
    time.sleep(0.01)
def init():
    reset()
    for i in range(8):
        ms5611_c[i] = prom(i)
def prom(coef_num):
    rxbuff = i2c.readfrom_mem(GY63_ADDRESS, 0XA0+coef_num*2, 3)
    return rxbuff[0] << 8 | rxbuff[1]    
def read_pressure():   
    i2c.writeto(GY63_ADDRESS, bytearray([0x48]))   
    time.sleep(0.02)    
    data = i2c.readfrom_mem(GY63_ADDRESS, 0, 3)    
    pressure = (data[0] << 16) + (data[1] << 8) + data[2]    
    return pressure
def read_temperature():
    i2c.writeto(GY63_ADDRESS, bytearray([0x58]))   
    time.sleep(0.02)    
    data = i2c.readfrom_mem(GY63_ADDRESS, 0, 3)    
    temperature = (data[0] << 16) + (data[1] << 8) + data[2]   
    return temperature
def calculate(ut, up):
    dT = ut - (ms5611_c[5] << 8)
    off = (ms5611_c[2] << 16) + ((ms5611_c[4]*dT) >> 7)
    sens = (ms5611_c[1] << 15) + ((ms5611_c[3]*dT) >> 8)
    temp = 2000 + ((dT*ms5611_c[6]) >> 23)   
    if (temp < 2000):
        delt = temp - 2000
        delt = 5 * delt *delt
        off = off - (delt >> 1)
        sens = sens - (delt >> 2)   
    if (temp < -1500):
        delt = temp + 1500
        delt = delt * delt
        off = off - (7 * delt)
        sens = sens - ((11 * delt) >> 1)   
    temp = temp - ((dT*dT) >> 31)
    press = (((int(up)*sens) >> 21) - off) >> 15
    return press, temp
flag = 0
total = 0
length = 10
buffer = array.array('H', (0 for _ in range(length)))
index = 0
position = 0
init_position = 0
current_press = 0
init()
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
    display.text("value", 150, 35, 194, 2)
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
    global init_position,current_press,index,length,position
    if reset_pin.value() == 0 :
        init_position = current_press
    up = read_pressure()
    ut = read_temperature()
    pressure, temperature = calculate(ut, up)
    buffer[index] = pressure
    index += 1
    index %= length
    for i in range (length) :
        current_press += buffer[i]
    current_press = current_press/length
#     print("Pressure:", current_press)
#     hight=(101325-current_press)/133*12
#     print("hight:", hight)
    position=int((current_press-init_position)*5)+25
    print(position)
    return position
#----------------------------------------------------------------------
def main():
    
    color = [0,255,0] 
    timer1 = Timer()
    display_init()
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(get_temp(), color))

    while True:
      sleep(0.1) 
main()

