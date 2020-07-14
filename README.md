# alphaprint

A command-line utility to print to AlphaCom throught the LPD protocol. Supports a user-specified port, host, file and printer.
Written in Python 3.x. Backwards compatible to Python 2.x

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
Output text: File sent Successfully. Closing File...
Output file: Alpha Document.prn
Contents: THIS IS A TEST (60 times)

```
AlphaPrint.py -v -p 515 -o HelloWorld.txt -d Test
```

