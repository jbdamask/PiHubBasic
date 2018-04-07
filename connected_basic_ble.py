from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

    def handleNotification(self, cHandle, data):
        DBG("Notification:", cHandle, "sent data", binascii.b2a_hex(data))


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
	if ("Complete" in desc):
            print "  %s = %s" % (desc, value)
            if ("Adafruit" in value):
               print "Found bluefruit. Creating Peripheral for " + dev.addr
               conn = Peripheral(dev.addr, "random")
               try:
                   for svc in conn.services:
                       print(str(svc), ":")
                       for ch in svc.getCharacteristics():
                           print("    {}, hnd={}, supports {}".format(ch, hex(ch.handle), ch.propertiesToString()))
                           chName = AssignedNumbers.getCommonName(ch.uuid)
                           if (ch.supportsRead()):
                               try:
                                   print("    ->", repr(ch.read()))
                               except BTLEException as e:
                                   print("    ->", e)
               finally:
                   conn.disconnect()
