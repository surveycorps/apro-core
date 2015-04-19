from nrf24 import NRF24
import math
import struct

class APRO:
   def __init__(self, num):
      self.num = num

   def set_pwm(self, pwm1, pwm2, pwm3):
      self.pwm1 = pwm1
      self.pwm2 = pwm2
      self.pwm3 = pwm3

   def set_dir(self, dir1, dir2, dir3):
      self.dir1 = dir1
      self.dir2 = dir2
      self.dir3 = dir3

   # Functions for tricks like rotate 90, flip over, nod, etc

   def transmit(self, radio):
      buf = [self.dir1, self.pwm1, self.dir2, self.pwm2, self.dir3, self.pwm3]
      radio.write(buf)
      
   def init_radio(self, radio):
      pipes = [ [0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2] ]
      radio.begin(0,0,"P9_15", "P9_16") #Set CE and IRQ pins
      radio.setRetries(2,15)

      # Number of bytes we're sending per payload
      radio.setPayloadSize(6)
      radio.setCRCLength(NRF24.CRC_8)
      radio.setChannel(0x60)
      radio.setDataRate(NRF24.BR_2MBPS)
      radio.setPALevel(NRF24.PA_MAX)
      radio.openWritingPipe(pipes[1])
      radio.openReadingPipe(1,pipes[0])
      radio.startListening()
      radio.stopListening()
      radio.printDetails()
      radio.powerUp()

   def init_imu(self, imu):
      imu.IMUInit()
      print("IMU Name: " + imu.IMUName())

      # this is a good time to set any fusion parameters
      imu.setSlerpPower(0.02)
      imu.setGyroEnable(True)
      imu.setAccelEnable(True)
      imu.setCompassEnable(True)

   def get_angle(self, imu):
      while 1:
         if imu.IMURead():
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            return math.degrees(fusionPose[1])

   def init_ADC (self, ADC):
      ADC.setup()

   # Need to clean up to include % battery remaining
   def get_voltage(self, ADC):
      return ADC.read("P9_39")* 1.8 * 4.55

   def init_socket(self, server):
      host = '192.168.7.2'
      port = 12345
      server.bind((host, port))

   def get_message(self, server):
      packet = [0, 0, 0, 0, 0, 0, 0]
      server.listen(5)
      client, addr = server.accept()
      print 'Got Connection from', addr
      packet = struct.unpack('B'*len(packet), client.recv(1024))
      print packet
      return packet
