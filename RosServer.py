import SocketServer
import rospy
from geometry_msgs.msg import Twist

###################################################################################
#### This file is responsible for reveive events from socketss and send to  ROS ###
###################################################################################


rospy.init_node ("controlador_web")
global publicadorRos
publicadorRos = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist)


class MyTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		global publicadorRos
		mapa = {"Right": (0, 1.4), "Left":(0, -1.4), "Up":(0.15,0) ,"Down":(-0.15, 0)}
		self.data = self.request.recv(1024).strip()
#		print "{} wrote:".format(self.client_address[0])
#		print str(mapa[self.data])
		velocidade = Twist()
		velocidade.linear.x, velocidade.angular.z = mapa [self.data]
		publicadorRos.publish (velocidade)
		
		self.request.sendall("Mensagem recebida")

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()


