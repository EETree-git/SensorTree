import uos
import machine
import st7789 as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import framebuf
machine.freq(200_000_000 )
#from DMA import DMA
import time
from math import pi,sin,exp,sqrt,floor,cos
import time, array, uctypes, rp_devices as devs
import math
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
############################################################
###
st7789_res = 0
st7789_dc  = 1

spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
reset=machine.Pin(st7789_res, machine.Pin.OUT)
dc=machine.Pin(st7789_dc, machine.Pin.OUT)

###

spi0=machine.SPI(0,baudrate=62500000, phase=1, polarity=1,bits = 8 , sck=spi_sck, mosi=spi_tx)
display = st7789.ST7789(spi0, disp_width, disp_width,reset,dc,xstart=0, ystart=0, rotation=3)
display.clear(st7789.BLACK)
#############################################################
dis_h = 150
dis_w = 150

dis_buff_0 = array.array('H', (0 for _ in range(dis_h*dis_w*2)))

###

DMA_CHAN_0 = 0
dma_chan_0 = devs.DMA_CHANS[DMA_CHAN_0]
#dma_0 = devs.DMA_DEVICE

dma_chan_0.READ_ADDR_REG = uctypes.addressof(dis_buff_0)
dma_chan_0.WRITE_ADDR_REG = devs.SPI0_SSPDR
dma_chan_0.TRANS_COUNT_REG = len(dis_buff_0)#int(len(dis_buff_0)/2)
dma_chan_0.CTRL_TRIG_REG = 0
dma_chan_0.CTRL_TRIG.BUSY = 0
#print(dma_chan_0.CTRL_TRIG.BUSY)
dma_chan_0.CTRL_TRIG.CHAIN_TO = DMA_CHAN_0
dma_chan_0.CTRL_TRIG.INCR_WRITE = 0
dma_chan_0.CTRL_TRIG.INCR_READ = 1
dma_chan_0.CTRL_TRIG.TREQ_SEL = devs.DREQ_SPI0_TX
# dma_chan_0.CTRL_TRIG.DATA_SIZE = 1


#############################################################
I2C_TEST = machine.I2C(0,scl=machine.Pin(21), sda=machine.Pin(20))     #initializing the I2C method for ESP32

#BM1422GMV

I2C_TEST.writeto_mem(14,0x1B,bytes([152]))
I2C_TEST.writeto_mem(14,0x5C,bytes([0]))
I2C_TEST.writeto_mem(14,0x5D,bytes([0]))
I2C_TEST.writeto_mem(14,0x1C,bytes([12]))
I2C_TEST.writeto_mem(14,0x6C,bytes([45]))
I2C_TEST.writeto_mem(14,0x72,bytes([45]))
I2C_TEST.writeto_mem(14,0x78,bytes([45]))
I2C_TEST.writeto_mem(14,0x1D,bytes([64]))

unsigned_x=0
unsigned_y=0
unsigned_z=0
signed_x=0
signed_y=0
signed_z=0
def read_component():
    global signed_x,signed_y,signed_z,unsigned_x,unsigned_y,unsigned_z
    unsigned_x = I2C_TEST.readfrom_mem(14, 0x10,2)
    unsigned_y = I2C_TEST.readfrom_mem(14, 0x12,2)
    unsigned_z = I2C_TEST.readfrom_mem(14, 0x14,2)
    signed_x=((unsigned_x[1]<<8)|unsigned_x[0])  - 256-380
    signed_y=((unsigned_y[1]<<8)|unsigned_y[0])  - 256-170
    signed_z=((unsigned_z[1]<<8)|unsigned_z[0]) - 230-200
#############################################################
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
display.set_window(125,45,150,150)
ROT_X_Y=0
ROT_X_Z=0
ROT_Y_Z=0
BM_X_Y_pre=0
BM_X_Z_pre=0
BM_Y_Z_pre=0
while True:
    read_component()
    BM_X_Y=math.atan2(float(signed_y),float(signed_x))*57.3+180
    BM_X_Z=math.atan2(float(signed_z),float(signed_x))*57.3+180
    BM_Y_Z=math.atan2(float(signed_z),float(signed_y))*57.3+180
    if BM_X_Y_pre >300 and BM_X_Y <60 :
        ROT_X_Y= -360
    elif BM_X_Y_pre <60 and BM_X_Y >300 :
        ROT_X_Y= 360
    else :
        ROT_X_Y=0
    if BM_X_Z_pre >300 and BM_X_Z <60 :
        ROT_X_Z= -360
    elif BM_X_Z_pre <60 and BM_X_Z >300 :
        ROT_X_Z= 360
    else :
        ROT_X_Z=0
    if BM_Y_Z_pre >300 and BM_Y_Z <60 :
        ROT_Y_Z= -360
    elif BM_Y_Z_pre <60 and BM_Y_Z >300 :
        ROT_Y_Z= 360
    else :
        ROT_Y_Z=0
    drawcube((BM_X_Y_pre-BM_X_Y+ROT_X_Y)/36,(BM_X_Z_pre-BM_X_Z+ROT_X_Z)/36,(BM_Y_Z_pre-BM_Y_Z+ROT_Y_Z)/36)
    print((BM_X_Y_pre-BM_X_Y+ROT_X_Y)/36,(BM_X_Z_pre-BM_X_Z+ROT_X_Z)/36,(BM_Y_Z_pre-BM_Y_Z+ROT_Y_Z)/36)
    BM_X_Y_pre=BM_X_Y
    BM_X_Z_pre=BM_X_Z
    BM_Y_Z_pre=BM_Y_Z
    dc.off()
    display.write(st7789.ST7789_RAMWR, b"" )
    dma_chan_0.READ_ADDR_REG = uctypes.addressof(dis_buff_0)
    dc.on()
    dma_chan_0.CTRL_TRIG.EN = 1
    while dma_chan_0.CTRL_TRIG.BUSY:
        pass
    dma_chan_0.CTRL_TRIG.EN = 0

    
 
