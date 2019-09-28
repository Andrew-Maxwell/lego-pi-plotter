import numpy
import sys
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD)
	
class plotter:
	
	def __init__(self):

		#given in mm/second
		
		self.zplusmaxspeed = 2.5
		self.zminusmaxspeed = 2.5
		
		#Distance along the axis the pen will travel in e.g. 0.05 seconds
		
		self.tplus005 = 0.002698
		self.tminus005 = -0.00255
		self.rplus005 = 0.518
		self.rminus005 = -0.488
		
		#position of R axis hits stop
		
		self.raxis = self.rzero = -1.5
		
		#R distance buffer
		
		self.rstore = 0
		
		#Time this motor turned off
		
		self.rstoptime = 0.0
		
		self.taxis = self.tzero = 0.371
		self.tstore = 0
		self.tstoptime = 0.0
		
		self.zaxis = 0
		self.xaxis = self.xzero = 32
		
		self.radius = 88.25
		
		#Defines the margin of error when driving a motor to the stop to reset
		
		self.rzeromargin = 3.5	
		self.tzeromargin = 0.025
		
		#Used for milling experiments
		
		self.timedelay = 0
		
		#GPIO pin assignments
		
		self.zplusout = 8
		self.zminusout = 10
		
		self.rplusout = 18
		self.rminusout = 16
		
		self.tplusout = 24
		self.tminusout = 26
		
		self.enable = 12
				
		GPIO.setup(zplusout, GPIO.OUT)
		GPIO.setup(zminusout, GPIO.OUT)
		GPIO.setup(rminusout, GPIO.OUT)
		GPIO.setup(rplusout, GPIO.OUT)
		GPIO.setup(tplusout, GPIO.OUT)
		GPIO.setup(tminusout, GPIO.OUT)
		GPIO.setup(enable, GPIO.OUT)
		
	def stop(self):
		GPIO.output(self.zplusout, GPIO.LOW)
		GPIO.output(self.zminusout, GPIO.LOW)
		GPIO.output(self.rminusout, GPIO.LOW)
		GPIO.output(self.rplusout, GPIO.LOW)
		GPIO.output(self.tplusout, GPIO.LOW)
		GPIO.output(self.tminusout, GPIO.LOW)
		GPIO.output(self.enable, GPIO.LOW)
	
	#Moves R axis as long as mm is greater than one step
	
	def rmove(self, mm):
		self.rstore += mm
		while (self.rstore > self.rplus005):
			self.rmoveplus(0.05)
			self.rstore -= self.rplus005
			self.raxis += self.rplus005
		while (self.rstore < self.rminus005):
			self.rmoveminus(0.05)
			self.rstore -= self.rminus005
			self.raxis += self.rminus005
	
	#Moves R motor in positive direction for S seconds
	
	def rmoveplus(self, s):
		if (time.time() - self.rstoptime < 0.2):
			time.sleep(0.2)
		GPIO.output(self.rminusout, GPIO.LOW)
		GPIO.output(self.rplusout, GPIO.HIGH)
		GPIO.output(self.enable, GPIO.HIGH)
		time.sleep(s)
		GPIO.output(self.rminusout, GPIO.HIGH)
		GPIO.output(self.rplusout, GPIO.HIGH)
		self.rstoptime = time.time()
	
	#Moves R motor in negative direction for S seconds
	
	def rmoveminus(self, s):
		if (time.time() - self.rstoptime < 0.2):
			time.sleep(0.2)
		GPIO.output(self.rminusout, GPIO.HIGH)
		GPIO.output(self.rplusout, GPIO.LOW)
		GPIO.output(self.enable, GPIO.HIGH)
		time.sleep(s)
		GPIO.output(self.rminusout, GPIO.HIGH)
		GPIO.output(self.rplusout, GPIO.HIGH)
		self.rstoptime = time.time()
	
	#Moves T axis as long as theta argument is greater than one step
	
	def tmove(self, theta):
		self.tstore += theta
		while (self.tstore > self.tplus005):
			self.tmoveplus(0.05)
			self.tstore -= self.tplus005
			self.taxis += self.tplus005
		while (self.tstore < self.tminus005):
			self.tmoveminus(0.05)
			self.tstore -= self.tminus005
			self.taxis += self.tminus005
	
	#Moves T motor in negative direction for S seconds
	
	def tmoveminus(self, s):
		if (time.time() - self.tstoptime < 0.2):
			time.sleep(0.2)
		GPIO.output(self.tplusout, GPIO.LOW)
		GPIO.output(self.tminusout, GPIO.HIGH)
		GPIO.output(self.enable, GPIO.HIGH)
		time.sleep(s)
		GPIO.output(self.tplusout, GPIO.HIGH)
		GPIO.output(self.tminusout, GPIO.HIGH)
		self.tstoptime = time.time()
	
	#Moves T motor in positive direction for S seconds
	
	def tmoveplus(self, s):
		if (time.time() - self.tstoptime < 0.2):
			time.sleep(0.2)
		GPIO.output(self.tplusout, GPIO.HIGH)
		GPIO.output(self.tminusout, GPIO.LOW)
		GPIO.output(self.enable, GPIO.HIGH)
		time.sleep(s)
		GPIO.output(self.tplusout, GPIO.HIGH)
		GPIO.output(self.tminusout, GPIO.HIGH)
		self.tstoptime = time.time()
	
	#Moves Z axis approximately "mm" mm
	
	def zmove(self, mm):
		if(mm > 0):
			GPIO.output(self.zplusout, GPIO.HIGH)
			GPIO.output(self.zminusout, GPIO.LOW)
			GPIO.output(self.enable, GPIO.HIGH)
			time.sleep(mm / self.zplusmaxspeed)
		else:
			GPIO.output(self.zplusout, GPIO.LOW)
			GPIO.output(self.zminusout, GPIO.HIGH)
			GPIO.output(self.enable, GPIO.HIGH)
			time.sleep(-1 * mm / self.zminusmaxspeed)
		self.stop()
		self.zaxis += mm
	
	#Moves R and T axis to a given point (xf, yf)
	
	def movepoint(self, xf, yf):
		self.tmove(numpy.arcsin(xf / self.radius) - self.taxis)
		time.sleep(self.timedelay)
		self.rmove(yf - self.radius * numpy.cos(numpy.arcsin(xf / self.radius)) - self.raxis)
		time.sleep(self.timedelay)
		self.xaxis = xf	
		print("(" + str(xf) + ", " + str(yf) + ")")
	
	#Moves R and T axis between a series of points on a line in X-Y system
	
	def movesmooth(self, xf, yf, steps):
		xi = self.xaxis
		yi = self.raxis + self.radius * numpy.cos(self.taxis)
		for i in range(1, 1 + steps):
			self.movepoint(xi + i * (xf - xi) / float(steps), yi + i * (yf - yi) / float(steps))
			
	#Resets R axis against stop
	
	def rset(self):
		self.rmove(-1 * (self.raxis - self.rzero + self.rzeromargin))
		self.raxis = self.rzero
	
	#Resets T axis against stop
	
	def tset(self):
		self.tmove(self.tzero - self.taxis + self.tzeromargin)
		self.tmoveminus(0.15)
		self.taxis = self.tzero
		self.xaxis = self.xzero
	
	#Resets Z axis so pen is touching the paper (acts as a stop)
	
	def zset(self):
		self.zmove(-1 * (self.zaxis + 5))
		self.zaxis = 0
	
#Prints octagonal smiley face

def smiley(p):
	p.tset()
	p.rset()
	p.zmove(5)
	p.movesmooth(5, 90, 10)
	p.zset()
	p.movesmooth(15, 100, 20)
	p.movesmooth(15, 110, 20)
	p.movesmooth(5, 120, 20)
	p.movesmooth(-5, 120, 20)
	p.movesmooth(-15, 110, 20)
	p.movesmooth(-15, 100, 20)
	p.movesmooth(-5, 90, 20)
	p.movesmooth(5, 90, 20)
	p.zmove(5)
	p.movesmooth(10, 100, 10)
	p.zset()
	p.movesmooth(5, 95, 20)
	p.movesmooth(-5, 95, 20)
	p.movesmooth(-10, 100, 20)
	p.zmove(5)
	p.movesmooth(-10, 105, 10)
	p.zset()
	p.movesmooth(-7, 110, 20)
	p.movesmooth(-5, 105, 20)
	p.zmove(5)
	p.movesmooth(5, 105, 10)
	p.zset()
	p.movesmooth(7, 110, 20)
	p.movesmooth(10, 105, 20)
	p.zmove(5)
	p.tset()
	p.rset()
	p.zset()

#Diamond+square test pattern

def diamond(p):
	p.rset()
	p.tset()
	p.zmove(5)
	p.movepoint(15, 115)
	p.zset()
	for x in range(4):
		p.movesmooth(0, 130, 40)
		p.movesmooth(-15, 115, 40)
		p.movesmooth(0, 100, 40)
		p.movesmooth(15, 115, 40)
		p.movesmooth(15, 130, 40)
		p.movesmooth(-15, 130, 40)
		p.movesmooth(-15, 100, 40)
		p.movesmooth(15, 100, 40)
		p.movesmooth(15, 115, 40)
	p.zmove(5)
	p.rset()
	p.tset()
	p.zset()

#Star pattern	

def star(p):
	p.zmove(5)
	p.movepoint(30, 115)
	p.zset()
	p.movesmooth(-10, 115, 80)
	p.movesmooth(20, 90, 80)
	p.movesmooth(10, 130, 80)
	p.movesmooth(0, 90, 80)
	p.movesmooth(30, 115, 80)
	p.zmove(5)
	p.tset()
	p.rset()
	p.zset()
	
p = plotter()

star(p)
diamond(p)
smiley(p)

print("Done!")

GPIO.cleanup()
