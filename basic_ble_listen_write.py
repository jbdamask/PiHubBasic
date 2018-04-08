from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers, BTLEException
import binascii

def DBG(*args):
    msg = " ".join([str(a) for a in args])
    print(msg)

class MyDelegate(DefaultDelegate):
    def __init__(self, addr):
        DefaultDelegate.__init__(self)
	self.id = addr

    def handleNotification(self, cHandle, data):
    	DBG("Notification:", cHandle, " send data ", binascii.b2a_hex(data))
	self.d = data
	map(self.broadcast, peripherals.values())

    def broadcast(self, p):
	if(self.id == p.addr):
	    print "Wait a minute, " + p.addr + " is me! I don't need to write to myself; return!"
	    return
        txh = peripherals[devices[1]].getCharacteristics(uuid=txUUID)[0]
	txh.write(self.d, True)
        

scanner = Scanner()
devices = ["e0:f2:72:20:15:43", "cd:38:25:5d:ce:a0"] # Two of my Feather boards
txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
peripherals = {}

p1 = Peripheral(devices[0], "random")
p2 = Peripheral(devices[1], "random")
peripherals[devices[0]] = p1
peripherals[devices[1]] = p2
m1 = MyDelegate(devices[0])
m2 = MyDelegate(devices[1])
p1.setDelegate(m1)
p2.setDelegate(m2)

print " Configuring RX to notify me on change"
p1.writeCharacteristic(35, b"\x01\x00", withResponse=True)
print "Subscribed to " + devices[0]
p2.writeCharacteristic(35, b"\x01\x00", withResponse=True)
print "Subscribed to " + devices[1]

while True:
    if p1.waitForNotifications(1):
	continue

p1.disconnect
p2.disconnect

