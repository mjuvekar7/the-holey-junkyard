TARGET=atmega8535
MCU=m8535

# makefile for compiling code for AVR devices
# converting it to Intel Hex object file
# and burining it onto the AVR device

FILES=$(MCU).c

# the compiler and flags --
CC=avr-gcc
CFLAGS=-mmcu=$(TARGET) -Wall -Os -g

# converting into object file and flags --
OBJCOPY=avr-objcopy
OBJFLAGS=-j .text -j .data -O ihex

# burning onto device and options --
DUDE=avrdude
DUDEFLAGS=-p $(MCU) -c usbtiny -e

# default target compile and convert to object file
compile_obj: compile obj

# target compile
compile: $(FILES)
	$(CC) $(CFLAGS) -o $(MCU).elf $(FILES)

# target convert to object file
obj: $(MCU).elf
	$(OBJCOPY) $(OBJFLAGS) $(MCU).elf $(MCU).hex

# target burn onto device
burn: $(MCU).hex
	su -c '$(DUDE) $(DUDEFLAGS) -U flash:w:$(MCU).hex'

# target compile, convert to object file, and burn onto device 
all: compile_obj burn

# target show assembly code with corresponding source code
show_assembly: $(FILES)
	$(CC) $(CFLAGS) -Wa,-a,-ad -o $(PROJ).out $(FILES) > $(PROJ).lst

# target clean backups, assembly, executables
clean:
	-rm -f *~ *.lst *.out