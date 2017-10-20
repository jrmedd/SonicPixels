import microbit


microbit.uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=microbit.pin14, rx=microbit.pin15)

#recommended to write pin16 low (this is the busy pin indicator)
microbit.pin16.read_digital()

Start_Byte = 0x7E
Version_Byte = 0xFF
CMD_Length = 0x06
Acknowledge = 0x00
End_Byte = 0xEF
HighByte = 0x00
LowByte = 0x00

def split(num):
    return num >> 8, num & 0xFF

def command(CMD, Par1, Par2):
    Checksum = -(Version_Byte + CMD_Length + CMD + Acknowledge + Par1 + Par2)
    HighByte, LowByte = split(Checksum)
    CommandLine = bytes([b & 0xFF for b in [
        Start_Byte, Version_Byte, CMD_Length, CMD, Acknowledge,
        Par1, Par2, HighByte, LowByte, End_Byte
    ]])
    microbit.uart.write(CommandLine)

#folders named "##", e.g. "00" to "99" with tracks named "###.mp3", e.g. "000.mp3" to "255.mp3"
def playTrack(Folder,Track):
    stopTrack()
    command(0x0F,int(Folder),int(Track))

#folders named "##", e.g. "00" to "99" with tracks named "###.mp3", e.g. "000.mp3" to "255.mp3"
def loopTrack(Folder,Track):
    stopTrack()
    command(0x0F,int(Folder),int(Track))
    command(0x19,0x00,0x00)  #loop the current track

#stops any track playing
def stopTrack():
    command(0x16,0,0)

#volume should be int between 0 (silent) and 48 (loud)
def setVolume(Volume):
    command(0x06,0,int(Volume))
