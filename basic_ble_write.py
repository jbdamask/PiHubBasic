from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers, BTLEException
import binascii

def DBG(*args):
    msg = " ".join([str(a) for a in args])
    print(msg)

scanner = Scanner()
devices = scanner.scan(10.0)
txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

p = Peripheral("e0:f2:72:20:15:43", "random")
tx = p.getCharacteristics(uuid=txUUID)[0]
msg = "21420894"
try:
#    tx.write("21430399", True)
    tx.write(binascii.unhexlify(msg), True)
except BTLEException:
    print "Caught BTLEException:"
    print BTLEException.message
except BaseException:
    print "Caught BaseException"
    print BaseException.message
except Exception:
    print "Exception"
    print Exception.message


#for dev in devices:
#    for (adtype, desc, value) in dev.getScanData():
#	if ("Complete" in desc):
#            print "  %s = %s" % (desc, value)
#            if ("Adafruit" in value):
#                print "Found bluefruit. Creating Peripheral for " + dev.addr
#                p = Peripheral(dev.addr, "random")
#	        tx = p.getCharacteristics(uuid=txUUID)[0]
#	       	try:
#		    tx.write("21420399", True)
#		except BTLEException:
#           	    print BTLEException.message
#        	except BaseException:
#            	    print "BaseException caught in Thread"
#            	    print BaseException.message
#		except Exception:
#		    print "Caught unknown exception"
#		    print Exception.message
#	        p.disconnect()
#               rxh = p.getCharacteristics(uuid=rxUUID)[0]
#               print " Configuring RX to notify me on change"
#               p.writeCharacteristic(35, b"\x01\x00", withResponse=True)
#               print " Subscribed..."
#               while True:
#                   if p.waitForNotifications(1):
#                       continue
