import Servo
from pydispatch import dispatcher

ARM = 'arm'
SAFE = 'safe'
ACTUATE = 'actuate'
puller = "HI"

class Trigger:
    def __init__(self, device, actuate):
        self.engage = False
        self.trigger = device
        self.trigger.pull = actuate
        dispatcher.connect(self.arm, signal=ARM, sender=dispatcher.Any)
        dispatcher.connect(self.safe, signal=SAFE, sender=dispatcher.Any)
        dispatcher.connect(self.fire, signal=ACTUATE, sender=dispatcher.Any)
    
    def arm(self):
        print "ARMED"
        self.trigger.armed = True
        
    def safe(self):
        print "SAFE"
        self.engage = False
        self.trigger.armed = False
    
    def fire(self):
        if self.trigger.armed:
            print "Fired!!!"
            self.trigger.pull()
        else:
            print "Not Armed!"

if __name__ == "__main__":
    mys = Servo.Servo(Servo.PARALLAX_CONTINUOUS, True)
    mys.right() #left or right depending on which way actuates the mechanism
    mys.set_speed(100)
    trig = Trigger(mys,mys.go)
    print trig.trigger.pull
    dispatcher.send(signal=ARM,sender=puller)
    dispatcher.send(signal=ACTUATE,sender=puller)
