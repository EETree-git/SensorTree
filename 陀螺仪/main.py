import uos
import machine
import st7789 as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import framebuf
machine.freq(200_000_000 )

import time
from math import pi,sin,exp,sqrt,floor,cos
import time, array, uctypes, rp_devices as devs
import mpu6050
#########################################################
###
w, h = 240, 220
j=0
i=0
x,y=0,0
offset_adc=0
offset_dis=0
x_Value=0
y_Value=0
disp_width = 240
disp_height = 240

def sine(x,offset):
    return (sin(x/120*pi+offset)+1)*120
############################################################
###
xAxis = machine.ADC(machine.Pin(28))
yAxis = machine.ADC(machine.Pin(29))
st7789_res = 0
st7789_dc  = 1
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
reset=machine.Pin(st7789_res, machine.Pin.OUT)
dc=machine.Pin(st7789_dc, machine.Pin.OUT)


###


spi0=machine.SPI(0,baudrate=62500000, phase=1, polarity=1,bits = 8 , sck=spi_sck, mosi=spi_tx)
display = st7789.ST7789(spi0, disp_width, disp_width,reset,dc,xstart=0, ystart=0, rotation=3)

#############################################################
dis_h = 150
dis_w = 150

dis_buff_0 = array.array('H', (0 for _ in range(dis_h*dis_w*2)))

dis_a=bytearray(150)
dis_b=bytearray(150)
###

DMA_CHAN_0 = 0
dma_chan_0 = devs.DMA_CHANS[DMA_CHAN_0]
#dma_0 = devs.DMA_DEVICE

dma_chan_0.READ_ADDR_REG = uctypes.addressof(dis_buff_0)
dma_chan_0.WRITE_ADDR_REG = devs.SPI0_SSPDR
dma_chan_0.TRANS_COUNT_REG = int(len(dis_buff_0)/2)
dma_chan_0.CTRL_TRIG_REG = 0
dma_chan_0.CTRL_TRIG.BUSY = 0
#print(dma_chan_0.CTRL_TRIG.BUSY)
dma_chan_0.CTRL_TRIG.CHAIN_TO = DMA_CHAN_0
dma_chan_0.CTRL_TRIG.INCR_WRITE = 0
dma_chan_0.CTRL_TRIG.INCR_READ = 1
dma_chan_0.CTRL_TRIG.TREQ_SEL = devs.DREQ_SPI0_TX
dma_chan_0.CTRL_TRIG.DATA_SIZE = 1


#############################################################
i2c = machine.I2C(0,scl=machine.Pin(21), sda=machine.Pin(20))     #initializing the I2C method for ESP32
mpu= mpu6050.accel(i2c)
def line( x0, y0, x1, y1, color):
    """
    Draw a single pixel wide line starting at x0, y0 and ending at x1, y1.

    Args:
        x0 (int): Start point x coordinate
        y0 (int): Start point y coordinate
        x1 (int): End point x coordinate
        y1 (int): End point y coordinate
        color (int): 565 encoded color
    """
    global dis_buff_0,dis_h,dis_w
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = abs(y1 - y0)
    err = dx // 2
    if y0 < y1:
        ystep = 1
    else:
        ystep = -1
    while x0 <= x1:
        if steep:
#             self.pixel(y0, x0, color)
            dis_buff_0[(y0-1)*dis_h+x0] = color
        else:
#             self.pixel(x0, y0, color)
            dis_buff_0[(x0-1)*dis_h+y0] = color
        err -= dy
        if err < 0:
            y0 += ystep
            err += dx
        x0 += 1
        
cube=[[-40,-40,-40],[-40,40,-40],[40,40,-40],[40,-40,-40],[-40,-40,40],[-40,40,40],[40,40,40],[40,-40,40]]
lineid=[1,2,2,3,3,4,4,1,5,6,6,7,7,8,8,5,8,4,7,3,6,2,5,1]
def matconv(a,matrix):
    res=[0,0,0]
    for i in range(0,3):
        res[i]=matrix[i][0]*a[0]+matrix[i][1]*a[1]+matrix[i][2]*a[2]
    for i in range(0,3):
        a[i]=res[i]
    return a

def rotate(obj,x,y,z):
    x=x/pi
    y=y/pi
    z=z/pi
    rz=[[cos(z),-sin(z),0],[sin(z),cos(z),0],[0,0,1]]
    ry=[[1,0,0],[0,cos(y),-sin(y)],[0,sin(y),cos(y)]]
    rx=[[cos(x),0,sin(x)],[0,1,0],[-sin(x),0,cos(x)]]
    matconv(matconv(matconv(obj,rz),ry),rx)
buff_1=bytearray(24)
buff_2=bytearray(24)
buff_pre_1=bytearray(24)
buff_pre_2=bytearray(24) 
def drawcube(x,y,z):
    global buff_1,buff_2,buff_pre_1,buff_pre_2,mpu_value
#     display.fill_rect(0,0,100,100,0)
#     display.fill(0)
    for i in range (0,24,2):
        line(buff_pre_1[i],buff_pre_1[i+1],buff_pre_2[i],buff_pre_2[i+1],st7789.BLACK)
    for i in range(0,8):
        rotate(cube[i],x,y,z)
    for i in range(0,24,2):
        buff_1[i]=int(75+cube[lineid[i]-1][0])
        buff_1[i+1]=int(75+cube[lineid[i]-1][1])
        buff_2[i]=int(75+cube[lineid[i+1]-1][0])
        buff_2[i+1]=int(75+cube[lineid[i+1]-1][1])
    for i in range (0,24,2):
        line(buff_1[i],buff_1[i+1],buff_2[i],buff_2[i+1],st7789.BLUE)
    buff_pre_1 = buff_1
    buff_pre_2  = buff_2
#############################################################
display.clear( 0x0000)
mpu_value = {}
display.set_window(125,45,150,150)
spi0.init(bits=16)
while True:

    mpu_value=mpu.get_values()
    drawcube(mpu_value["GyX"]/32767.5,mpu_value["GyY"]/32767.5,mpu_value["GyZ"]/32767.5)
    
    
    dc.off()
    display.write(st7789.ST7789_RAMWR, b"" )
    dma_chan_0.READ_ADDR_REG = uctypes.addressof(dis_buff_0)
    dc.on()
    dma_chan_0.CTRL_TRIG.EN = 1
    while dma_chan_0.CTRL_TRIG.BUSY:
        pass
    dma_chan_0.CTRL_TRIG.EN = 0

    




