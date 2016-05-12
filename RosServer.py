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
			print "\n---- Requsisição --- "
			global ultimo
			mapa = {"Stop":(0,0), "Right": (0, 1.4), "Left":(0, -1.4), "Up":(0.15,0) ,"Down":(-0.15, 0)}
			self.data = self.request.recv(1024).strip()
			if self.data.count ("\n")> 0:
				temp = self.data.split("\n")
				temp = temp[0]
				temp = temp.split(" ")
				temp = temp[1]
				self.data = temp.replace("/","")
			robot, cmd = self.data.split ("&")
			velocidade = Twist()

			if(mapa.has_key(cmd)):
				velocidade.linear.x, velocidade.angular.z = mapa [cmd]
				print "cmd = " + str (cmd)
				if robot == "pioneer":
					print "pioneer"
					global publicadorRosP
					publicadorRos.publish (velocidade)
				elif robot == "turtlebot":
					print "turtlebot"
					global publicadorRos
					publicadorRos.publish (velocidade)
				else:
					print "404:robot"
					self.request.sendall("404: Robô não disponível")
			else:
				print "404:cmd"
				self.request.sendall("404: Comando não disponível")
		except Exception  as e:
			raise e 
			self.request.sendall(str (e))
		finally:
			self.request.sendall("Mensagem recebida")

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()

#while True: 
#	print 'tru'
