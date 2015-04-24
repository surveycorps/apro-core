from apro import APRO
from nrf24 import NRF24

import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math

s = RTIMU.Settings("RTIMULib")
imu = RTIMU.RTIMU(s)

robot = APRO(0)
radio = NRF24()
robot.init_radio(radio)
robot.init_imu(imu)
robot.set_pwm(0, 125, 255)
robot.set_dir(0, 1, 1)
angle = robot.get_angle(imu)
print(angle)
while 1:
   robot.transmit(radio)
   time.sleep(1)
   robot.set_pwm(129, 150, 78)
   robot.set_dir(1,1,0)
   robot.transmit(radio)
   time.sleep(1)
   robot.set_pwm(200, 230, 0)
   robot.set_dir(0,0,1)
