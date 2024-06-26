import utime
import math
from machine import Pin, I2C
# ========= Start LTR381 RGB IR sensor driver =============
ADDR  = (0X53)

LTR381_MAIN_CTRL = (0x00)  # Main control register
LTR381_MEAS_RATE = (0x04)  # Resolution and data rate
LTR381_GAIN = (0x05)  # ALS and UVS gain range
LTR381_PART_ID = (0x06)  # Part id/revision register
LTR381_MAIN_STATUS = (0x07)  # Main status register
LTR381_IRDATA = (0x0A)  # ALS data lowest byte, 3 byte
LTR381_GREENDATA = (0x0D)  # UVS data lowest byte, 3 byte
LTR381_REDDATA = (0x10)  # ALS data lowest byte, 3 byte
LTR381_BLUEDATA = (0x13)  # UVS data lowest byte, 3 byte
LTR381_INT_CFG = (0x19)  # Interrupt configuration
LTR381_INT_PST = (0x1A)  # Interrupt persistance config
LTR381_THRESH_UP = (0x21)  # Upper threshold, low byte, 3 byte
LTR381_THRESH_LOW = (0x24)  # Lower threshold, low byte, 3 byte

#RGB IR measurement resolution, Gain setting, measurement rate
RESOLUTION_20BIT_utime400MS = (0X00)
RESOLUTION_19BIT_utime200MS = (0X10)
RESOLUTION_18BIT_utime100MS = (0X20)#default
RESOLUTION_17BIT_utime50MS  = (0x3)
RESOLUTION_16BIT_utime25MS  = (0x40)
RESOLUTION_13BIT_utime12_5MS  = (0x50)
RATE_25MS = (0x0)
RATE_50MS = (0x1)
RATE_100MS = (0x2)# default
RATE_200MS = (0x3)
RATE_500MS = (0x4)
RATE_1000MS = (0x5)
RATE_2000MS = (0x6)

# measurement Gain Range.
GAIN_1  = (0x0)
GAIN_3  = (0x1)# default
GAIN_6 = (0x2)
GAIN_9 = (0x3)
GAIN_18 = (0x4)


class LTR381:
    def __init__(self, address=ADDR):
		self.i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)
		self.address = address

		self.ID = self.Read_Byte(LTR381_PART_ID)
		print("ID = %#x" %self.ID)
		if(self.ID != 0xC2):
			print("read ID error!,Check the hardware...")
			return

		self.Write_Byte(LTR381_MAIN_CTRL, 0x06) #  UVS in Active Mode
		#self.Write_Byte(LTR381_MEAS_RATE, RESOLUTION_20BIT_utime400MS | RATE_2000MS) #  Resolution=18bits, Meas Rate = 100ms
		self.Write_Byte(LTR381_MEAS_RATE, RESOLUTION_18BIT_utime100MS | RATE_100MS) #  Resolution=18bits, Meas Rate = 100ms		
		self.Write_Byte(LTR381_GAIN, GAIN_3) #  Gain Range=3.
		# self.Write_Byte(LTR381_INT_CFG, 0x34) # UVS_INT_EN=1, Command=0x34
		# self.Write_Byte(LTR381_GAIN, GAIN_3) #  Resolution=18bits, Meas Rate = 100ms
        
    def Read_Byte(self, cmd):
        rdate = self.i2c.readfrom_mem(int(self.address), int(cmd), 1)
        return rdate[0]

    def Write_Byte(self, cmd, val):
        self.i2c.writeto_mem(int(self.address), int(cmd), bytes([int(val)]))
        
    def REDS(self):
        # self.Write_Byte(LTR381_MAIN_CTRL, 0x0A) #  UVS in Active Mode
        Data1 = self.Read_Byte(LTR381_REDDATA)
        Data2 = self.Read_Byte(LTR381_REDDATA + 1)
        Data3 = self.Read_Byte(LTR381_REDDATA + 2)
        ret =  (Data3 << 16)| (Data2 << 8) | Data1
        # UVS = Data3*65536+Data2*256+Data1
        # print("UVS = ", UVS)
        return ret
    def GREENS(self):
        # self.Write_Byte(LTR381_MAIN_CTRL, 0x0A) #  UVS in Active Mode
        Data1 = self.Read_Byte(LTR381_GREENDATA)
        Data2 = self.Read_Byte(LTR381_GREENDATA + 1)
        Data3 = self.Read_Byte(LTR381_GREENDATA + 2)
        ret =  (Data3 << 16)| (Data2 << 8) | Data1
        # UVS = Data3*65536+Data2*256+Data1
        # print("UVS = ", UVS)
        return ret
    def BLUES(self):
        # self.Write_Byte(LTR381_MAIN_CTRL, 0x0A) #  UVS in Active Mode
        Data1 = self.Read_Byte(LTR381_BLUEDATA)
        Data2 = self.Read_Byte(LTR381_BLUEDATA + 1)
        Data3 = self.Read_Byte(LTR381_BLUEDATA + 2)
        ret =  (Data3 << 16)| (Data2 << 8) | Data1
        # UVS = Data3*65536+Data2*256+Data1
        # print("UVS = ", UVS)
        return ret   
    
