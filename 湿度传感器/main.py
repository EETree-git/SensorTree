from breakout_colourlcd240x240 import BreakoutColourLCD240x240
from machine import ADC, Pin, Timer, PWM,I2C
from utime import sleep
import time, math,array
#------------------------------------------------------------------

######################################################################

# 定义连接到 DHT22 数据线的引脚
data_pin=Pin(20, Pin.IN,Pin.PULL_UP)

def readdata():
    # 向 DHT22 传感器发送启动信号
    data_pin.init(Pin.OUT)
    data_pin.low()
    time.sleep_ms(20)#微处理器的I/O设置为输出同时输出低电平，且低电平保持时间不能小于18ms（最大不得超过30ms）
    data_pin.high()
    data_pin.init(Pin.IN, Pin.PULL_UP)
    # 等待 DHT22 传感器响应
    while data_pin.value() == 1:
        pass
    while data_pin.value() == 0:
        pass
    while data_pin.value() == 1:
        pass
    data_pro = []
    j=0
    k=0
    while j < 40:
        k = 0
        while data_pin.value() == 0:
            pass
        while data_pin.value() == 1:
            k += 1
            if k > 100:
                break
        if k < 3:
            data_pro.append(0)
        else:
            data_pro.append(1)
        j += 1
    return data_pro

def read():
    # 读取传感器数据并验证校验和
    data=[]
    data = readdata()
    humidity_bit=data[0:8]
    humidity_point_bit=data[8:16]
    temperature_bit=data[16:24]
    temperature_point_bit=data[24:32]
    check_bit=data[32:40]
    humidity=0
    humidity_point=0
    temperature=0
    temperature_point=0
    check=0
    #温度、湿度、校验位计算
    for i in range(8):
        #湿度计算
        humidity+=humidity_bit[i]*2**(7-i)
        humidity_point+=humidity_point_bit[i]*2**(7-i)
        #温度计算
        temperature+=temperature_bit[i]*2**(7-i)
        temperature_point+=temperature_point_bit[i]*2**(7-i)
        #校验位计算
        check+=check_bit[i]*2**(7-i)
    tmp=humidity+humidity_point+temperature+temperature_point
    return temperature, humidity

######################################################################    
#初始化
width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT
display_buffer = bytearray(width * height*2)
display = BreakoutColourLCD240x240(display_buffer)

timer1 = Timer()                    #定时器1

stemp = ADC(2)                  
current_temp = 0         
#-------------------------------------------------------------------
def display_init():  
  
    display.set_pen(0,255,0)
    display.rectangle(58,30,13,160)
    display.circle(64,190,10)
    display.set_pen(255,0,0)
    display.text("current", 150, 20, 194, 2)
    display.text("humidity", 150, 35, 194, 2)

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
    display.circle(64,190,10)
    display.set_pen(0,0,150)
    display.rectangle(58,20,13,7+int((50-temp/2)/2)*6)
    display.set_pen(0,0,0)
    display.rectangle(150,50,90,40)
    display.set_pen(0,255,0)
    display.text(str(temp)+"%", 150, 50, 5, 5)
    display.update()
#----------------------------------------------------------------------

def get_temp():
    # 尝试从DHT22传感器读取温度和湿度数据
    temperature, humidity = read()
    time.sleep(0.5)  # 等待 2 秒，然后进行下一次读数
    return humidity

#-----------------------------------------------------------------------

def main():
    
    color = [0,255,0]      
    timer1 = Timer()
  
    display_init()
    
    #timer1初始化
    timer1.init(freq=5,mode=Timer.PERIODIC, callback=lambda t:display_change(round(get_temp(),1), color))

    while True:
      sleep(0.1) 
main()
