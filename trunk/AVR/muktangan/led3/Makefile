#  make:               to compile
#  make burn:          to burn to device
#  make all:           to compile and burn to device
#  make clean:         to remove backup files and assembly files
#  make assembly:      to show assembly code alongside source code
PROJECTNAME=lc_main

# fill in target (eg. atmega8) and MCU (eg. m8), and project name (eg. blinker)
TARGET=atmega8535
MCU=m8535

# fill in CPU frequency (eg. 1000000L)
F_CPU=1000000L

# makefile for compiling code for AVR devices
# converting it to Intel Hex object file
# and burining it onto the AVR device

# fill in source files
FILES=src/physical.c src/common.c src/trial.c

# the compiler and flags --
CC=avr-gcc
CFLAGS=-mmcu=$(TARGET) -Wall -Os -g -DF_CPU=$(F_CPU)

# converting into object file and flags --
OBJCOPY=avr-objcopy
OBJFLAGS=-j .text -j .data -O ihex

# burning onto device and options --
DUDE=avrdude
DUDEFLAGS=-p $(MCU) -c usbtiny -e

# default target -- compile and convert to object file
compile_obj: compile obj

# target compile
compile: $(FILES)
	$(CC) $(CFLAGS) -o bin/$(PROJECTNAME).elf $(FILES)

# target convert to object file
obj: bin/$(PROJECTNAME).elf
	$(OBJCOPY) $(OBJFLAGS) bin/$(PROJECTNAME).elf bin/$(PROJECTNAME).hex

# target burn onto device
burn: bin/$(PROJECTNAME).hex
	sudo $(DUDE) $(DUDEFLAGS) -U flash:w:bin/$(PROJECTNAME).hex

# target compile, convert to object file, and burn onto device 
all: compile_obj burn

# target assembly code with corresponding source code
assembly: $(FILES)
	$(CC) $(CFLAGS) -Wa,-a,-ad -o bin/$(PROJECTNAME).out $(FILES) > bin/$(PROJECTNAME).lst

# target clean files
clean:
	-rm -f *~ *.lst *.out
