import sys,os
import time
import math
#sys.path.append(r'C:\Users\User\Documents\#Analog\PythonOryx\PFE_1_Shut\Equipment\aardvark')
from aardvark_py import *
#import aardvark_py 
import timeit
import matplotlib.pyplot as plt

_debug = False

class DAC():

    def __init__(self,dev_handler):
        self.ver = 'beta'
        print("Initialized DAC Module - ver:", self.ver)
        self.addr = 0x60
        self.DAC_Data = [0, 0, 0, 0]
        self.dev_handler = dev_handler

    def DAC_Update(self, channel, data, vref = 1, gain = 0):
        #TODO: Add variable type/range checking
        settings = vref << 7 | gain << 4
        self.DAC_Data[channel] = data
        #Multi-Write Command
        i2c_data = array('B',[(0x40 | (channel & 3) << 1), settings | (data >> 8), (data & 0xFF)])
        aa_i2c_write(self.dev_handler, self.addr, AA_I2C_NO_FLAGS, i2c_data)

    def volt_to_dac (self, voltage, vref_voltage):
        return (4096.0*voltage/(vref_voltage))

class PORT_EXTENDER():

    def __init__(self):
        self.ver = 'beta'
        print("Initialized Port Extender Module - ver:", self.ver)
        self.addr=0x20
        #self.port=[0xF0,0]

    def init_device(self, dev_handler, ports):
        self.dev_handler = dev_handler
        i2c_data = array('B',[0x06, ports['p0']['dir'], ports['p1']['dir']])
        if (aa_i2c_write(dev_handler, self.addr, AA_I2C_NO_FLAGS, i2c_data) == 3):
            print("Port Configuration Written")
        else:
            print("Port Configuration Failed")
        # i2c_data = array('B', [0x02, ports['p0']['data'], ports['p1']['data']])
        # if (aa_i2c_write(dev_handler, self.addr, AA_I2C_NO_FLAGS, i2c_data) == 3):
        #     print "Port Data Written"
        # else:
        #     print "Port Data Failed"
        self.port = [ports['p0']['data'], ports['p1']['data']]
        self.set_port(self.port)

    def set_port(self, data):
        port = [data[0],data[1]]
        i2c_data = array('B',[0x02, port[0], port[1]])
        if (aa_i2c_write(self.dev_handler, self.addr, AA_I2C_NO_FLAGS, i2c_data) == 3):
            if _debug:
                print ("Port Written")
        else:
            print("Port Write Failed")

    def read_port(self,port):
        aa_i2c_write(self.dev_handler, self.addr, AA_I2C_NO_FLAGS, array('B',[0x00+port]))
        i2c_data = array_u08(1)
        aa_i2c_read(self.dev_handler, self.addr, AA_I2C_NO_FLAGS, i2c_data)
        c = (bin(i2c_data[0]).split('0b')[1]).rjust(8,'0')
        cmp_out_f = [int(x) for x in c[4:8]]
        sr_data_out_f = [int(x) for x in c[0:4]]
        return cmp_out_f, sr_data_out_f

    def set_bit(self, port_num, bit):
        self.port[port_num] |= (1 << bit)
        self.set_port(self.port)

    def clr_bit(self, port_num, bit):
        self.port[port_num] &= ~(1 << bit)
        self.set_port(self.port)


class PFE():

    def __init__(self):

        #PORT_EXTENDER.__init__(self)

        self.port_extender=PORT_EXTENDER()

        self.ver = 'beta'
        print("Initialized PFE Module - ver:", self.ver)

        self.init_device()

    def latch(self, flavor):
        #This function toggles the latch
        #F0 is mapped to P0.0, F1: P0.1 ... F3: P0.3
        self.port_extender.set_bit(0,flavor)
        self.port_extender.clr_bit(0,flavor)

    def write_sr(self, flavor, out_buffer):
        #out_buffer = array('B', [0x55]*128/8)
        in_buffer = array('B', [0x00]*16)
        if aa_spi_write(self.dev_handler, out_buffer, in_buffer)[0] != 16:
            print("Error In SPI Write")
        self.latch(flavor)

    #only works with flavor 3
    def write_validate_sr(self, flavor, out_buffer):
        #self.port_extender.clr_bit(0,flavor)
        in_buffer = array('B', [0x00] * 16)
        if aa_spi_write(self.dev_handler, out_buffer, in_buffer)[0x00] != 16:
            print("Error In SPI Write")
        #self.port_extender.set_bit(0, flavor)
        self.latch(flavor)
        #self.port_extender.clr_bit(0, flavor)
        if aa_spi_write(self.dev_handler, out_buffer, in_buffer)[0x00] != 16:
            print("Error In SPI Write")
        #self.port_extender.set_bit(0, flavor)
        return in_buffer == out_buffer

    # def read_data(self, dev_handler, data_length_b, address, flags):
    #      data = array_u08(data_length_b)
    #      c,data = aa_i2c_read(dev_handler, address, flags, data)
    #      return data[0:]
    #
    # def write_data(self, dev_handler, data_lenth_b, data_to_send):
    #      data_out = array_u08(data_lenth_b)
    #      data_in = array_u08(data_lenth_b)
    #      for t in range(data_lenth_b):
    #         data_out[t] = data_to_send[t]
    #      c = aa_spi_write(dev_handler, data_out, data_in)
    #      return c
    #
    #
    # def load_fullfeed(self, dev_handler, stps):
    #     """
    #
    #     :param dev_handler:
    #     :param stps:
    #     :return:
    #     """
    #
    # def updateRegister(self, dev_handler):
    #     self.write_data(dev_handler,)

    def init_device(self):

        (num, ports, unique_ids) = aa_find_devices_ext(16, 16)
        # num=0 #added by irad for debug 22/5/19
        if num > 0:
            print("%d device(s) found:" % num)
            # Print the information on each device
            for i in range(num):
             port = ports[i]
             unique_id = unique_ids[i]

             # Determine if the device is in-use
             inuse = "(avail)"
             if (port & AA_PORT_NOT_FREE):
                 inuse = "(in-use)"
                 port = port & ~AA_PORT_NOT_FREE

             # Display device port number, in-use status, and serial number
             print("    port = %d   %s  (%04d-%06d)" % (port, inuse, unique_id / 1000000, unique_id % 1000000))
        else:
            print("No devices found.")

          # Open the device
        try:
            self.dev_handler = aa_open(port)
        except:
            raise("Advark is not connected")

        if (self.dev_handler <= 0):
            print("Unable to open Aardvark device on port %d" % port)
            print("Error code = %d" % self.dev_handler)

        # Ensure that the I2C and SPI subsystems are enabled
        aa_configure(self.dev_handler, AA_CONFIG_SPI_I2C)

        # Determine available I2C bitrates
        bitrates = {}
        for rate in range(1000):
            bitrate = aa_i2c_bitrate(self.dev_handler, rate)
            bitrates[bitrate] = 1

         # Print the available I2C bitrates
         #print "I2C Bitrates (kHz):"
         #self.printBitrates(bitrates.keys())

         # Determine available SPI bitrates
        bitrates = {}
        for rate in range(0, 8000, 25):
            bitrate = aa_spi_bitrate(self.dev_handler, rate)
            bitrates[bitrate] = 1

         # Print the available SPI bitrates
         #print "SPI Bitrates (kHz):"
         #self.printBitrates(bitrates.keys())

        c = aa_spi_bitrate(self.dev_handler, 1)
        print ("Setting The SPI Bitrate to: " + str(c) + " kHz")
        c = aa_spi_configure(self.dev_handler, AA_SPI_POL_RISING_FALLING, AA_SPI_PHASE_SAMPLE_SETUP, AA_SPI_BITORDER_MSB)  # needs to check MSB or LSB first
        print("Configured Polarity, Phase and Bitorder:", c)
        aa_i2c_pullup(self.dev_handler, AA_I2C_PULLUP_BOTH)
        print( "I2C Pull Ups Enabled")
        c = aa_i2c_bitrate(self.dev_handler, 800)
        print ("Setting The I2C Bitrate to: " + str(c) + " kHz")

        ports = {'p0': {'dir': 0x00, 'data': 0xF0}, 'p1': {'dir': 0xFF, 'data': 0}}
        self.port_extender.init_device(self.dev_handler, ports)


    def printBitrates(rates):
        sorted_rates = rates[:]
        sorted_rates.sort()

        print("  ")
        count = 0
        for rate in sorted_rates:
            if count >= 9:
                print("\n ")
                count = 0
            print("%4d " % rate)
            count += 1
        print("\n")

    # def free_bus(self, dev_handler):
    #     #     c = aa_i2c_free_bus(dev_handler)
    #     #     print "Freeing the bus"#,c
    # def scan_bus_for_devs(self, dev_handler, out = 0): # this will return 1 if device presents on specific address and 0 otherwise
    #     p=[]
    #     for t in range(128):
    #         t=int(t)
    #         c=self.write_data(dev_handler,1,t,AA_I2C_NO_FLAGS,[0x0])
    #         if out:
    #             print"address:",t,
    #             print "returns:",c
    #         p.append(c)
    #     return p
    #
    def close_adap(self):
        c = aa_close(self.dev_handler)


def main():
    pfe=PFE()

    #pfe.init_device()

    #pfe.latch(3);

    dac = DAC(pfe.dev_handler)
    #dac.init_device(pfe.dev_handler)
    dac.DAC_Update(0, 0)
    #dac.DAC_Update(0, int(dac.volt_to_dac(0.1 * 26.538, 3.3, 1)))

    pfe.write_sr(2, array('B', [0x55]*16))
    #pfe.write_validate_sr(3, array('B', [0x55]*128))

    #cmp_out_f, sr_data_out_f = pfe.port_extender.read_port(0)
    #print("CMP_OUT_F3 = " + str(cmp_out_f[3]))

    pfe.close_adap()


if __name__ == '__main__':
    main()