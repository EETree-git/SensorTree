from machine import UART,Pin,Timer,PWM,SPI,time_pulse_us, I2C,freq
import _thread
from time import sleep_us,ticks_us,sleep
import uos
import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
import random
import  math,array
import struct
import framebuf
freq(150_000_000)
st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=60_000_000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.WHITE)

f_list = [open("/bin/{}.bin".format(i), "rb") for i in range(18)]

uart1 = UART(1, baudrate=9600, tx=Pin(20), rx=Pin(21))

class GPS():
    buff = bytearray(270)
    def __init__(self):
        
        self.a = 0
        self.b = 0
        self.flag = 0
        self.array1 = '$GPGGA,'
        self.array2 = ''
    def read_and_process(self):
        
            buff = uart1.read(1)
            if buff == None:
#                 print(1)
                self.b = 0
            else:
                if buff == b'\n':
                    self.a = 1
#                     print(buff)
                if self.a == 1:
                    
                    buff = uart1.read(270)
#                     print(buff)
                    self.array2 = buff[0:6]
#                     print(self.array2)
                    if self.array2 == b'GPGGA,':
                        self.array2 = buff[7:44]
                        if self.array2[24]==b'A' or self.array2[25]==b'A' :
                            display.text(font2, 'N:'+str(self.array2[14:15], 'utf-8')+'*'+str(self.array2[16:17], 'utf-8')+'\''+str(self.array2[19:20], 'utf-8'),10, 30)
                            display.text(font2, 'E:'+str(self.array2[24:26], 'utf-8')+'*'+str(self.array2[27:28], 'utf-8')+'\''+str(self.array2[30:31], 'utf-8'), 10, 80)
                        else :
                            display.text(font2, 'N:serching...',10, 30)
                            display.text(font2, 'E:serching...', 10, 80)
                       
                        self.a = 0
                        
gps = GPS()

while True :
    for f in f_list: 
        f.seek(0)
        for row in range(100):
            buffer = f.read(200)
            display.blit_buffer(buffer, 120, row+120, 100, 1)
        gps.read_and_process()

