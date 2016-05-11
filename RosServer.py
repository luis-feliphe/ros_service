# -*- coding: utf-8 -*-
import SocketServer
import rospy
from geometry_msgs.msg import Twist

import threading
import time


import os


###################################################################################
#### This file is responsible for reveive events from socketss and send to  ROS ###
###################################################################################


rospy.init_node ("controlador_web")
global publicadorRos
publicadorRos = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist)
global publicadorRosP
publicadorRosP = rospy.Publisher("RosAria/cmd_vel", Twist)
global ultimo
ultimo = None


class MapGenerate(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			time.sleep(8)
			retvalue = os.system("rosrun map_server map_saver")
			retvalue = os.system("convert map.pgm ./static/map.jpg")

gen = MapGenerate()
#gen.start()

class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		try:
			global ultimo
			mapa = {"Stop":(0,0), "Right": (0, 1.4), "Left":(0, -1.4), "Up":(0.15,0) ,"Down":(-0.15, 0)}
			self.data = self.request.recv(1024).strip()
			print str (self.data)
	#		print "{} wrote:".format(self.client_address[0])
	#		print str(mapa[self.data])
			velocidade = Twist()
			if self.data == "t1":
				global publicadorRos
				ultimo = publicadorRos
				print "setando para T1"
			elif(self.data =="p1"):
				global publicadorRosP
				ultimo = publicadorRosP
				print "setando para P1"
			elif(mapa.has_key(self.data)):
				print "publicando velocidade"
				velocidade.linear.x, velocidade.angular.z = mapa [self.data]
				ultimo.publish (velocidade)
			
				self.request.sendall("Mensagem recebida")
			else:
				print " Não foi possível interpretar o comando recebido."
		except Exception  as e:
			print "Ocorreu um erro inesperado"
		finally:
			print "Tentando recuperar"

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()

#while True: 
#	print 'tru'
