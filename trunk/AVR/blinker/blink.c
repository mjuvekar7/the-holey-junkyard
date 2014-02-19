// standard includes
#include <avr/io.h>
#include <util/delay.h>

/*
 * This is the main method/function.
 * It contains the main executing code.
 * Pin usage--
 * 	PB0 - main output pin.
 */
int main (void)
{
    // configuring i/o pins and ports
    DDRB |= _BV(DDB0);
    PORTB &= ~_BV(PB0);
    
    while(1) 
    {
	// to toggle PB0 for blinking output
	PORTB ^= _BV(PB0);
	// delay of 100ms
	_delay_ms(100);
    }
}
