#!/usr/bin/env python

#Jazz Sussman Moss
#6/25/2020

#imports
import socket, time, os, getpass, string, sys, argparse

parser = argparse.ArgumentParser(description="defaults")
parser.add_argument('-v', action='store_true', help='Use to enable verbose mode. Displays hexdump and some step-by-step confirmation')

parser.add_argument('-p', action="store", dest = "p", default=False, help="Set port. Don't specify for default")
parser.add_argument('-o', action="store", dest = "o", default=False, help="Set filename. Don't specify for default")
parser.add_argument('-i', action="store", dest = "i", default=False, help="Set set hostname. Don't specify for default")
parser.add_argument('-d', action="store", dest = "d", default=False, help="Set printer. Don't specify for default")


args = parser.parse_args()


port = args.p
filename = args.o
hostname = args.i
printer = args.d
verbose = args.v

if not hostname:
    hostname = socket.gethostname()
if not port:
    port = 515
else:
    try:
        port = int(port)
    except:
        print("Connection failed. Port designation must be an integer")
if not filename:
    filename = "AlphaFile.txt"
if not printer:
    printer = "Test"

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

#argv = input("Please input [host printer port filename] as shown, use an 'x' for default: ")
#argv = argv.split()

user = getpass.getuser()  #should work on windows or linux  

def ack(): #sends for acknowledgment from server and if there's a NAK shows error code
    ack2 = s.recv(1024)
    ack = ack2.decode('utf-8', 'replace')
    if ack == '\x00': #everything is good
        print("Success. Proceed")
        print("")
        ack = "unknown"
    else:
        s.send(bytes("\001\012","utf-8")) #abort print job
        enablePrint()
        if ack2!=b'\xff':
            print("Encountered error. Code "+ str(ack2) + ". Cancelling print") #hopefully readable error
        else: #the only time it doesn't send back b'\xff' is for unrecognised printer, so this may help
            print("Encountered error. Likely to do with printer name " + printer+ ". Please ensure this is a valid printer.")
        s.close()
        sys.exit(0)

def hex(s): #formats output as hex string
   return " ".join("{:02x}".format(ord(i)) for i in s)

def hexdump(z): #formats as readable hexdump
    hexed = (hex(z))
    strlen = len(z)
    lines = (strlen + (15)) // 16 #how many lines the ouput will be, saves having to import math for math.ceil
    counter = 0
    counter2 = 0
    printable = ""
    for i in range(len(z)): #checks for charachters not 32 <= x < 127
        if 32 <= ord(z[i]) < 127:
            printable = printable + z[i]
        else:
            printable = printable + "."    
    for i in range(lines):
        if i+1 != lines:  
            print("000000"+str(i)+"0"+"  "+hexed[counter:counter+24]+"  "+hexed[counter+24:counter+48]+"  "+printable[counter2:counter2+16])
            counter+=48
            counter2+=16
        else: #last line needs to be different, because of whitespace
            wht1 = ""
            wht2 = ""
            len1 = (len(hexed[counter:counter+24]))
            len2 = len(hexed[counter+24:counter+48])
            for k in range(24-len1):
                wht1 = wht1+" "
            for k in range(24-len2):
                wht2 = wht2+" "        
            print("000000"+str(i)+"0"+"  "+hexed[counter:counter+24]+wht1+"  "+hexed[counter+24:counter+48]+wht2+"  "+printable[counter2:counter2+16])

#Prints out some information that might be useful, not sure
if verbose:
    print("Python version")
    print (sys.version)
    print("Version info.")
    print (sys.version_info)
    print(" ")

if not verbose:
    blockPrint()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #open connection
    s.connect((hostname, port))
    print("Connected to "+ str(hostname)+ " on port "+str(port))
except socket.error:
    print("Connection failed, retrying..")
    time.sleep(2) #in case something else was interfering with port, read it might cause issues
    try: #tries again as above
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        print("Connected to "+ str(hostname)+ " on port "+str(port))
    except socket.error:
        print()
        enablePrint()
        print("Connection to "+ str(hostname)+ " on port "+ str(port)+ " failed")
        sys.exit(0)

#s.send(bytes("\002Test\n","utf-8"))
#MAY NOT BE NEEDED NOW

if filename != "AlphaFile.txt": #if they specified a file
    f = open(filename, "rb")
    l = f.read()

    #length of file. I think this is better than len() for this implementation
    f.seek(0, 2)
    length = f.tell()
    f.seek(0, 0)
else: #If they didn't default file contents
    contents = "THIS IS A TEST\012"
    length = len(contents)*60


s.send("\002"+printer+"\012".encode("utf-8")) #establish printer
print("Establishing printer...")
hexdump("\002"+printer+"\012")
ack()


#compile control file--------------------------------
control = 'H'+hostname+"\012"+'N'+filename+"\012"+'P'+user+"\012"+'o'+filename+"\012"
s.send("\002"+str(len(control))+" cfA000"+hostname+"\012".encode("utf-8"))

print("Assembling control file...")
hexdump("\002"+str(len(control))+" cfA000"+hostname+"\012")
ack()

print("Sending control file...")
hexdump(control)
s.send(control.encode("utf-8"))

s.send("\000".encode("utf-8"))

ack()
#end of control file


#compile data file--------------------------------
data = "\003"+str(length)+" dfA000"+hostname+"\012"
s.send(data.encode("utf-8"))
print("Assembling and sending data file...")
hexdump(data)

ack()
#end of data file


#Sending data--------------------------------
print("Sending print job...")

if filename!="AlphaFile.txt": #send their file
    while True:
        contents = f.readline()
        if not contents:
            break
        s.send(contents)
else: #send a the default file
    for i in range(60):
        s.send(contents.encode("utf-8"))

s.send("\000".encode("utf-8"))

print("Closing connection...")
if not verbose:
    enablePrint()
    print("File sent succesfully. Closing connection...")
s.close()
sys.exit(0)