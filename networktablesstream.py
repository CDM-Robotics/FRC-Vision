
# import the necessary packages
from threading import Thread
from networktables import NetworkTables

class NetworkTablesStream:
	def __init__(self, server_name='roborio-6072-frc.local'):
		# initialize the video camera stream and read the first frame
		# from the stream
		NetworkTables.initialize(server=server_name)
		self.table = NetworktTables.getTable('vision_data')
		self.send_data()
		self.send_viewability()
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			self.table.putNumber("horizontal_angle",self.horizontal_angle)
			self.table.putNumber("vertical_angle",self.vertical_angle)
			self.table.putNumber("distance",self.distance)
			self.table.putBoolean("viewable",self.in_view)

	def send_data(self,horiz_angle=0,vert_angle=0,dist=0):
		# return the frame most recently read
		self.horizontal_angle=horiz_angle
		self.vertical_angle=vert_angle
		self.distance=dist
	def send_viewability(self, viewable=false):		
		self.in_view=viewable
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
