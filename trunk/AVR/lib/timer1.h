#ifndef TIMER1_LIB
#define TIMER1_LIB

#include <avr/io.h>

#define BOTTOM          0x0000
#define MAX             0xFFFF
#define PRESCALE_VALUES 5
#define CONTROL_A       TCCR1A
#define CONTROL_B       TCCR1B
#define COUNT           TCNT1
#define INTERRUPT_MASK  TIMSK
#define INTERRUPT_FLAG  TIFR

uint8_t prescale_values [PRESCALE_VALUES] = {1, 8, 64, 256, 1024};

#endif