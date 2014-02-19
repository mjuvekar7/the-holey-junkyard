#ifndef TIMER0_LIB
#define TIMER0_LIB

#include <avr/io.h>

#define BOTTOM          0x00
#define MAX             0xFF
#define PRESCALE_VALUES 5
#define CONTROL         TCCR0
#define COUNT           TCNT0
#define INTERRUPT_FLAG  TIFR
#define INTERRUPT_MASK  TIMSK

uint8_t prescale_values [PRESCALE_VALUES] = {1, 8, 64, 256, 1024};

void clk_external_falling (void);
void clk_external_rising (void);
void reset (void);
void set_prescale (uint8_t prescale);
void start (void);
void wait (uint8_t count);
uint8_t get_count (void);

void clk_external_falling (void)
{
    CONTROL = 0x06;
}

void clk_external_rising (void)
{
    CONTROL = 0x07;
}

void reset (void)
{
    COUNT = BOTTOM;
}

void set_prescale (uint8_t prescale)
{
    uint8_t i;
    for (i = 0; i < PRESCALE_VALUES; i++)
    {
	if (prescale == prescale_values[i])
	{
	    CONTROL = i + 1;
	    return;
	}
    }
}

void start (void)
{
    if (CONTROL == 0) CONTROL = 1;
    reset();
}

void wait (uint8_t count)
{
    reset();
    while (COUNT != count);
}

uint8_t get_count (void)
{
    return COUNT;
}

#endif