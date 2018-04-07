from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers, BTLEException
import binascii

def DBG(*args):
    msg = " ".join([str(a) for a in args])
    print(msg)

scanner = Scanner()
devices = scanner.scan(10.0)
txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

msg = "21420894"

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
	if ("Complete" in desc):
            print "  %s = %s" % (desc, value)
            if ("Adafruit" in value):
                print "Found bluefruit. Creating Peripheral for " + dev.addr
                p = Peripheral(dev.addr, "random") # BluePy default is "public" so we have to set it to random or it won't connect
	        tx = p.getCharacteristics(uuid=txUUID)[0]
	       	try:
		    tx.write(binascii.unhexlify(msg), True)
		except BTLEException:
           	    print BTLEException.message
        	except BaseException:
            	    print "BaseException caught in Thread"
            	    print BaseException.message
		except Exception:
		    print "Caught unknown exception"
		    print Exception.message
	        p.disconnect()
