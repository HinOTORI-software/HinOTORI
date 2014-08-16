#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import AllunaToolKit
import time

class TelescopeServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -p 10001")

		telescope = Telescope()
		adapter.add(telescope, self.communicator().stringToIdentity("telescope"))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Telescope(HinOTORI.Telescope,AllunaToolKit.Telescope):
	def __init__(self):
		self.z=0.
		HinOTORI.Telescope.__init__(self)
		AllunaToolKit.Telescope.__init__(self)
		self.Connect()

	def GetFocusZ(self,current=None):
		self.z = self.FocusingPosition()
		print "Telescope: z= %lf" % self.z
		return self.z

	def SetFocusZ(self,targetz,current=None):
		self.z=targetz
		self.FocusingTargetPosition(self.z)

if __name__ == "__main__":
	app = TelescopeServer()
	status = app.main(sys.argv)
	sys.exit(status)