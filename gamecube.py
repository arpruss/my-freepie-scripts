from System.IO.Ports import SerialPort
import struct
import time

STATE_WAITING = 0
STATE_PACKET_STARTED = 1

def processPacket(packet):
    packetTime = time.time()
    diagnostics.debug(str(packet))

def update(sender, e):
   global state,packet
   data = sender.ReadExisting()
   for c in data:
        if state==STATE_WAITING:
            if c == b"G":
                state = STATE_PACKET_STARTED
                packet = b""
            elif c == b"E":
                diagnostics.debug("Err")            
        elif state==STATE_PACKET_STARTED:
            packet += c
            if len(packet) == 8:
                processPacket(packet)
                state = STATE_WAITING
                            
   diagnostics.debug(data)
   diagnostics.debug(str(struct.unpack("B",data[:1])))

if starting:
   global port
   global connected
   global state
   global packet
   global packetTime
   port = SerialPort("COM3", 115200)
   port.Open()
   port.DataReceived += update
   connected = False
   state = STATE_WAITING
   diagnostics.debug("started")
else:
   if not connected:
       try:
            port.Write("*#1c810")
            connected = True
            packetTime = time.time()
       except:
            pass
   else:
       if packetTime + 2 < time.time():
            connected = False
       pass
   
if stopping:
   port.Close()
