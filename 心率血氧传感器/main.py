import uos
import st7789_c as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import framebuf
from machine import Pin, SPI, ADC,PWM,I2C,SoftI2C,Timer
import time, math,array
from utime import sleep_ms,ticks_diff, ticks_us
import struct
###############################################
from MAX30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from spo2cal import calc_hr_and_spo2
###############################################
st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=40000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=Pin(st7789_res, Pin.OUT),
                          dc=Pin(st7789_dc, Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.BLACK)
display.text(font2, "EETREE", 10, 10)
display.text(font2, "www.eetree.cn", 10, 40)

######################################################################
BEATS = 0  # 存储心率
FINGER_FLAG = False  # 默认表示未检测到手指

SPO2 = 0  # 存储血氧
TEMPERATURE = 0  # 存储温度

def display_info(t):
    # 如果没有检测到手指，那么就不显示
    if FINGER_FLAG is False:
        return
    display.text(font1, "Heart Rate=", 10, 100)
    display.text(font2, str(BEATS), 100, 90)
    display.text(font1, "SpO2=", 10, 140)
    display.text(font2, str(SPO2), 50, 130)
def main():
    global BEATS, FINGER_FLAG, SPO2, TEMPERATURE  # 如果需要对全局变量修改，则需要global声明

    # 创建I2C对象(检测MAX30102)
    i2c = SoftI2C(sda=Pin(20), scl=Pin(21), freq=400000)  # Fast: 400kHz, slow: 100kHz

    # 创建传感器对象
    sensor = MAX30102(i2c=i2c)

    # 检测是否有传感器
    if sensor.i2c_address not in i2c.scan():
        print("没有找到传感器")
        return
    elif not (sensor.check_part_id()):
        # 检查传感器是否兼容
        print("检测到的I2C设备不是MAX30102或者MAX30105")
        return
    else:
        print("传感器已识别到")

    # 配置
    sensor.setup_sensor()
    sensor.set_sample_rate(400)
    sensor.set_fifo_average(8)
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    t_start = ticks_us()  # Starting time of the acquisition

    MAX_HISTORY = 32
    
    beats_history = []
    beat = False

    red_list = []
    ir_list = []
    history = []
    while True:
        sensor.check()
        if sensor.available():
            # FIFO 先进先出，从队列中取数据。都是整形int
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage() 
            if red_reading < 1000:
                print('No finger')
                FINGER_FLAG = False  # 表示没有放手指
                continue
            else:
                FINGER_FLAG = True  # 表示手指已放

            # 计算心率
            history.append(red_reading)

            # 为了防止列表过大，这里取列表的后32个元素
            history = history[-MAX_HISTORY:]

            # 提取必要数据
            minima, maxima = min(history), max(history)
            threshold_on = (minima + maxima * 3) // 4   # 3/4
            threshold_off = (minima + maxima) // 2      # 1/2

            if not beat and red_reading > threshold_on:
                beat = True                    
                t_us = ticks_diff(ticks_us(), t_start)
                t_s = t_us/1000000
                f = 1/t_s
                bpm = f * 60
                if bpm < 500:
                    t_start = ticks_us()
                    beats_history.append(bpm)                    
                    beats_history = beats_history[-MAX_HISTORY:]   # 只保留最大30个元素数据
                    BEATS = round(sum(beats_history)/len(beats_history), 2)  # 四舍五入
            if beat and red_reading < threshold_off:
                beat = False

            # 计算血氧
            red_list.append(red_reading)
            ir_list.append(ir_reading)
            # 最多 只保留最新的100个
            red_list = red_list[-100:]
            ir_list = ir_list[-100:]
            # 计算血氧值
            if len(red_list) == 100 and len(ir_list) == 100:
                hr, hrb, sp, spb = calc_hr_and_spo2(red_list, ir_list)
                if hrb is True and spb is True:
                    if sp != -999:
                        SPO2 = int(sp)

            # 计算温度
            TEMPERATURE = sensor.read_temperature()

if __name__ == '__main__':

    tim = Timer(period=2000, mode=Timer.PERIODIC, callback=display_info)

    main()




