from machine import I2C
from machine import Pin
import array
from time import sleep
import mpu6050
i2c = I2C(0,scl=Pin(21), sda=Pin(20))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)
dis_buff_0 = array.array('H', (0 for _ in range(90000)))
while True:
    value=mpu.get_values()
    print(value["GyX"]/32767.5,value["GyY"]/32767.5,value["GyZ"]/32767.5)
    sleep(0.1)
