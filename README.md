# alphaprint

A command-line utility to print to AlphaCom through the LPD protocol. Supports a user-specified port, host, file and printer.
Written in Python 3.x. Backwards compatible to Python 2.x.  
Tested on Windows 10 with both python 3.x and 2.x.  

## Installation

Install from https://github.com/omnicomtech/alphaprint and run through command line.


## Usage

```
AlphaPrint.py #Prints "THIS IS A TEST" 60 times on the local machine to a printer named Test
AlphaPrint.py -v #Produces verbose output as well as hexdump and step-by-step confirmation
AlphaPrint.py -h #Show help text along with a list of possible flags and their uses 
```
All flags:
```
AlphaPrint.py -p Port -o Filename -i Hostname -d Printer
```

## Examples

```
AlphaPrint.py
```
Output text: File sent Successfully. Closing connection...   
Output file: Alpha Document.prn   
Contents: THIS IS A TEST (60 times)   

```
AlphaPrint.py -v -p 515 -o HelloWorld.txt -i host -d Test
```
Output text:
```
Python version
2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
Version info.
sys.version_info(major=2, minor=7, micro=18, releaselevel='final', serial=0)

Connected to host on port 515
Establishing printer...
00000000  02 54 65 73 74 0a                                   .Test.
Success. Proceed

Assembling control file...
00000000  02 34 33 20 63 66 41 30   30 30 4a 61 7a 7a 0a      .43 cfA000Jazz.
Success. Proceed

Sending control file...
00000000  48 68 6f 73 74 2e 4e 48   65 6c 6c 6f 57 6f 72 6c   Hhost.NHelloWorl
00000010  64 2e 74 78 74 2e 50 75   73 65 72 2e 6f 48 65 6c   d.txt.Puser.oHel
00000020  6c 6f 57 6f 72 6c 64 2e   74 78 74 2e               loWorld.txt.
Success. Proceed

Assembling and sending data file...
00000000  2e 39 30 30 20 64 66 41   30 30 30 68 6f 73 74 2e   .900 dfA000host.
Success. Proceed

Sending print job...
Closing connection...
```
Output file: Alpha Document.prn   
Contents: Hello World   

## Troubleshooting
Most errors are down to newer printers not supporting LPD. Follow [these steps](http://www.kbytes.co.uk/Articles.asp?articleid=58) to set up a text-only printer named 'Test' to test the functionality of the utility. These same steps also work on Windows 10.
