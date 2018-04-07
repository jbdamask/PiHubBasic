from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers, BTLEException
import binascii

def DBG(*args):
    msg = " ".join([str(a) for a in args])
    print(msg)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
	DBG("Notification:", cHandle, " send data ", binascii.b2a_hex(data))

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
# Currently only tx, rx and NOTIFY are supported
rxUUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
	if ("Complete" in desc):
            print "  %s = %s" % (desc, value)
            if ("Adafruit" in value):
               print "Found bluefruit. Creating Peripheral for " + dev.addr
               p = Peripheral(dev.addr, "random")
               m = MyDelegate()
               p.setDelegate(m)
               rxh = p.getCharacteristics(uuid=rxUUID)[0]
               print " Configuring RX to notify me on change"
               p.writeCharacteristic(35, b"\x01\x00", withResponse=True)
               print " Subscribed..."
               while True:
                   if p.waitForNotifications(1):
                       continue
