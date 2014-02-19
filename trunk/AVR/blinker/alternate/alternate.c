#define F_CPU 1000000UL

#include <avr/io.h>
#include <util/delay.h>

int
main (void)
{
    DDRB |= _BV(DDB0);
    DDRB |= _BV(DDB1);
    
    PORTB = 0xFF;
    while(1) 
    {
        PORTB ^= _BV(PB0);
	_delay_ms(1000);
	PORTB ^= _BV(PB0);
	PORTB ^= _BV(PB1);
	_delay_ms(1000);
	PORTB ^= _BV(PB1);
    }
}