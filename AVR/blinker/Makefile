PROJECTNAME=blink
TARGET=
MCU=
F_CPU=`

# makefile for compiling code for AVR devices
# converting it to Intel Hex object file
# and burining it onto the AVR device

FILES=blink.c

# the compiler and flags --
CC=avr-gcc
CFLAGS=-mmcu=$(TARGET) -Wall -Os -g -DF_CPU=$(F_CPU)

# converting into object file and flags --
OBJCOPY=avr-objcopy
OBJFLAGS=-j .text -j .data -O ihex

# burning onto device and options --
DUDE=avrdude
DUDEFLAGS=-p $(MCU) -c usbtiny -e -U

# default target -- compile and convert to object file
compile_obj: compile obj

# target compile
compile: $(FILES)
	$(CC) $(CFLAGS) -o $(PROJECTNAME).elf $(FILES)

# target convert to object file
obj: $(PROJECTNAME).elf
	$(OBJCOPY) $(OBJFLAGS) $(PROJECTNAME).elf $(PROJECTNAME).hex

# target burn onto device
burn: $(PROJECTNAME).hex
	sudo $(DUDE) $(DUDEFLAGS) flash:w:$(PROJECTNAME).hex

# target compile, convert to object file, and burn onto device 
all: compile_obj burn

# target show assembly code with corresponding source code
show_assembly: $(FILES)
	$(CC) $(CFLAGS) -Wa,-a,-ad -o $(PROJECTNAME).out $(FILES) > $(PROJECTNAME).lst

# target clean all files except source
clean:
	-rm -f *~ *.elf *.hex *.lst *.out
