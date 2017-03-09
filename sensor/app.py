import os
import sys
import time
import requests

from sensor import Sensor
from daemon import Daemon

urlStart = "http://0.0.0.0:5000/occupied"
urlStop= "http://0.0.0.0:5000/free"

delay = 150 # ~ 25 sec
timestamp = 0.1
sensor = Sensor()

class PirSensor(object):
    trigger = 0
    lastResult = -1

    def detectState(self):
        status = sensor.status()
        if status == 1: 
            self.trigger = delay
            if self.lastResult != status:
                self.lastResult = status
                self.callBusy()
        elif status == 0:
            self.trigger = self.trigger - 1
            if self.trigger < 0 and self.lastResult != status:
                self.lastResult = status
                self.callFree()         

    def callBusy(self):
        try:
            requests.get(urlStart)
        except:
            return

    def callFree(self):
        try:
            requests.get(urlStop)
        except:
            return
        
    def run(self):
        try:
            while True:
                self.detectState()
                time.sleep(timestamp)
        finally:
            sensor.clean()

class PirSensorDaemon(Daemon):
    def run(self):
        your_code = PirSensor()
        your_code.run()

if __name__ == "__main__":
    daemon = PirSensorDaemon(str(os.path.dirname(os.path.realpath(__file__))) + '/deamon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            sensor.clean()
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            sensor.clean()
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)